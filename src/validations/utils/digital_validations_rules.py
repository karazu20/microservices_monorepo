import locale
from datetime import datetime

from dateutil.relativedelta import relativedelta

from setup.adapters.podemos_mambu import PodemosMambu as mambu
from src.validations.config import DAYS  # type: ignore
from src.validations.utils.util import change_day_spanish  # type: ignore
from src.validations.utils.util import convert_value_to_data_type  # type: ignore
from src.validations.utils.util import extract_streetnumber  # type: ignore
from src.validations.utils.util import strip_accents  # type: ignore

locale.setlocale(locale.LC_TIME, "")


class DigitalValidationsRules(object):
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
        self.clients = clients
        self.group = group
        self.loan = loan
        self.quantity = quantity
        self.field_validations = field_validations
        if rule_data_validation:
            self.rule_data_validation = self.convert_rule_data_validation_to_data_type(
                rule_data_validation=rule_data_validation
            )
        self.validate_data = validate_data
        self.products = products
        self.type_validation = type_validation

    def convert_rule_data_validation_to_data_type(self, rule_data_validation) -> dict:
        for value in rule_data_validation:
            value.valor = convert_value_to_data_type(
                data_type=value.tipo_dato, value=value.valor
            )

        return rule_data_validation

    def street_address(self) -> dict:
        data_response = []
        status = True

        for value in self.clients:
            if (
                not value.addresses[0].line_1
                or value.addresses[0].line_1 == ""
                or "|" in str(value.addresses[0].line_1)
            ):
                data_response.append(
                    {
                        "message": (
                            "Calle y número invalidos. La dirección de la integrante"
                            " %s - (ID: %s), presenta errores en los campos: Calle y Número.\n"
                        )
                        % (value.full_name, value.id),
                        "field": "street_address",
                        "client_id": value.id,
                    }
                )
                status = False
                continue
            num_street = value.addresses[0].line_1
            try:
                extract_streetnumber(num_street, "numsimb")
            except AttributeError:
                import re

                if re.search(r" S[/]?N(?!\w)", num_street):
                    continue
                data_response.append(
                    {
                        "message": "Calle/Numero de %s (%s) en formato incorrecto (%s)\n"
                        % (
                            value.full_name,
                            value.id,
                            num_street,
                        ),
                        "field": "street_address",
                        "client_id": value.id,
                    }
                )
                status = False
            except Exception as ex:
                data_response.append(
                    {
                        "message": (
                            "Error desconocido validando calle/numero de la direccion de la "
                            "integrante %s (%s) (error: %s, favor de informar este mensaje completo a TI)\n"
                        )
                        % (value.full_name, value.id, repr(ex)),
                        "field": "street_address",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def colony_address(self) -> dict:
        data_response = []
        status = True

        for value in self.clients:
            if not value.addresses[0].line_2 or value.addresses[0].line_2 == "":
                data_response.append(
                    {
                        "message": (
                            "Colonia invalida. La dirección de la integrante %s - "
                            "(ID: %s), presenta un error en el campo: Colonia.\n"
                        )
                        % (value.full_name, value.id),
                        "field": "line_2",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def municipality_address(self) -> dict:
        data_response = []
        status = True

        municipalities = [value.valor for value in self.rule_data_validation]
        for value in self.clients:
            if value.addresses[0].city == "" or not value.addresses[0].city:
                data_response.append(
                    {
                        "message": (
                            "El Municipio es inválido. La dirección de la "
                            "integrante %s - (ID: %s), tiene un error en el campo Municipio. %s\n"
                        )
                        % (value.full_name, value.id, str(value.addresses[0].city)),
                        "field": "city",
                        "client_id": value.id,
                    }
                )
                status = False
                continue

            if value.addresses[0].city not in municipalities:
                data_response.append(
                    {
                        "message": (
                            "El Municipio es inválido. La dirección de la "
                            "integrante %s - (ID: %s), tiene un error en el campo Municipio. %s\n"
                        )
                        % (value.full_name, value.id, str(value.addresses[0].city)),
                        "field": "city",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def quote_validation_in_addresses_client(self) -> dict:
        data_response = []
        status = True
        for value in self.clients:
            if value.full_addresses:
                for key, value_dir in enumerate(value.full_addresses):
                    if '"' in value_dir or "'" in value_dir:
                        status = False
                        data_response.append(
                            {
                                "message": (
                                    "La dirección %s del cliente %s"
                                    " no puede contener comillas()."
                                    % (str(key), value.id)
                                ),
                                "field": "full_addresses",
                                "client_id": value.id,
                            }
                        )
            else:
                status = False
                data_response.append(
                    {
                        "message": (
                            "El cliente %s" " no tiene dirección registrada" % value.id
                        ),
                        "field": "full_addresses",
                        "client_id": value.id,
                    }
                )

        return {"status": status, "data_response": data_response}

    def calendar_validate(self) -> dict:
        try:
            if len(self.loan.installments) > 0 and self.loan.installments[0].due_date:
                return {"status": True, "data_response": []}
            else:
                return {
                    "status": False,
                    "data_response": [
                        {
                            "message": "La cuenta debe tener un calendario de pagos asignado",
                            "field": "installments",
                            "loan_id": self.loan.id,
                        }
                    ],
                }
        except Exception:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "La cuenta debe tener un calendario de pagos asignado",
                        "field": "installments",
                        "loan_id": self.loan.id,
                    }
                ],
            }

    def difference_of_days_in_day_meeting(self) -> dict:
        if not self.loan.dia_de_pago_loan_accounts:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El campo: Día de pago, es necesario. En el crédito: %s"
                        % (self.loan.id),
                        "field": "pay_day",
                        "loan_id": self.loan.id,
                    }
                ],
            }
        pay_day = self.loan.dia_de_pago_loan_accounts.upper()

        if not self.loan.fecha_de_la_primer_reunion_loan:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El campo: Fecha de la primera reunión es "
                            "necesario en el crédito %s" % (self.loan.id)
                        ),
                        "field": "meeting_date",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        meeting_date = self.loan.fecha_de_la_primer_reunion_loan

        try:
            meeting_date = (
                datetime.strptime(meeting_date, "%d/%m/%Y").strftime("%A").upper()
            )
        except ValueError:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "La fecha de primer reunión tiene un formato incorrecto,"
                            " formato correcto: dd/mm/AAAA del crédito: %s"
                        )
                        % (self.loan.id),
                        "field": "meeting_date",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        meeting_date = DAYS[meeting_date]

        try:
            pay_day = DAYS[pay_day]
        except KeyError:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El día %s, no puede ser elegido como fecha de primer reunión"
                        )
                        % pay_day,
                        "field": "pay_day",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        difference_of_days = abs(meeting_date - pay_day)
        if difference_of_days not in [2, 3]:
            return {"status": True, "data_response": []}

        return {
            "status": False,
            "data_response": [
                {
                    "message": (
                        "La diferencia entre el día de pago y "
                        "día de reunion, no puede ser mayor a 1 día. Del crédito: %s"
                        % self.loan.id
                    ),
                    "field": "pay_day",
                    "loan_id": self.loan.id,
                }
            ],
        }

    def gender(self) -> dict:
        data_response = []
        status = True

        for value in self.clients:
            if not value.gender:
                data_response.append(
                    {
                        "message": (
                            "La integrante: %s (ID: %s) no tiene género "
                            "asignado (Género Hombre o Mujer)\n"
                            % (value.full_name, value.id)
                        ),
                        "field": "gender",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def experience(self) -> dict:
        data_response = []
        status = True

        for value in self.clients:
            if value.experiencia >= 0:
                age = datetime.now() - value.birth_date
                max_experience = age.days / 365 - relativedelta(years=15).years
                if value.experiencia > max_experience:
                    data_response.append(
                        {
                            "message": (
                                "Los años de experiencia (%s) de %s - (ID: %s), no pueden ser mayor a: %s."
                                % (
                                    value.experiencia,
                                    value.full_name,
                                    value.id,
                                    max_experience,
                                )
                            ),
                            "field": "experiencia",
                            "client_id": value.id,
                        }
                    )
                    status = False

        return {"status": status, "data_response": data_response}

    def age_range(self) -> dict:
        data_response = []
        status = True

        for value in self.clients:
            if value.loan_cycle == 0 and value.group_loan_cycle == 0:
                today = datetime.now()
                birth_date = value.birth_date
                age = (
                    today.year
                    - birth_date.year
                    - ((today.month, today.day) < (birth_date.month, birth_date.day))
                )
                min_age, max_age = 18, 72
                if (age > max_age) or (age < min_age):
                    data_response.append(
                        {
                            "message": (
                                "El rango de edad de la integrante %s (ID: %s), tiene que estar: %s - %s años."
                                % (value.full_name, value.id, min_age, max_age)
                            ),
                            "field": "birth_date",
                            "client_id": value.id,
                        }
                    )
                    status = False

        return {"status": status, "data_response": data_response}

    def clients_in_group(self) -> dict:
        id_clients_loan = [value["integrante"] for value in self.loan.integrantes_loan]
        id_clients_group = [
            value.client.encoded_key for value in self.group.group_members
        ]
        data_response = []
        status = True

        not_in_ids_group = []
        for value in id_clients_loan:
            if value not in id_clients_group:
                client = mambu.clients.get(id=value)
                status = False
                data_response.append(
                    {
                        "message": "La cliente: %s - %s no esta en el grupo"
                        % (
                            client.full_name,
                            client.id,
                        ),
                        "client_id": client.id,
                        "group_id": self.group.id,
                        "field": "group",
                    }
                )
                not_in_ids_group.append(value)

        return {"status": status, "data_response": data_response}

    def same_clients_in_loan(self) -> dict:
        status = True
        data_response = []

        clientes = [v["integrante"] for v in self.loan.integrantes_loan]

        repetidos = set([c for c in clientes if clientes.count(c) > 1])

        if repetidos:
            status = False
            names = ""
            for value in repetidos:
                client = mambu.clients.get(id=value)
                names += " - %s (%s)" % (client.full_name, client.id)
            data_response.append(
                {
                    "message": "Hay integrantes duplicadas en la cuenta: %s" % (names),
                    "field": "loan",
                    "loan_id": self.loan.id,
                    "client_id": client.id,
                }
            )

        return {"status": status, "data_response": data_response}

    def group_meeting_day(self) -> dict:
        if not self.loan.account_holder.dia_de_reunion_groups:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El campo: Día de reunión es necesario en el grupo %s"
                        % (self.loan.account_holder.id),
                        "loan_id": self.loan.id,
                        "field": "meeting_day",
                    }
                ],
            }
        meeting_day_group = self.loan.account_holder.dia_de_reunion_groups.upper()

        if not self.loan.fecha_de_la_primer_reunion_loan:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El campo: Fecha de la primera reunión es necesario en el crédito %s"
                        % (self.loan.id),
                        "loan_id": self.loan.id,
                        "field": "meeting_date",
                    }
                ],
            }

        meeting_date = self.loan.fecha_de_la_primer_reunion_loan
        try:
            meeting_day_one = datetime.strptime(meeting_date, "%d/%m/%Y").strftime("%A")
        except ValueError:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "La fecha de primer reunión tiene un formato incorrecto,"
                            " formato correcto: dd/mm/AAAA del crédito: %s"
                        )
                        % (self.loan.id),
                        "loan_id": self.loan.id,
                        "field": "meeting_date",
                    }
                ],
            }

        meeting_day_one = str(
            strip_accents(meeting_day_one.encode().decode("utf-8")).upper()
        )
        find_day = change_day_spanish(meeting_day_one)

        if find_day:
            meeting_day_one = find_day

        if meeting_day_one == meeting_day_group:
            return {"status": True, "data_response": []}

        return {
            "status": False,
            "data_response": [
                {
                    "message": (
                        "El día de la primera reunión de la cuenta es (%s),"
                        " no coincide con el día de reunión del grupo (%s)."
                        % (meeting_day_one, meeting_day_group)
                    ),
                    "loan_id": self.loan.id,
                    "field": "meeting_date",
                }
            ],
        }
