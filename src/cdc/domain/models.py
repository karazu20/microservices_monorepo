from __future__ import annotations  # type: ignore

import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, List, Optional

from dateutil.relativedelta import relativedelta

from setup.domain import Model
from shared.cdc_utils import CDCResponse
from src.cdc import errors
from src.cdc.config import FOLIO_LEN_ID_EMPLEADO, FOLIO_LEN_TRIBU
from src.cdc.domain.evaluations_rules import EvaluateRules

logger = logging.getLogger(__name__)


@dataclass
class Grupo(Model):
    grupo_id: str = field(init=False)


@dataclass
class Person(Model):
    id: int = field(init=False)
    nombre: str = ""
    apellido_paterno: str = ""
    apellido_materno: str = ""
    fecha_nacimiento: Optional[date] = None  # type: ignore
    curp: str = ""
    rfc: str = ""
    nacionalidad: str = ""
    direccion: str = ""
    colonia: str = ""
    delegacion: str = ""
    ciudad: str = ""
    estado: str = ""
    codigo_postal: str = ""  # type: ignore
    es_referida: int = False
    grupo_id: int = field(init=False)
    _query_cdc: List[Any] = field(default_factory=list, init=False)
    _grupo: Grupo = field(default_factory=Grupo)

    def add_query_cdc(self, query_cdc: QueryCdc):
        self._query_cdc.append(query_cdc)


@dataclass
class QueryCdc(Model):
    id: int = field(init=False)
    archivo_xml: str = ""
    centro_comunitario: str = ""
    folio: str = ""
    persona_id: int = field(init=False)
    username: str = ""
    usuario_cdc: Optional[str] = None
    timestamp_consulta: Optional[datetime] = None  # type: ignore
    timestamp_aprobacion_consulta: Optional[datetime] = None  # type: ignore
    timestamp_aprobacion_tyc: Optional[datetime] = None  # type: ignore
    estatus_consulta_id: int = 0
    fallo_regla: str = ""
    nip: Optional[str] = ""
    folio_cdc_consulta: Optional[str] = ""
    tipo_consulta: str = ""
    created: Optional[datetime] = None  # type: ignore

    def generate_folio(self, user, folios) -> str:
        from datetime import date

        try:
            tribu = (
                user.tribus_usuario[0]["UnidadesCoordinador"]
                .rjust(FOLIO_LEN_TRIBU, "0")
                .replace("Tribu", "")
                .replace("-", "")
            )
        except Exception:
            tribu = "0000PP"
        num_empleado = str(user.id_empleado).rjust(FOLIO_LEN_ID_EMPLEADO, "P")

        folio = "00" + tribu + num_empleado + date.today().strftime("%y%m%d")
        folios = sorted(folios, key=lambda x: x.folio)
        if not folios:
            folio += "001"
        else:
            folio += str(int(folios[-1].folio[-3:]) + 1).rjust(3, "0")
        self.folio = folio
        self.archivo_xml = "{}.xml".format(self.folio)
        return folio


@dataclass
class QueryStatus:
    id: int = field(init=False)
    status: str = ""
    id_status: int = field(init=False)


# V2
@dataclass
class Usuario(Model):
    usuario_id: int = field(init=False)
    username: str = field(default="")


@dataclass
class CentroComunitario(Model):
    centro_comunitario_id: int = field(init=False)
    name: str = field(default="")


@dataclass
class Nip(Model):
    id: int = field(init=False)
    nip: str = field(default="")
    curp: str = field(default="")
    fecha: date = field(default=datetime.now().date())
    vigente: int = field(default=1)
    validado: int = field(default=0)
    num_consultas: int = field(default=0)


@dataclass
class StatusConsultaCdC(Model):
    id: int = field(init=False)
    id_status: int = field(init=False)
    status: str = ""


@dataclass
class DireccionProspecto(Model):
    calle: str = ""
    numero_exterior: str = ""
    numero_interior: str = ""
    colonia: str = ""
    ciudad: str = ""
    estado: str = ""
    pais: str = ""
    CP: str = ""


