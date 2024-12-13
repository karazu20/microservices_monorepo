import re

from setup.adapters.podemos_mambu import PodemosMambu as mambu
from src.validations.utils import digital_validations_rules  # type: ignore
from src.validations.utils.util import disbursement_date  # type: ignore
from src.validations.utils.util import extract_min_max_levels, find_client


class GeneralValidationsRules(digital_validations_rules.DigitalValidationsRules):
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
        digital_validations_rules.DigitalValidationsRules.__init__(
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

    def validate_tribe_in_group(self) -> dict:
        if self.loan.product_type.id in ["Insoluto-v2_bi"]:
            return {"status": True, "data_response": []}

        data_response = []
        status = True

        try:
            self.loan.assigned_user.id
        except Exception:
            status = False
            data_response.append(
                {
                    "loan_id": self.loan.id,
                    "field": "assigned_user",
                    "message": (
                        "El crédito: %s no tiene asignado coordinador" % self.loan.id
                    ),
                }
            )

        try:
            self.group.assigned_user.id
        except Exception:
            status = False
            data_response.append(
                {
                    "group_id": self.group.id,
                    "field": "assigned_user",
                    "message": (
                        "El grupo: %s no tiene asignado coordinador" % self.group.id
                    ),
                }
            )

        if not status:
            return {"status": status, "data_response": data_response}

        if self.group.assigned_user.id == self.loan.assigned_user.id:
            return {"status": True, "data_response": []}

        data_response.append(
            {
                "field": "assigned_user",
                "message": "El coordinador del grupo no coincide con el del crédito",
                "loan_id": self.loan.id,
                "group_id": self.group.id,
            }
        )

        return {
            "status": False,
            "data_response": data_response,
        }

    def is_new_group(self) -> bool:
        try:
            last_closed_loan = self.group.loans[-1]
        except Exception:
            last_closed_loan = None

        count_loan_actives = len(
            [
                value.id
                for value in self.group.loans
                if value.account_state in ["ACTIVE", "ACTIVE_IN_ARREARS"]
            ]
        )
        if count_loan_actives == 0 and not last_closed_loan:
            return True

        return False

    def mix_not_interest(self, count_installments) -> bool:
        if (
            self.loan.loan_name.upper() != "INTERES MIXTO INSOLUTO"
            or self.loan.account_state not in ["PENDING_APPROVAL", "ACTIVE"]
        ):
            return True

        return False

    def mix_interest(self, count_installments) -> bool:
        if (
            self.loan.account_state == "ACTIVE"
            and self.loan.original_account_key
            and 4 <= count_installments
            and count_installments <= 22
        ):
            return True

        return False

    def mix_group_interest(self, count_installments) -> bool:
        if self.is_new_group() and (
            (4 <= count_installments and count_installments <= 15)
            or (count_installments == 23)
        ):
            return True

        return False

    def mix_notkey_account(self, count_installments) -> bool:
        if not self.loan.original_account_key and count_installments in [11, 15, 23]:
            return True

        return False

    def mix_msg_interest(self) -> str:
        message = "La cuenta " + self.loan.id + " " + self.loan.loan_name
        semanas = ""

        if self.loan.account_state == "ACTIVE" and self.loan.original_account_key:
            message = message + " (RENEGOCIADA)"
            semanas = "4 a 22"
        elif self.is_new_group():
            semanas = "4 a 15"
        else:
            semanas = "11, 15 o 23"

        message = message + ", solo puede tener " + semanas + " semanas"

        return message

    def weeks_mix_interest(self) -> dict:
        count_installments = len(self.loan.installments)

        if (
            self.mix_not_interest(count_installments)
            or self.mix_interest(count_installments)
            or self.mix_group_interest(count_installments)
            or self.mix_notkey_account(count_installments)
        ):
            return {"status": True, "data_response": []}

        message = self.mix_msg_interest()

        return {
            "status": False,
            "data_response": [
                {"message": message, "field": "interes_mixto", "loan_id": self.loan.id}
            ],
        }

    def client_notes(self) -> dict:
        clients_loan_keys = [value["integrante"] for value in self.loan.integrantes_loan]
        clients_keys = [value.encoded_key for value in self.clients]
        data_response = []
        status = True

        for value in clients_loan_keys:
            if value not in clients_keys:
                status = False
                data_response.append(
                    {
                        "message": (
                            "La integrante %s no pertenece a este grupo." % value
                        ),
                        "field": "notes",
                        "client_id": value,
                    }
                )

        nummiembros = self.loan.num_de_miembros_loan_accounts
        totintegrantes = len(self.loan.integrantes_loan)

        if totintegrantes != nummiembros:
            status = False
            data_response.append(
                {
                    "message": (
                        "La cantidad de miembros indicada en la "
                        "cuenta, no es la misma que la cantidad de integrantes del crédito."
                    ),
                    "field": "notes",
                    "loan_id": self.loan.id,
                }
            )

        return {"status": status, "data_response": data_response}

    def authorization_op(self) -> dict:
        status_cuentas = [
            "ACTIVE",
            "ACTIVE_IN_ARREARS",
            "CLOSED",
            "CLOSED_RESCHEDULED",
            "CLOSED_WRITTEN_OFF",
        ]

        ciclo = len(
            [
                value
                for value in self.group.loans
                if value.account_state in status_cuentas
                and value.product_type.name
                not in [
                    "Credito Adicional",
                    "Credito Adicional MI",
                    "Credito Adicional Insoluto",
                ]
            ]
        )

        if ciclo == 0 and type(self.loan.generalidades_loan_accounts) not in [int, float]:
            return {
                "status": False,
                "data_response": [
                    {
                        "field": "generalidades_loan_accounts",
                        "message": (
                            "Un credito del ciclo 1 debe tener: "
                            "Generalidades de Autorización Operativa"
                        ),
                        "loan_id": self.loan.id,
                    }
                ],
            }
        elif type(self.loan.renovacion_loan_accounts) not in [int, float]:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "Un crédito en Renovación debe tener Renovación de Autorización Operativa",
                        "field": "renovacion_loan_accounts",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        if self.loan.autopmenu == self.loan.autlegmenu:
            return {
                "status": False,
                "data_response": [
                    {
                        "field": "autlegmenu",
                        "message": (
                            "El usuario que hizo la Autorización Operativa, "
                            "es el mismo que el que hizo la Autorizacion Legal."
                        ),
                        "loan_id": self.loan.id,
                    }
                ],
            }
        elif self.loan.autopmenu == self.loan.intgpomenu:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El usuario que hizo la Autorización Operativa"
                            ", es el mismo que el que hizo la Integración."
                        ),
                        "field": "intgpomenu",
                        "loan_id": self.loan.id,
                    }
                ],
            }
        elif self.loan.autlegmenu == self.loan.intgpomenu:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "El usuario que hizo la Autorización Legal, "
                            "es el mismo que el que hizo la Integración."
                        ),
                        "field": "intgpomenu",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        return {
            "status": True,
            "data_response": [],
        }

    def endorsement_exceed(self) -> dict:
        count_clients = len(self.loan.integrantes_loan)

        count_endorsement = sum(
            [
                value["endoso"] == True
                for value in self.loan.integrantes_loan
                if "endoso" in value
            ]
        )

        if (
            float(count_endorsement) / float(count_clients)
            > self.rule_data_validation[0].valor
        ):
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "Solo se puede endosar a la Tesorera un maximo del %s"
                            " de integrantes del grupo"
                            % str(self.rule_data_validation[0].valor)
                        ),
                        "field": "role",
                        "loan_id": self.loan.id,
                        "group_id": self.group.id,
                    }
                ],
            }

        roles_id = [
            (value_2.roles[0], value_2.client.encoded_key)
            for value_2 in self.group.group_members
            if value_2.roles
        ]

        try:
            lider = [value[1] for value in roles_id if value[0].role_name == "Lider"][0]
            tesorera = [
                value[1] for value in roles_id if value[0].role_name == "Tesorera"
            ][0]
        except Exception:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "Deben existir los roles de lider y tesorera en el grupo: %s"
                            % self.group.id
                        ),
                        "field": "role",
                        "loan_id": self.loan.id,
                        "group_id": self.group.id,
                    }
                ],
            }

        clients_in = []
        for val in self.loan.integrantes_loan:
            try:
                if val["endoso"]:
                    clients_in.append(val["integrante"])
            except KeyError:
                continue

        if tesorera not in clients_in and lider not in clients_in:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": (
                            "No se puede endosar a la Tesorera del grupo: %s"
                            ", los roles Tesorera y Lider necesitan endosar. Por "
                            "favor cambia los endosos o  los roles del grupo e in"
                            "téntalo de nuevo." % self.group.id
                        ),
                        "field": "role",
                        "loan_id": self.loan.id,
                        "group_id": self.group.id,
                    }
                ],
            }

        return {
            "status": True,
            "data_response": [],
        }

    def role_authorization(self) -> dict:
        status = True
        data_response = []

        user_types = {
            "user_cs": {
                "regex": r"(?i)()+consejer+(o|a)",
                "message": "El usuario que hizo la Autorizacion Operativa no es Consejero",
                "user": self.loan.autopmenu,
            },
            "user_ca": {
                "regex": r"(?i)()+(coordinador+(a?)|consejer+(o|a))\s+administrativ+(o|a?)",
                "message": "El usuario que hizo la Autorizacion Legal no es Coordinador Administrativo",
                "user": self.loan.autlegmenu,
            },
            "user_ce": {
                "regex": r"(?i)()+coordinador+(a?)\sde\s+emprendedoras",
                "message": "El usuario que hizo la integracion no tiene permisos de CE",
                "user": self.loan.intgpomenu,
            },
        }

        for key, value in user_types.items():
            try:
                credit_office_access = value["user"].access["creditOfficerAccess"]
            except Exception:
                credit_office_access = None

            if not value["user"]:
                status = False
                data_response.append(
                    {
                        "message": "La cuenta no tiene un usuario %s" % key,
                        "field": "user",
                        "user": None,
                    }
                )
                continue

            try:
                re.search(value["regex"], value["user"].title).group()  # type: ignore
            except AttributeError:
                if key == "user_ce" and credit_office_access:
                    continue
                status = False
                data_response.append(
                    {
                        "message": value["message"],
                        "field": "user",
                        "user": value["user"],
                    }
                )
            except TypeError:
                status = False
                data_response.append(
                    {
                        "message": value["message"]
                        + ". Escribiste '{}'".format(value["user"].title),
                        "field": "user",
                        "user": value["user"],
                    }
                )

        return {
            "status": status,
            "data_response": data_response,
        }

    def group_in_client(self) -> dict:
        status_loan = [
            "PENDING_APPROVAL",
            "APPROVED",
            "ACTIVE",
            "ACTIVE_IN_ARREARS",
            "CLOSED",
            "CLOSED_WRITTEN_OFF",
            "CLOSED_RESCHEDULED",
        ]

        products = ["INDIVIDUAL_MIXTO", "INTERES_MIXTO_INSOLUTO_BISEMANAL"]

        status = True
        data_response = []

        for value in self.clients:
            count_groups = len(value.groups)
            if count_groups == 0:
                continue

            loans_solidary = []
            for value_2 in value.groups:
                group_loans = [
                    l
                    for l in value_2.loans
                    if l.account_state in status_loan and l.loan_name not in products
                ]

                if len(group_loans) == 0:
                    continue

                loans_solidary.append(group_loans)

            if len(loans_solidary) <= 1 and count_groups > 0:
                continue

            data_response.append(
                {
                    "message": (
                        "La integrante %s - (ID: %s) pertenece a más de un grupo%s"
                        % (
                            value.full_name,
                            value.id,
                            " solidario"
                            " %s"
                            % (
                                [
                                    "%s %s %s"
                                    % (g.group_name, g.id, g.assigned_branch.id)
                                    for g in value.groups
                                ]
                            ),
                        )
                    ),
                    "field": "group",
                    "client_id": value.id,
                }
            )
            status = False

        return {
            "status": status,
            "data_response": data_response,
        }

    def renewal_num_member(self) -> dict:
        if not (
            self.loan.loan_name
            not in [
                "Credito Adicional",
                "Credito Adicional MI",
                "Credito Adicional Insoluto",
            ]
            and self.loan.account_holder.loan_cycle > 0
        ):
            return {
                "status": True,
                "data_response": [],
            }

        try:
            closed_loans = [
                l
                for l in self.loan.account_holder.loans
                if l.id != self.loan.id
                and l.loan_name
                not in [
                    "CREDITO_ADICIONAL",
                    "CREDITO_ADICIONAL_MI",
                    "CREDITO_ADICIONAL_INSOLUTO",
                ]
                and l.account_state
                in [
                    "ACTIVE",
                    "ACTIVE_IN_ARREARS",
                    "CLOSED",
                    "CLOSED_RESCHEDULED",
                    "CLOSED_WRITTEN_OFF",
                ]
                and (l.account_sub_state != "WITHDRAWN")
            ]
            closed_loans.sort(key=disbursement_date, reverse=True)
            last_closed_loan = closed_loans[0]
        except IndexError:
            return {
                "status": True,
                "data_response": [],
            }

        new_names = [
            integrante["integrante"] for integrante in self.loan.integrantes_loan
        ]

        old_names = [
            integrante["integrante"] for integrante in last_closed_loan.integrantes_loan
        ]

        not_in = []
        for n in old_names:
            if n not in new_names:
                not_in.append(n)

        if (float(len(not_in))) / float(len(old_names)) > (
            1 - self.rule_data_validation[0].valor
        ):
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "La cuenta renovada debe tener al menos el "
                        + str(int(self.rule_data_validation[0].valor * 100))
                        + "% de las mismas integrantes que la anterior",
                        "field": "integrantes",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        return {
            "status": True,
            "data_response": [],
        }

    def political_exposed(self) -> dict:
        data_response = []
        status = True

        for value in self.clients:
            if not value.people_could_political_exposed:
                continue

            if type(value.people_could_political_exposed) == str:
                continue

            status = False
            data_response.append(
                {
                    "message": (
                        "El campo 'Personas relacionadas que podrian ser politicamente expuestas' de %s"
                        " debe ser un texto" % str(value.people_could_political_exposed)
                    ),
                    "field": "people_could_political_exposed",
                    "client_id": value.id,
                }
            )

        return {"status": status, "data_response": data_response}

    def amnt_valid_client(self) -> dict:
        if self.loan.original_account_key or not self.loan.integrantes_loan:
            return {"status": True, "data_response": []}

        data_response = []
        status = True
        amount_max = extract_min_max_levels(
            data=self.rule_data_validation, value_to_extract="max"
        )
        amount_min = extract_min_max_levels(
            data=self.rule_data_validation, value_to_extract="min"
        )

        for value in self.loan.integrantes_loan:
            client = find_client(id=value["integrante"], clients=self.clients)
            if value["monto"] < 0:
                status = False
                data_response.append(
                    {
                        "message": "La cantidad para %s - (ID: %s) es invalida: $%.2f"
                        % (
                            client.full_name,
                            client.id,
                            value["monto"],
                        ),
                        "field": "amount",
                        "client_id": client.id,
                        "loan_id": self.loan.id,
                    }
                )
            elif value["monto"] > amount_max:
                status = False
                data_response.append(
                    {
                        "message": (
                            "Las integrantes no pueden recibir una cantidad tan grande (%s (%s): $%.2f; max: $%.2f)"
                            % (
                                client.full_name,
                                client.id,
                                value["monto"],
                                amount_max,
                            )
                        ),
                        "field": "amount",
                        "client_id": client.id,
                        "loan_id": self.loan.id,
                    }
                )
            elif (
                self.loan.loan_name
                not in [
                    "Credito Adicional",
                    "Credito Adicional MI",
                    "Credito Adicional Insoluto",
                ]
                and value["monto"] < amount_min
                and value["monto"] != 0
            ):
                status = False
                data_response.append(
                    {
                        "message": (
                            "Las integrantes no pueden recibir una cantidad tan chica (%s (%s): $%.2f; min: $%.2f)"
                            % (
                                client.full_name,
                                client.id,
                                value["monto"],
                                amount_min,
                            )
                        ),
                        "field": "amount",
                        "client_id": client.id,
                        "loan_id": self.loan.id,
                    }
                )

        return {"status": status, "data_response": data_response}

    def last_amnt_valid_client(self) -> dict:
        if not self.loan.integrantes_loan:
            return {"status": True, "data_response": []}

        data_response = []
        status = True
        amount_max = extract_min_max_levels(
            data=self.rule_data_validation, value_to_extract="max"
        )

        for value in self.loan.integrantes_loan:
            client = find_client(id=value["integrante"], clients=self.clients)
            if value["montoanterior"] < 0:
                status = False
                data_response.append(
                    {
                        "message": "La cantidad anterior para %s (%s) es invalida: $%.2f"
                        % (
                            client.full_name,
                            client.id,
                            value["montoanterior"],
                        ),
                        "field": "last_amount",
                        "client_id": client.id,
                        "loan_id": self.loan.id,
                    }
                )
            elif value["montoanterior"] > amount_max:
                status = False
                data_response.append(
                    {
                        "message": (
                            "Las integrantes no pudieron haber recibido una cantidad tan "
                            "grande en su ultimo credito (%s (%s): $%.2f; max: $%.2f)"
                            % (
                                client.full_name,
                                client.id,
                                value["montoanterior"],
                                amount_max,
                            )
                        ),
                        "field": "last_amount",
                        "client_id": client.id,
                        "loan_id": self.loan.id,
                    }
                )

        return {"status": status, "data_response": data_response}

    def total_amount_notes(self) -> dict:
        total_amount = float(
            sum([value["monto"] for value in self.loan.integrantes_loan])
        )
        loan_amount = float(self.loan.loan_amount)
        status = False
        data_response = []

        if self.loan.original_account_key and abs(loan_amount - total_amount) < 0.1:
            status = True
        elif loan_amount == total_amount:
            status = True
        else:
            data_response.append(
                {
                    "message": (
                        "Las cantidades asignadas a las integrantes, no suman el total"
                        " de la cuenta. (Total de la cuenta: $%.2f, suma: $%.2f)"
                    )
                    % (
                        self.loan.loan_amount,
                        total_amount,
                    ),
                    "field": "amount_notes",
                    "loan_id": self.loan.id,
                }
            )

        return {"status": status, "data_response": data_response}

    def num_members_in_notes(self) -> dict:
        status = True
        data_response = []

        if self.loan.loan_name not in [
            "Credito Adicional",
            "Credito Adicional MI",
            "Credito Adicional Insoluto",
        ]:
            if len(self.loan.account_holder.group_members) != len(
                self.loan.integrantes_loan
            ):
                data_response.append(
                    {
                        "message": (
                            "La cantidad de miembros del grupo %s, no es la misma que la cantidad de integrantes "
                            "en las notas del crédito (Cantidad de miembros: %d, Notas de crédito: %d)"
                        )
                        % (
                            self.loan.account_holder.id,
                            len(self.loan.account_holder.group_members),
                            len(self.loan.integrantes_loan),
                        ),
                        "group_id": self.loan.account_holder.id,
                        "loan_id": self.loan.id,
                        "field": "group_members",
                    }
                )
                status = False
        else:
            if len(self.loan.account_holder.group_members) < len(
                self.loan.integrantes_loan
            ):
                data_response.append(
                    {
                        "message": (
                            "La cantidad de miembros del grupo %s, es menor a la cantidad de integrantes en las no"
                            "tas del crédito (Cantidad de miembros: %d, Notas de crédito: %d)"
                        )
                        % (
                            self.loan.account_holder.id,
                            len(self.loan.account_holder.group_members),
                            len(self.loan.integrantes_loan),
                        ),
                        "group_id": self.loan.account_holder.id,
                        "loan_id": self.loan.id,
                        "field": "group_members",
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def cycle_valid(self) -> dict:
        not_accepted_products = [
            "Credito Adicional",
            "Credito Adicional MI",
            "Credito Adicional Insoluto",
        ]

        accepted_states = [
            "ACTIVE",
            "CLOSED",
            "ACTIVE_IN_ARREARS",
            "CLOSED_RESCHEDULED",
            "CLOSED_WRITTEN_OFF",
        ]

        if not self.loan.ciclo:
            return {
                "status": False,
                "data_response": [
                    {
                        "message": "El ciclo en el crédito: "
                        + self.loan.id
                        + " es requerido",
                        "field": "cycle",
                        "loan_id": self.loan.id,
                    }
                ],
            }

        if not self.is_new_group():
            return {"status": True, "data_response": []}

        products = [p.name for p in self.products if p.name not in not_accepted_products]
        status = True
        data_response = []

        loans_by_group = [
            l
            for l in self.loan.account_holder.loans
            if l.id != self.loan.id
            and l.loan_name not in not_accepted_products
            and l.account_state in accepted_states
            and (l.account_sub_state not in ["WITHDRAWN", "RESCHEDULED"])
        ]

        if self.loan.loan_name in products:
            additional_loan = 1
        else:
            additional_loan = 0

        loans_by_group = len(loans_by_group) + additional_loan  # type: ignore

        if self.loan.ciclo != loans_by_group:
            data_response.append(
                {
                    "message": (
                        "La información del campo: Ciclo personalizado, no "
                        "coincide con el número de cuentas validas cerradas,"
                        " (Crédito: %s, Ciclo: %s, Cuentas validas cerradas: %s)."
                        % (self.loan.id, self.loan.ciclo, loans_by_group)
                    ),
                    "loan_id": self.loan.id,
                    "field": "cycle",
                }
            )
            status = False

        return {"status": status, "data_response": data_response}

    def not_special_characters_in_name(self) -> dict:
        status = True
        data_response = []

        for value in self.clients:
            expresion = r"[^a-zA-Z \.ÑñáéíóúÁÉÍÓÚ]+"
            matches = re.search(expresion, value.full_name)

            if matches:
                data_response.append(
                    {
                        "message": (
                            "El nombre de la integrante %s (ID: %s), tiene caracteres inválidos"
                            % (value.full_name, value.id)
                        ),
                        "field": "full_name",
                        "client_id": value.id,
                    }
                )
                status = False

        return {"status": status, "data_response": data_response}

    def curp_validate(self) -> dict:
        status = True
        data_response = []
        for value in self.clients:
            find_curp = mambu.clients.search_by_curp(value.curp)
            if not find_curp:
                status = False
                data_response.append(
                    {
                        "message": "No existe integrante con este CURP: %s" % value.curp,
                        "field": "curp",
                        "client_id": value.id,
                    }
                )
            elif len(find_curp) > 1:
                status = False
                ids = [value.id for value in find_curp]
                data_response.append(
                    {
                        "message": (
                            "CURP existente La CURP: %s de la integrante %s, pertenece a %s ."
                            % (value.curp, value.full_name, ids)
                        ),
                        "field": "curp",
                        "client_id": value.id,
                    }
                )

        return {"status": status, "data_response": data_response}
