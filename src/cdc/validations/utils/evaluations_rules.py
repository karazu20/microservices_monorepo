"""
Validations Rules
"""
import logging
from datetime import datetime
from typing import List

import yaml
from dateutil.relativedelta import relativedelta

from shared.cdc_utils import CuentaData, DomicilioData
from src.cdc import config

logger = logging.getLogger(__name__)


class EvaluateRules:
    def __init__(
        self,
        accounts: List[CuentaData] = [],
        addresses: List[DomicilioData] = [],
        folio=None,
        curp=None,
        username=None,
    ):
        self.accounts: List[CuentaData] = accounts
        self.addresses: List[DomicilioData] = addresses
        # Info para el logger
        self.folio = folio
        self.curp = curp
        self.username = username
        self.response_dict = {
            "status_respuesta": config.PENDIENTE,
            "id_status": "",
            "fallo_regla": "",
        }
        self.constant_past_due_account = self.get_rule_info(
            rule_name="is_past_due_account"
        )
        self.constant_broken_account = self.get_rule_info(rule_name="is_broken_account")
        self.constant_two_broken_accounts = self.get_rule_info(
            rule_name="are_two_broken_accounts"
        )
        self.constant_are_three_addresses = self.get_rule_info(
            rule_name="are_three_addresses"
        )
        self.constant_is_revolving_account = self.get_rule_info(
            rule_name="is_revolving_account"
        )
        self.constant_is_fraudulent = self.get_rule_info(rule_name="is_fraudulent")

    def get_rule_info(
        self,
        default_path="docs/validations/BRMS.yml",
        rule_name="",
    ):
        try:
            with open(default_path) as file_yml:
                file_yml = file_yml.read()  # type: ignore
            config_rules = yaml.full_load(file_yml)
            return config_rules["config_rules"][rule_name]
        except Exception as ex:  # pragma: no cover
            logger.error("ERROR: Rules not loaded: %s %s", rule_name, repr(ex))
            return "Error: {}".format(ex)

    def evaluation_accounts(self):
        """
        Evaluate respond with a dictionary contaning the name of the consulted person, the invoice generated,
        the consulted cupr and the status of the response.
        If the prospect dont pass the rules of verification, the status will be NO PASS. Otherwise
        the status will be PASS. Finally if the credit circle (cdc) throws an ERROR scheme,
        the status will be FAIL.

        Response: diccionario {Nombre:,Folio:,CURP:,STATUS_RESPUESTA:, FalloRegla:}
        """
        if len(self.accounts) == 0:
            self.response_dict["status_respuesta"] = config.PRE_APROBADO
            self.response_dict["id_status"] = "2"
        else:
            logger.info("Check Info about Folio %s ", (self.folio))
            if (
                self.check_past_due_accounts(self.accounts)
                or self.check_broken_accounts(self.accounts)
                or self.check_two_broken_accounts(self.accounts)
                or self.check_fraudulent_accounts(self.accounts)
                or self.check_three_addresses(self.addresses)
            ) == True:
                logger.info(
                    "%s: FOLIO: %s DONT PASS Evaluation Accounts",
                    self.username,
                    self.folio,
                )
                self.response_dict[
                    "status_respuesta"
                ] = config.RECHAZADO  # pragma: no cover
                self.response_dict["id_status"] = 3  # type: ignore # pragma: no cover
            else:
                logger.info(
                    "%s: FOLIO: %s PASS Evaluation Accounts",
                    self.username,
                    self.folio,
                )
                self.response_dict["status_respuesta"] = config.PRE_APROBADO
                self.response_dict["id_status"] = 2  # type: ignore

        return self.response_dict

    def check_past_due_accounts(self, accounts: List[CuentaData]):
        """
        Dont have overdue accounts with an overdue grater than $ 3,500 (MOP > 1) and
        with an age of 12 months from the date of opening

        When it returns False it means that its not within the rule for which the validation passes
        otherwise returns True.
        """
        result = False
        today = datetime.today()
        months = self.get_key(self.constant_past_due_account, "months")
        today_subtraction_months = today - relativedelta(months=months)
        amount = int(self.get_key(self.constant_past_due_account, "amount"))
        is_revolving_account = self.get_key(
            self.constant_is_revolving_account, "account_type"
        )
        for c in accounts:
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
                            self.folio,
                        )
                        result = True
                        self.response_dict[
                            "fallo_regla"
                        ] = "Cuentas vencidas"  # pragma: no cover
                        break
        return result

    def check_broken_accounts(self, accounts: List[CuentaData]):
        """
        Dont have broken accounts, fraudulent, executive judgment, untraceable or
        cobranza of $1500 with an age of 12 months from the date of opening
        """
        result = False
        today = datetime.today()
        months = self.get_key(self.constant_broken_account, "months")
        prevention_keys = self.get_key(self.constant_broken_account, "prevention_keys")
        amount = int(self.get_key(self.constant_broken_account, "amount"))
        is_revolving_account = self.get_key(
            self.constant_is_revolving_account, "account_type"
        )
        today_subtraction_months = today - relativedelta(months=months)
        for c in accounts:
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
                    self.folio,
                )
                result = True
                self.response_dict[
                    "fallo_regla"
                ] = "Cuentas en quebranto, fraude, juicio ejecutivo, ilocalizables"  # pragma: no cover
                break
            else:
                result = False
        return result

    def check_two_broken_accounts(self, accounts: List[CuentaData]):
        """
        Dont have two or more broken accounts, fraudulent, executive judgment, untraceable or
        cobranza. Regardless of amount and less than 12 months
        """
        result = False
        today = datetime.today()
        months = int(self.get_key(self.constant_two_broken_accounts, "months"))
        prevention_keys = self.get_key(
            self.constant_two_broken_accounts, "prevention_keys"
        )
        total = int(self.get_key(self.constant_two_broken_accounts, "total"))
        today_subtraction_months = today - relativedelta(months=months)
        constant_accounts_prevention = 0
        for c in accounts:
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
                self.folio,
            )
            result = True
            self.response_dict[
                "fallo_regla"
            ] = "Dos cuentas o más en quebranto, fraude, juicio ejecutivo, ilocalizable"  # pragma: no cover
        return result

    def check_fraudulent_accounts(self, accounts: List[CuentaData]):
        """
        In the "fraudulent" accounts, on "demand" or on "mora". Don't matter the amount and the period.
        solo se tomara en cuenta que exista en el reporte de circulo de credito
        """
        result = False
        prevention_keys = self.get_key(self.constant_is_fraudulent, "prevention_keys")
        for c in accounts:
            if c.clave_prevencion in prevention_keys:
                logger.info(
                    "CURP: %s with FOLIO: %s Dont Pass Rule check_fraudulent_accounts ",
                    self.curp,
                    self.folio,
                )
                result = True
                self.response_dict[
                    "fallo_regla"
                ] = "Cuenta fraudulenta,en demanda o en mora"  # pragma: no cover
                break
            else:
                result = False
        return result

    def check_three_addresses(self, addresses: List[DomicilioData]):
        """Not having three different addresses in the last 6 months"""
        result = False
        today = datetime.today()
        months = int(self.get_key(self.constant_are_three_addresses, "months"))
        max_addresses = int(
            self.get_key(self.constant_are_three_addresses, "max_addresses")
        )
        today_subtraction_months = today - relativedelta(months=months)
        aux_set_cps = set()
        if addresses is None or len(addresses) < max_addresses:
            result = False
        else:
            for d in addresses:
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
                self.folio,
            )
            result = True
            self.response_dict[
                "fallo_regla"
            ] = "3 Domicilios en los ultimos 6 meses"  # pragma: no cover
        return result

    def get_key(self, dict_t, keyName):
        for key, value in dict_t.items():
            if key == keyName:
                return value
        return "key doesn't exist"