@dataclass
class Prospecto(Model):
    curp: str = ""
    nombre: str = ""
    segundo_nombre: str = ""
    apellido_paterno: str = ""
    apellido_materno: str = ""
    fecha_nacimiento: Optional[date] = None  # type: ignore
    nacionalidad: Optional[str] = ""
    telefono: str = ""
    _consultas: List[ConsultaCdc] = field(default_factory=list, init=False)
    _direcciones: List[DireccionProspecto] = field(default_factory=list, init=False)
    _consultaData: CDCResponse = field(default_factory=CDCResponse)

    def add_direccion(self, direccion: DireccionProspecto):
        if self._direcciones == [] or not self._direcciones[-1] == direccion:
            self._direcciones.append(direccion)

    def get_direcciones(self):
        return self._direcciones

    def add_consulta_prospecto(self, consulta: ConsultaCdc):
        self._consultas.append(consulta)

    def get_consultas(self):
        return self._consultas

    def _update_consulta(
        self,
        consulta: ConsultaCdc,
        folio_cdc: str,
        fallo: str,
        estatus: StatusConsultaCdC,
    ):
        if consulta not in self._consultas:
            raise errors.CdcDomainError(
                "Error la consulta que se intenta actualizar no existe."
            )
        consulta.cdc_folio = folio_cdc
        consulta.fallo_regla = fallo
        consulta._estatus = estatus

    def _check_past_due_accounts(self, consulta: ConsultaCdc):
        """
        Dont have overdue accounts with an overdue grater than $ 3,500 (MOP > 1) and
        with an age of 12 months from the date of opening

        When it returns False it means that its not within the rule for which the validation passes
        otherwise returns True.
        """
        er = EvaluateRules()
        result = False
        today = datetime.today()
        months = er.get_key(er.constant_past_due_account, "months")  # type: ignore
        today_subtraction_months = today - relativedelta(months=months)  # type: ignore
        amount = int(er.get_key(er.constant_past_due_account, "amount"))  # type: ignore
        is_revolving_account = er.get_key(  # type: ignore
            er.constant_is_revolving_account, "account_type"
        )
        for c in self._consultaData.cuentas:  # type: ignore
            if c.saldo_vencido is not None:
                past_due_balance = int(c.saldo_vencido)
                opening_date = datetime.strptime(c.fecha_apertura_cuenta, "%Y-%m-%d")
                if c.tipo_cuenta == is_revolving_account:
                    try:
                        opening_date = datetime.strptime(c.fecha_ultimo_pago, "%Y-%m-%d")
                    except TypeError:
                        logger.info(
                            "Rule check_past_due_accounts: \
                                is_revolving_account without DATE OF LAST PAYMENT, the OPENING DATE is taken"
                        )
                        opening_date = datetime.strptime(
                            c.fecha_apertura_cuenta, "%Y-%m-%d"
                        )
                    if (
                        past_due_balance > amount
                        and opening_date >= today_subtraction_months
                    ):
                        logger.info(
                            "CURP: %s FOLIO: %s Dont Pass Rule check_past_due_accounts ",
                            self.curp,
                            consulta.folio,
                        )
                        result = True
                        self.fallo = "Cuentas vencidas."
                        break
        return result

    def _check_broken_accounts(self, consulta: ConsultaCdc):
        """
        Dont have broken accounts, fraudulent, executive judgment, untraceable or
        cobranza of $1500 with an age of 12 months from the date of opening
        """
        er = EvaluateRules()
        result = False
        today = datetime.today()
        months = er.get_key(er.constant_past_due_account, "months")  # type: ignore
        today_subtraction_months = today - relativedelta(months=months)  # type: ignore
        amount = int(er.get_key(er.constant_past_due_account, "amount"))  # type: ignore
        is_revolving_account = er.get_key(  # type: ignore
            er.constant_is_revolving_account, "account_type"
        )
        prevention_keys = er.get_key(er.constant_broken_account, "prevention_keys")
        for c in self._consultaData.cuentas:  # type: ignore
            current_balance = int(c.saldo_actual)
            prevention_account = c.clave_prevencion
            opening_date = datetime.strptime(c.fecha_apertura_cuenta, "%Y-%m-%d")
            if c.tipo_cuenta == is_revolving_account:
                try:
                    opening_date = datetime.strptime(c.fecha_ultimo_pago, "%Y-%m-%d")
                except TypeError:
                    logger.info(
                        "Rule check_broken_accounts: \
                        is_revolving_account without DATE OF LAST PAYMENT, the OPENING DATE is taken"
                    )
                    opening_date = datetime.strptime(c.fecha_apertura_cuenta, "%Y-%m-%d")
            if (
                prevention_account in prevention_keys
                and current_balance >= amount
                and opening_date >= today_subtraction_months
            ):
                logger.info(
                    "La CURP: %s FOLIO: %s  Dont Pass Rule check_broken_accounts ",
                    self.curp,
                    consulta.folio,
                )
                result = True
                self.fallo = (
                    "Cuentas en quebranto, fraude, juicio ejecutivo, ilocalizables."
                )
                break
            else:
                result = False
        return result

    def _check_two_broken_accounts(self, consulta: ConsultaCdc):
        """
        Dont have two or more broken accounts, fraudulent, executive judgment, untraceable or
        cobranza. Regardless of amount and less than 12 months
        """
        er = EvaluateRules()
        result = False
        today = datetime.today()
        months = er.get_key(er.constant_past_due_account, "months")  # type: ignore
        today_subtraction_months = today - relativedelta(months=months)  # type: ignore
        prevention_keys = er.get_key(er.constant_two_broken_accounts, "prevention_keys")
        total = int(er.get_key(er.constant_two_broken_accounts, "total"))
        constant_accounts_prevention = 0
        for c in self._consultaData.cuentas:  # type: ignore
            opening_date = datetime.strptime(c.fecha_apertura_cuenta, "%Y-%m-%d")
            if (
                c.clave_prevencion in prevention_keys
                and opening_date >= today_subtraction_months
            ):
                constant_accounts_prevention = constant_accounts_prevention + 1
        if constant_accounts_prevention >= total:
            logger.info(
                "La CURP: %s FOLIO: %s Dont Pass Rule check_two_broken_accounts ",
                self.curp,
                consulta.folio,
            )
            result = True
            self.fallo = (
                "Dos cuentas o más en quebranto, fraude, juicio ejecutivo, ilocalizable."
            )
        return result

    def _check_fraudulent_accounts(self, consulta: ConsultaCdc):
        """
        In the "fraudulent" accounts, on "demand" or on "mora". Don't matter the amount and the period.
        solo se tomara en cuenta que exista en el reporte de circulo de credito
        """
        er = EvaluateRules()
        result = False
        prevention_keys = er.get_key(er.constant_is_fraudulent, "prevention_keys")
        for c in self._consultaData.cuentas:  # type: ignore
            if c.clave_prevencion in prevention_keys:
                logger.info(
                    "CURP: %s with FOLIO: %s Dont Pass Rule check_fraudulent_accounts ",
                    self.curp,
                    consulta.folio,
                )
                result = True
                self.fallo = "Cuenta fraudulenta,en demanda o en mora."
                break
            else:
                result = False
        return result

    def _check_three_addresses(self, consulta: ConsultaCdc):
        """Not having three different addresses in the last 6 months"""
        er = EvaluateRules()
        result = False
        today = datetime.today()
        months = er.get_key(er.constant_are_three_addresses, "months")  # type: ignore
        today_subtraction_months = today - relativedelta(months=months)  # type: ignore
        max_addresses = int(er.get_key(er.constant_are_three_addresses, "max_addresses"))
        aux_set_cps = set()
        if (
            self._consultaData.domicilios is None
            or len(self._consultaData.domicilios) < max_addresses
        ):
            result = False
        else:
            for d in self._consultaData.domicilios:
                try:
                    registration_date = datetime.strptime(
                        d.fecha_registro_domicilio, "%Y-%m-%d"
                    )
                except TypeError:
                    logger.info(
                        "Rule check_three_addresses: Account without ADDRESS REGISTRATION DATE becomes empty"
                    )
                    registration_date = None  # type: ignore
                if registration_date and registration_date >= today_subtraction_months:
                    aux_set_cps.add(d.cp)
        if len(aux_set_cps) >= max_addresses:
            logger.info(
                "CURP: %s FOLIO: %s Dont Pass Rule check_three_addresses ",
                self.curp,
                consulta.folio,
            )
            result = True
            self.fallo = "3 Domicilios en los ultimos 6 meses."
        return result

    def set_consulta_data(self, data: CDCResponse):
        self._consultaData = data

    def validate_consulta_cdc(self, consulta: ConsultaCdc):
        self.folio_cdc = consulta.cdc_folio
        self.fallo = ""
        self.estatus: StatusConsultaCdC = consulta._estatus
        if consulta not in self._consultas:
            raise errors.CdcDomainError(
                "Error la consulta que se intenta validar no existe."
            )
        if not self._consultaData.encabezado.folio_consulta:  # type: ignore
            raise errors.CdcDomainError("Error, el response no tiene folio de consulta.")
        if not self._consultaData.encabezado.folio_consulta == self.folio_cdc:  # type: ignore
            raise errors.CdcDomainError(
                "Error el folio de consulta del response debe coincidir con el folio de la consulta."
            )
        if len(self._consultaData.cuentas) == 0:  # type: ignore
            self.estatus = StatusConsultaCdC("PRE APROBADO")
        else:
            if self._consultaData.domicilios == []:
                raise errors.CdcDomainError(
                    "Error la prospecto no tiene domicilios para validar."
                )
            logger.info("Check Info about Folio %s ", (consulta.folio))
            if (
                self._check_past_due_accounts(consulta)
                or self._check_broken_accounts(consulta)
                or self._check_two_broken_accounts(consulta)
                or self._check_fraudulent_accounts(consulta)
                or self._check_three_addresses(consulta)
            ):
                logger.info(
                    "%s: FOLIO: %s DONT PASS Evaluation Accounts",
                    consulta._usuario.username,
                    consulta.folio,
                )
                self.estatus = StatusConsultaCdC("RECHAZADO")
            else:
                logger.info(
                    "%s: FOLIO: %s PASS Evaluation Accounts",
                    consulta._usuario.username,
                    consulta.folio,
                )
                self.estatus = StatusConsultaCdC("PRE APROBADO")

        self._update_consulta(consulta, self.folio_cdc, self.fallo, self.estatus)

        return self.estatus.status

    def generate_folio(
        self, consulta: ConsultaCdc, folios: List[str], num_empleado: str, tribu: str
    ) -> str:
        if consulta not in self._consultas:
            raise errors.CdcDomainError(
                "Error la consulta a la que intentas asignar folio, no existe dentro de las consultas de la Prospecto."
            )

        if not tribu:
            tribu = "0000PP"
            folios = [x for x in folios if x[:6] == "000000"]
        else:
            folios = [x for x in folios if x[2:5] == tribu]

        folio = "00" + tribu + num_empleado + date.today().strftime("%y%m%d")

        if not folios:
            folio += "001"
        else:
            last_folio = max(folios)
            folio_number = int(last_folio[-3:]) + 1
            folio += str(folio_number).rjust(3, "0")

        consulta.folio = folio
        self._update_consulta(
            consulta, consulta.cdc_folio, consulta.fallo_regla, consulta._estatus
        )

        return folio


@dataclass
class ConsultaCdc(Model):
    cliente_id: int = field(init=False)
    direccion_id: int = field(init=False)
    nip_id: int = field(init=False)
    status_consulta_id: int = field(init=False)
    usuario_id: int = field(init=False)
    centro_comunitario_id: int = field(init=False)
    cdc_folio: str = ""
    folio: str = ""
    consulta_timestamp: Optional[datetime] = None  # type: ignore
    consulta_apr_timestamp: Optional[datetime] = None  # type: ignore
    consulta_tyc_timestamp: Optional[datetime] = None  # type: ignore
    consulta_cdc_tipo: str = ""
    fallo_regla: str = ""
    es_referido: bool = False
    _prospecto: Prospecto = field(default_factory=Prospecto)
    _direccion: DireccionProspecto = field(default_factory=DireccionProspecto)
    _nip: Nip = field(default_factory=Nip)
    _estatus: StatusConsultaCdC = field(default_factory=StatusConsultaCdC)
    _usuario: Usuario = field(default_factory=Usuario)
    _centro_comunitario: CentroComunitario = field(default_factory=CentroComunitario)
