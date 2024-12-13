"""
Validations Rules
"""
import re
from datetime import datetime

from shared.errors import BaseErrorsTypes
from src.validations.domain.models import InitClient
from src.validations.utils import general_validations_rules  # type: ignore
from src.validations.utils.util import convert_value_to_data_type  # type: ignore
from src.validations.utils.util import extract_data_by_id  # type: ignore
from src.validations.utils.util import extract_data_from_document_mambu  # type: ignore
from src.validations.utils.util import strip_accents  # type: ignore
from src.validations.utils.util import valida_curp  # type: ignore
from src.validations.utils.util import validate_data_rfc  # type: ignore


class ValidationsRules(general_validations_rules.GeneralValidationsRules):
    def __init__(
        self,
        type_validation="CDC",
        clients=None,
        group=None,
        loan=None,
        quantity=None,
        field_validations=None,
        rule_data_validation=None,
        validate_data=None,
        products=None,
    ):
        general_validations_rules.GeneralValidationsRules.__init__(
            self,
            type_validation=type_validation,
            clients=clients,
            group=group,
            loan=loan,
            quantity=quantity,
            field_validations=field_validations,
            rule_data_validation=rule_data_validation,
            validate_data=validate_data,
            products=products,
        )

    def convert_rule_data_validation_to_data_type(self, rule_data_validation):
        for value in rule_data_validation:
            value.valor = convert_value_to_data_type(
                data_type=value.tipo_dato, value=value.valor
            )

        return rule_data_validation

    def validate_field(self, field, model) -> dict:

        value = getattr(model, field)
        if value:
            return {
                "status": True,
                "message": "",
            }
        else:
            return {
                "status": False,
                "message": " no tiene el campo: " + field,
            }

    def group_risk(self) -> dict:
        if self.group.riesgo_grupo in ["Alto"]:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El grupo tiene riesgo Alto",
                        "field": "riesgo_grupo",
                        "group_id": self.group.id,
                    }
                ],
            }

        return {
            "status": True,
            "data_response": [],
        }

    def len_custom_fields(self, data_to_validate, key=None) -> dict:
        missing_fields = []
        for value in self.field_validations:
            try:
                attribute = getattr(data_to_validate, value.campo)
                if not attribute:
                    missing_fields.append(value.campo)
            except AttributeError:
                missing_fields.append(value.campo)

        if missing_fields:
            response_text = "Campos faltantes "
            for value in missing_fields:
                response_text = (
                    response_text + "ID: " + data_to_validate.id + " " + str(value) + "\n"
                )

            return {
                "status": False,
                "message": response_text,
            }

        return {
            "status": True,
            "message": "",
        }

    def len_custom_fields_groups(self) -> dict:
        if self.group:
            return self.len_custom_fields(data_to_validate=self.group)

        return {
            "status": True,
            "message": "",
        }

    def len_custom_fields_client(self) -> dict:
        if self.clients:
            message = ""
            for client in self.clients:
                response = self.len_custom_fields(data_to_validate=client)
                if response["status"] == False:
                    message = message + "\n" + response["message"]

            if message:
                return {
                    "status": False,
                    "message": message,
                }

        return {
            "status": True,
            "message": "",
        }

    def len_custom_fields_loans(self) -> dict:
        if self.loan:
            return self.len_custom_fields(
                data_to_validate=self.loan, key="customFieldValues"
            )

        return {
            "status": True,
            "message": "",
        }

    def custom_field_empty(self, data_to_validate) -> dict:
        message = ""

        required_fields = extract_data_by_id(
            data_to_extract=self.field_validations,
            key="campo",
            if_check=True,
            key_validate="requerido",
        )

        for value in required_fields:
            try:
                attribute = getattr(data_to_validate, value)
                if not attribute:
                    message = message + " El campo está vacío: " + value + "\n"
            except AttributeError:
                message = message + " Campo Faltante: " + value + "\n"

        if message:
            return {
                "status": False,
                "message": message,
            }

        return {
            "status": True,
            "message": "",
        }

    def custom_field_empty_group(self) -> dict:
        if self.group:
            return self.custom_field_empty(data_to_validate=self.group)

        return {
            "status": True,
            "message": "",
        }

    def custom_field_empty_loan(self) -> dict:
        if self.loan:
            return self.custom_field_empty(data_to_validate=self.loan)

        return {
            "status": True,
            "message": "",
        }

    def custom_field_empty_client(self) -> dict:
        if self.clients:
            message = ""
            for value in self.clients:
                response = self.custom_field_empty(data_to_validate=value)
                if response["status"] == False:
                    message = message + "\n" + response["message"]

            if message:
                return {
                    "status": False,
                    "message": message,
                }

        return {
            "status": True,
            "message": "",
        }

    def group_roles(self) -> dict:
        roles = {"LIDER": "LIDER", "TESORERA": "TESORERA"}
        for value in self.group.group_members:
            try:
                response = self.validate_field(field="role_name", model=value.roles[0])
                if not response["status"]:
                    continue
                if value.roles[0].role_name.upper() in roles:
                    del roles[value.roles[0].role_name.upper()]
            except Exception:
                continue

        if roles:
            rol_key = [*roles.values()]
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El grupo: "
                        + self.group.id
                        + " no tiene el ROL de "
                        + str(rol_key),
                        "field": "rol",
                        "group_id": self.group.id,
                    }
                ],
            }

        return {
            "status": True,
            "data_response": [],
        }

    def branch_client(self) -> dict:
        status = True
        data_response = []
        if self.clients:
            for value in self.clients:
                response = self.validate_field(field="assigned_branch_key", model=value)
                if not response["status"]:
                    data_response.append(
                        {
                            "message": "La integrante: %s no tiene ningún centro comunitario asignado"
                            % value.id,
                            "field": "assigned_branch_key",
                            "client_id": value.id,
                        }
                    )
                    status = False

        return {
            "status": status,
            "data_response": data_response,
        }

    def no_user_assignment_ce(self) -> dict:
        data_response = []
        status = True
        if self.clients:
            for value in self.clients:
                response = self.validate_field(field="assigned_user_key", model=value)

                if response["status"]:
                    data_response.append(
                        {
                            "message": "La integrante: %s no debe tener coordinador asignado"
                            % value.id,
                            "field": "assigned_user_key",
                            "client_id": value.id,
                        }
                    )
                    status = False

        return {
            "status": status,
            "data_response": data_response,
        }

    def date_birth_client(self) -> dict:
        data_response = []
        status = True
        if self.clients:
            for value in self.clients:
                try:
                    value.birth_date.strftime("%y%m%d")
                except AttributeError:
                    data_response.append(
                        {
                            "message": "Falta fecha de cumpleaños en el cliente: %s"
                            % value.id,
                            "field": "birth_date",
                            "client_id": value.id,
                        }
                    )
                    status = False

        return {
            "status": status,
            "data_response": data_response,
        }

    def client_telephone(self) -> dict:
        data_response = []
        status = True
        if self.clients:
            for value in self.clients:
                response = self.validate_field(
                    field="home_phone",
                    model=value,
                )

                if response["status"]:
                    phone = re.sub(r"\W", "", str(value.home_phone))
                    if not phone.isdigit():
                        data_response.append(
                            {
                                "message": (
                                    "El teléfono de domicilio del cliente: %s"
                                    " deben ser dígitos" % value.id
                                ),
                                "field": "home_phone",
                                "client_id": value.id,
                            }
                        )
                        status = False
                    elif phone and len(phone) != self.quantity:
                        data_response.append(
                            {
                                "message": (
                                    "El teléfono de domicilio del cliente: %s"
                                    " debe contener al menos %s dígitos"
                                    % (value.id, str(self.quantity))
                                ),
                                "field": "home_phone",
                                "client_id": value.id,
                            }
                        )
                        status = False

        return {
            "status": status,
            "data_response": data_response,
        }

    def validate_curp_client(self) -> dict:
        data_response = []
        status = True
        for value in self.clients:
            curp = extract_data_from_document_mambu(
                data_to_extract=value.id_documents, document_type="CURP"
            )

            if not curp:
                data_response.append(
                    {
                        "message": "La integrante %s no tiene CURP registrado" % value.id,
                        "field": "curp",
                        "client_id": value.id,
                    }
                )
                status = False
                continue

            required_fields = extract_data_by_id(
                data_to_extract=self.field_validations,
                key="campo",
            )

            if curp in required_fields:
                continue

        return {
            "status": status,
            "data_response": data_response,
        }

    def validate_curp(self, validar=["NOMBRE", "FECHANACIMIENTO"]) -> dict:
        for value in self.clients:
            if self.type_validation == "PCP":
                client = InitClient(
                    curp=value.curp,
                    first_name=value.first_name,
                    last_name=value.last_name,
                    middle_name=value.last_name.split(" ")[1],
                    birth_date=value.birth_date.strftime("%Y-%m-%d"),
                )
                validate_curp_client = valida_curp(
                    client=client,
                    palabras_inconvenientes=self.rule_data_validation,
                    validar=validar,
                )
            else:
                validate_curp_client = valida_curp(
                    client=value,
                    palabras_inconvenientes=self.rule_data_validation,
                    validar=validar,
                )
        return {
            "status": validate_curp_client[0],
            "message": validate_curp_client[1],
            "type_error": BaseErrorsTypes.EDITAR,
        }

    def validate_rfc(self) -> dict:
        data_response = []
        status = True
        fields_to_validate = extract_data_by_id(
            data_to_extract=self.field_validations,
            key="campo",
        )
        for value in self.clients:
            if not value.id_documents:
                data_response.append(
                    {
                        "message": "La integrante %s no tiene CURP registrado" % value.id,
                        "field": "curp",
                        "client_id": value.id,
                    }
                )
                status = False
                continue

            curp = extract_data_from_document_mambu(
                data_to_extract=value.id_documents, document_type="CURP"
            )

            if not curp:
                data_response.append(
                    {
                        "message": "La integrante %s no tiene CURP registrado" % value.id,
                        "field": "curp",
                        "client_id": value.id,
                    }
                )
                status = False

            if not value.rfc:
                status = False
                data_response.append(
                    {
                        "message": "El RFC de la integrante %s esta vacío" % value.id,
                        "field": "rfc",
                        "client_id": value.id,
                    }
                )
                continue

            if curp in fields_to_validate:
                continue

            rfc_validate = validate_data_rfc(id=value.id, rfc=value.rfc, curp=curp)
            if not rfc_validate["status"]:
                status = False
                data_response.append(
                    {
                        "message": rfc_validate["message"],
                        "field": "rfc",
                        "client_id": value.id,
                    }
                )

        return {
            "status": status,
            "data_response": data_response,
        }

    def client_email(self) -> dict:
        status = True
        data_response = []
        if self.clients:
            fields_to_validate = extract_data_by_id(
                data_to_extract=self.field_validations,
                key="campo",
            )
            for value in self.clients:

                if not value.email_address:
                    continue

                if value.email_address in fields_to_validate:
                    continue

                regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
                matches = re.match(regex, str(value.email_address))
                if not matches:
                    status = False
                    data_response.append(
                        {
                            "message": "El email de la integrante: %s tiene formato incorrecto"
                            % value.id,
                            "field": "email_address",
                            "client_id": value.id,
                        }
                    )

        return {
            "status": status,
            "data_response": data_response,
        }

    def minimum_number_of_members_loan(self) -> dict:
        if self.is_new_group() and not (len(self.clients) >= self.quantity):
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El crédito: "
                        + self.loan.id
                        + " no cuenta con el mínimo número de miembros que es: "
                        + str(self.quantity)
                        + "\n",
                        "loan_id": self.loan.id,
                        "field": "minimo_numero_miembros",
                    }
                ],
            }

        return {
            "status": True,
            "data_response": [],
        }

    def validate_address_clients(self) -> dict:
        status = True
        data_response = []
        if self.clients:
            for value in self.clients:
                if not value.addresses:
                    status = False
                    data_response.append(
                        {
                            "message": "La integrante %s no tiene dirección" % value.id,
                            "field": "address",
                            "client_id": value.id,
                        }
                    )

        return {
            "status": status,
            "data_response": data_response,
        }

    def family_home_restrictions_loan(self) -> dict:
        if not self.loan.restricciones_fam_dom_dist:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El crédito: %s no cumple las"
                            " restricciones de familia, domicilio y/o distancia"
                            % self.loan.id
                        ),
                        "field": "restricciones_fam_dom_dist",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        return {"status": True, "data_response": []}

    def cycle_group_type(self) -> dict:
        group_cycle = re.match(
            r"^(\s*[C]?\s*[-]?\s*\d+)\s*-?\s*([A-Z]?\s*\w+)\s*$",
            self.group.ciclo_tipo_groups,
        )

        if not group_cycle or len(group_cycle.groups()) != 2:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El campo Ciclo-Tipo es incorrecto"
                            " en el grupo: %s" % self.group.id
                        ),
                        "field": "ciclo_tipo_groups",
                        "group_id": self.group.id,
                    }
                ],
            }

        cycle = self.loan.ciclo
        cycle_group = re.match(r"^[C\s\-]*(\d+)$", group_cycle.groups()[0]).groups()[  # type: ignore
            0
        ]
        if int(cycle_group) != int(cycle):
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El número de ciclo no coincide con la "
                            "información Ciclo-Tipo del grupo. Ciclo-Tipo: %s"
                            ". Ciclo del grupo: %s" % (cycle_group, str(cycle))
                        ),
                        "field": "ciclo_tipo_groups",
                        "group_id": self.group.id,
                    }
                ],
            }

        product_name = self.loan.product_type.name
        if "Credito Solidario" in product_name:
            product_name += " MI"
        type_product = "".join([c for c in product_name if c.isupper()])
        group_type = re.match(r"^[C]?\s*(\w+)$", group_cycle.groups()[1]).groups()[0]  # type: ignore

        if product_name not in [
            "Credito Adicional",
            "Credito Adicional MI",
            "Credito Adicional Insoluto",
        ] and not (group_type in type_product or group_type in type_product[:-2]):
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El tipo de crédito no coincide con "
                            "la informacion del Ciclo-Tipo del grupo %s"
                            " Producto: %s" % (self.group.id, product_name)
                        ),
                        "field": "ciclo_tipo_groups",
                        "group_id": self.group.id,
                    }
                ],
            }

        return {"status": True, "data_response": []}

    def black_list_client(self) -> dict:
        if self.clients:
            message = ""
            for value in self.clients:
                if value.state == "BLACKLISTED":
                    message = (
                        message
                        + "Esta persona "
                        + value.id
                        + " no esta autorizada para recibir créditos en Podemos Progresar\n"
                    )

            if message:
                return {
                    "status": False,
                    "type_error": BaseErrorsTypes.NO_EDITAR,
                    "message": message,
                }

        return {
            "status": True,
            "message": "",
        }

    def client_risk(self) -> dict:
        data_response = []
        status = True
        if self.clients:
            for value in self.clients:
                if value.riesgo_integrante in ["Alto"]:
                    status = False
                    data_response.append(
                        {
                            "message": ("La integrante %s tiene riesgo Alto" % value.id),
                            "field": "riesgo_integrante",
                            "client_id": value.id,
                        }
                    )

        return {
            "status": status,
            "data_response": data_response,
        }

    def product_member_number(self) -> dict:
        for value in self.rule_data_validation:
            if (value.llave == self.loan.product_type.id) and (
                len(self.clients) < value.valor
            ):
                return {
                    "status": False,
                    "data_response": [
                        {
                            "message": (
                                "La cantidad de miembros del credito: %s "
                                "no cubre el minimo necesario (%s)"
                                % (self.loan.id, str(value.valor))
                            ),
                            "field": "product_type",
                            "loan_id": self.loan.id,
                        }
                    ],
                }

        return {
            "status": True,
            "data_response": [],
        }

    def product_validate(self) -> dict:
        if self.loan.product_type.state == "ACTIVE":
            return {"status": True, "data_response": []}

        return {
            "status": False,
            "data_response": [
                {
                    "message": (
                        "El crédito: %s no tiene un producto de crédito activo"
                        % self.loan.id
                    ),
                    "field": "product_type",
                    "loan_id": self.loan.id,
                }
            ],
        }

    def client_address_cp(self) -> dict:
        data_response = []
        status = True
        for value in self.clients:
            try:
                if len(str(value.addresses[0].postcode)) != 5:
                    data_response.append(
                        {
                            "message": (
                                "El código postal del cliente: %s es incorrecto"
                                % value.id
                            ),
                            "field": "postcode",
                            "client_id": value.id,
                        }
                    )
                    status = False
            except Exception:
                data_response.append(
                    {
                        "message": "El cliente %s no tiene código postal" % value.id,
                        "field": "postcode",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def client_address_state(self) -> dict:
        states = [value.valor for value in self.rule_data_validation]
        data_response = []
        status = True

        for value in self.clients:
            try:
                state_client = str(
                    strip_accents(value.addresses[0].region).strip().upper()
                )
                if state_client not in states:
                    data_response.append(
                        {
                            "message": (
                                "El estado (dirección) del cliente: %s es incorrecto"
                                % value.id
                            ),
                            "field": "region",
                            "client_id": value.id,
                        }
                    )
                    status = False
            except Exception:
                data_response.append(
                    {
                        "message": (
                            "El cliente %s no tiene estado (dirección) registrado"
                            % value.id
                        ),
                        "field": "region",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def validate_consult_cdc(self) -> dict:
        status = True
        message = ""
        if self.validate_data:
            message = ""
            status = False
            message = "Lo sentimos la información de esta emprendedora ya fue consultada."
        return {
            "status": status,
            "message": message,
            "type_error": BaseErrorsTypes.NO_EDITAR,
        }

    def first_meeting_date(self) -> dict:
        first_meet_date = self.loan.fecha_de_la_primer_reunion_loan
        today = datetime.now()
        message = ""
        status = True

        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                first_meet_date = datetime.strptime(first_meet_date, fmt)
                if today > first_meet_date:
                    status = False
                    message = (
                        "La primera reunión aún no ha comenzado. Fecha de la primera reunión: "
                        + str(first_meet_date)
                    )
                break
            except ValueError:
                continue
            except Exception:
                status = False
                message = "Fecha de la primer reunión es incorrecta: " + str(
                    first_meet_date
                )
                break
        else:
            status = False
            message = (
                "La fecha de primer reunión tiene un formato incorrecto. Formato correcto dd/mm/AAAA: (Ej. "
                + str(first_meet_date)
                + ")"
            )

        return {
            "status": status,
            "message": message,
        }

    def validate_status_pending_approval(self) -> dict:
        if self.loan.account_state == "PENDING_APPROVAL" or (
            self.loan.account_state == "ACTIVE" and self.loan.account_holder_key
        ):
            return {"status": True, "message": ""}

        return {
            "status": False,
            "message": "La cuenta: "
            + self.loan.id
            + " no esta en Pendiente de Aprobación",
        }

    def verify_coordinator_exists(self) -> dict:
        try:
            if self.group.assigned_user.encoded_key:
                return {"status": True, "message": ""}
        except Exception:
            return {
                "status": False,
                "message": "El grupo "
                + self.group.group_name
                + " - (ID: "
                + self.group.id
                + "), no tiene coordinador asignado.",
            }

        return {
            "status": False,
            "message": "El grupo "
            + self.group.group_name
            + " - (ID: "
            + self.group.id
            + "), no tiene coordinador asignado.",
        }

    def verify_center_exists(self) -> dict:
        try:
            if self.group.assigned_branch.encoded_key:
                return {"status": True, "message": ""}
        except Exception:
            return {
                "status": False,
                "message": "El grupo "
                + self.group.group_name
                + " - (ID: "
                + self.group.id
                + "), no tiene unidad ni centro asignado. "
                + "Por favor asigna una unidad y un centro al grupo.",
            }

        return {
            "status": False,
            "message": "El grupo "
            + self.group.group_name
            + " - (ID: "
            + self.group.id
            + "), no tiene unidad ni centro asignado. "
            + "Por favor asigna una unidad y un centro al grupo.",
        }

    def member_number_custom_field_in_loan(self) -> dict:
        try:
            nummiembros = int(self.loan.num_de_miembros_loan_accounts)
        except ValueError:
            return {
                "status": False,
                "message": "La cantidad de miembros indicada en la cuenta es inválida.",
            }
        if nummiembros == 0:
            return {
                "status": False,
                "message": "La cantidad de miembros indicada en la cuenta es inválida.",
            }
        if len(self.clients) != nummiembros:
            return {
                "status": False,
                "message": "La cantidad de miembros indicada en la cuenta es inválida.",
            }
        return {"status": True, "message": ""}

    def quote_validation_in_addresses_group(self) -> dict:
        message = ""
        if self.group.full_addresses:
            for key, value in enumerate(self.group.full_addresses):
                if '"' in value or "'" in value:
                    message = (
                        message
                        + "La dirección "
                        + str(key)
                        + " del grupo "
                        + self.group.id
                        + " no puede contener comillas("
                        ").\n"
                    )
        else:
            return {
                "status": False,
                "message": "El grupo " + self.group.id + " no tiene dirección registrada",
            }

        if message:
            return {
                "status": False,
                "message": message,
            }

        return {"status": True, "message": ""}
