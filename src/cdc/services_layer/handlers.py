import logging
from datetime import datetime

from setup import domain  # type: ignore
from setup.adapters import bus, podemos_mambu, smtp
from setup.domain import events
from setup.sessions import current_user
from shared.cdc_utils import CDCResponse
from src.cdc import config, utils
from src.cdc.adapters import file_service
from src.cdc.adapters.credit_service import CDCService
from src.cdc.adapters.pdf_service import CDCPdfService
from src.cdc.adapters.xml_service import CDCXmlService
from src.cdc.domain import commands, models, queries
from src.cdc.errors import CdcError
from src.cdc.services_layer import unit_of_work
from src.cdc.utils import _gen_tribus_usuario_2
from src.cdc.validations.utils.evaluations_rules import EvaluateRules

from typing import Callable, Dict, Type  # isort:skip

logger = logging.getLogger(__name__)


def add_person(
    command: commands.ADDPerson,
    uow: unit_of_work.UnitOfWorkCdc,
    mambu: podemos_mambu.PodemosMambu,
    bus: bus.AbstractBus,
) -> Dict:
    with uow:
        logger.info("Se inicia consulta  %s", command.curp)
        user = current_user()
        if not command.apellido_materno:
            command.apellido_materno = "NO PROPORCIONADO"
        person = models.Person(
            command.nombre,
            command.apellido_paterno,
            command.apellido_materno,
            command.fecha_nacimiento,
            command.curp,
            command.rfc,
            command.nacionalidad,
            command.direccion,
            command.colonia,
            command.delegacion,
            command.ciudad,
            command.estado,
            command.codigo_postal.zfill(5),
            command.es_referida,
        )
        try:
            logger.info("Se guarda informacion integrante  %s", command.curp)
            uow.persons.add_person(command.grupo_id, person)
            uow.commit()
            logger.info("Se genera consulta integrante  %s", command.curp)
            today = datetime.today()
            timestamp_consulta = datetime.now()
            folios = uow.query_status.get_folios(user.username, today)  # type: ignore
            # mambu
            mambu_user = mambu.users.get(id=user.username)
            try:
                branch_name = mambu_user.assigned_branch.name
            except Exception:
                branch_name = ""

            # generacion de folio
            querycdc = models.QueryCdc(
                centro_comunitario=branch_name,
                username=user.username,
                timestamp_consulta=timestamp_consulta,
                timestamp_aprobacion_consulta=command.timestamp_aprobacion_consulta,
                timestamp_aprobacion_tyc=command.timestamp_aprobacion_tyc,
                estatus_consulta_id=1,
                usuario_cdc=config.CDC_USERNAME,
                tipo_consulta=config.CDC_TIPO_CONSULTA,
                nip=command.nip,
            )
            querycdc.generate_folio(user=mambu_user, folios=folios)
            logger.info("Se guarda consulta de integrante  %s", command.curp)
            person.add_query_cdc(querycdc)
            uow.commit()

            xml_response: str = CDCService.consult(
                person=person, folio=querycdc.folio, nip=querycdc.nip
            )
            xml_service = CDCXmlService()

            try:
                credit_data = CDCResponse.from_response(
                    response=xml_response, claves_permitidas=config.CLAVES_PERMITIDAS
                )
                is_success = credit_data.error is None
                xml_service.save(
                    folio=querycdc.folio, xml_response=xml_response, is_success=is_success
                )
            except Exception as ex:  # pragma: no cover
                xml_service.save(
                    folio=querycdc.folio, xml_response=xml_response, is_success=False
                )
                querycdc.estatus_consulta_id = 5
                uow.commit()
                logger.error("Error en formato de respuesta de CDC: %s", str(ex))
                raise Exception("Error en respuesta de CDC.")

            if credit_data.error is not None:
                logger.error(
                    "Error con consulta a círculo de credito %s %s %s",
                    command.curp,
                    credit_data.encabezado.folio_consulta,
                    querycdc.folio,
                )
                querycdc.estatus_consulta_id = 4
                uow.commit()
                raise Exception("Error con consulta a círculo de credito")

            # reglas de validacion
            response_consult = _evaluate_consult(
                credit_data, querycdc.folio, command.curp, user.username
            )

            querycdc.estatus_consulta_id = int(response_consult["id_status"])
            querycdc.fallo_regla = response_consult["fallo_regla"]
            querycdc.folio_cdc_consulta = credit_data.encabezado.folio_consulta

            uow.commit()

            pdf_service = CDCPdfService()
            filename, result = pdf_service.save(querycdc.folio, credit_data)

            if config.get_email_active() and result:
                if mambu_user.tribus_usuario:
                    centre = mambu.centres.get(id=mambu_user.unidades_coordinador_0)
                    consejeros = [centre.consejero.email]
                    tribus_usuario = mambu_user.tribus_usuario
                else:
                    consejeros = []
                    tribus_usuario = []

                to_s = utils.get_recipients_email(
                    tribus_usuario=tribus_usuario,
                    consejeros=consejeros,
                )

                event = events.Email(  # type: ignore
                    attachments=[filename],
                    to=to_s,
                    cc=[],
                    subject="CDC {} {} {}".format(
                        credit_data.nombre.full_name,
                        querycdc.folio,
                        mambu_user.username,
                    ),
                    message="Esta consulta fue generada por {}".format(user.username),
                )
                bus.publish(event)
            else:  # pragma: no cover
                logger.info("Envio de correo desactivado. Usuario %s:", user.username)

            return {
                "id": response_consult["id_status"],
                "estatus": response_consult["status_respuesta"],
                "curp": command.curp,
                "folio": querycdc.folio,
                "timestamp_consulta": timestamp_consulta.strftime("%Y-%m-%d %H:%M:%S"),
                "fallo_regla": response_consult["fallo_regla"],
                "msg_success": "Consulta Realizada Exitosamente",
            }
        except Exception as ex:
            logger.exception("Error con consulta %s", str(ex))

            errors_list = (
                credit_data.error.errores.descripcion_error
                if credit_data.error is not None
                else ""
            )

            folio = querycdc.folio if "querycdc" in locals() else ""

            raise CdcError(
                id=5,
                estatus=config.ERROR,
                curp=command.curp,
                folio=folio,
                timestamp_consulta=timestamp_consulta.strftime("%Y-%m-%d %H:%M:%S"),
                fallo_regla=errors_list,
                msg_error="La Consulta Tiene Errores. Contacte a soporte",
            )  # pragma: no cover


def validate_consulta_cdc(
    command: commands.ValidateConsultaCDC,
    uow: unit_of_work.UnitOfWorkCdc,
    mambu: podemos_mambu.PodemosMambu,
    bus: bus.AbstractBus,
):  # pragma: no cover
    with uow:
        """"""


def _evaluate_consult(credit_data, folio, curp, username):
    response_consult = {}
    try:
        logger.info("inicia evaluacion integrante")
        response_evaluation = EvaluateRules(
            accounts=credit_data.cuentas,
            addresses=credit_data.domicilios,
            folio=folio,
            curp=curp,
            username=username,
        ).evaluation_accounts()
        response_consult = {
            "status_respuesta": response_evaluation["status_respuesta"],
            "id_status": response_evaluation["id_status"],
            "fallo_regla": response_evaluation["fallo_regla"],
        }
        return response_consult
    except Exception as e:  # pragma: no cover
        logger.error("Error al evaluar integrante %s", str(e))
        raise Exception("Error al evaluar integrante")


def get_person(
    query: queries.GetPerson,
    uow: unit_of_work.UnitOfWorkCdc,
) -> list:
    with uow:
        person = uow.persons.list()
        return [
            {
                "id": per.id,
                "nombre": per.nombre,
                "apellido_paterno": per.apellido_paterno,
                "apellido_materno": per.apellido_materno,
                "fecha_nacimiento": str(per.fecha_nacimiento),
                "curp": per.curp,
                "rfc": per.rfc,
                "nacionalidad": per.nacionalidad,
                "direccion": per.direccion,
                "colonia": per.colonia,
                "delegacion": per.delegacion,
                "ciudad": per.ciudad,
                "estado": per.estado,
                "codigo_postal": per.codigo_postal,
                "es_referida": per.es_referida,
            }
            for per in person
        ]


def get_consult_cdc(
    query: queries.GetConsultCDC,
    uow: unit_of_work.UnitOfWorkCdc,
) -> list:
    with uow:
        user = current_user()
        query.username = user.username
        query.periodo = config.PERIODO
        list_consult_cdc = uow.view_consult.search(query)
        return [
            {
                "folio": row[0],
                "timestamp_consulta": row[1].strftime("%Y-%m-%d"),
                "curp": row[2],
                "nombre_completo": "{} {} {} ".format(row[3], row[4], row[5]),
                "nombre": row[3],
                "apellido_paterno": row[4],
                "apellido_materno": row[5],
                "estatus_consulta_id": row[6],
                "grupo_id": row[7] if row[7] else 0,
            }
            for row in list_consult_cdc  # type: ignore
        ]


def notify_cdc_email(event: events.Email, smtp: smtp.SmtpEmail):
    logger.info(
        "Email information: to=%s, cc=%s, message=%s",
        str(event.to),
        str(event.cc),
        event.message,
    )

    smtp.send(
        to=event.to,
        cc=event.cc,
        subject=event.subject,
        message=event.message,
        attachments=event.attachments,
    )

    return True


def create_and_send_pdf(
    event: events.ValidConsultaCdc,
    bus: bus.AbstractBus,
    pdfservice: file_service.FileService = CDCPdfService(),
):
    credit_data = CDCResponse.from_response(
        response=event.xml_response, claves_permitidas=config.CLAVES_PERMITIDAS
    )

    pdf_service = pdfservice
    filename, result = pdf_service.save(event.cdc_folio, credit_data)

    if config.CDC_EMAIL_ACTIVE and result:
        consejeros = []
        tribus_usuario = []
        if event.consejero_email:
            consejeros.append(event.consejero_email)
        if event.tribus_usuario:
            tribus_usuario.extend(event.tribus_usuario)

        to_s = utils.get_recipients_email(
            tribus_usuario=tribus_usuario,
            consejeros=consejeros,
            gen_tribus=_gen_tribus_usuario_2,
        )

        email_event = events.Email(  # type: ignore
            attachments=[filename],
            to=to_s,
            cc=[],
            subject="CDC {} {} {}".format(
                credit_data.nombre.full_name,
                event.cdc_folio,
                event.username,
            ),
            message="Esta consulta fue generada por {}".format(event.username),
        )
        bus.publish(email_event)
    else:  # pragma: no cover
        logger.info("Envio de correo desactivado. Usuario %s:", event.username)

    return True


QUERY_HANDLERS = {
    queries.GetPerson: get_person,
    queries.GetConsultCDC: get_consult_cdc,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {
    commands.ADDPerson: add_person,
    commands.ValidateConsultaCDC: validate_consulta_cdc,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {
    events.Email: notify_cdc_email,
    events.ValidConsultaCdc: create_and_send_pdf,
}  # type: ignore
