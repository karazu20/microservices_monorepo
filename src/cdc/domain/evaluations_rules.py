"""
Validations Rules
"""
import logging

import yaml

logger = logging.getLogger(__name__)


class EvaluateRules:
    def __init__(self):
        with open("src/cdc/confs/config_evaluations_rules.yml") as file_yml:
            file_yml = file_yml.read()  # type: ignore
        config_rules = yaml.full_load(file_yml)
        self.constant_past_due_account = config_rules["config_rules"][
            "is_past_due_account"
        ]
        self.constant_broken_account = config_rules["config_rules"]["is_broken_account"]
        self.constant_two_broken_accounts = config_rules["config_rules"][
            "are_two_broken_accounts"
        ]
        self.constant_are_three_addresses = config_rules["config_rules"][
            "are_three_addresses"
        ]
        self.constant_is_revolving_account = config_rules["config_rules"][
            "is_revolving_account"
        ]
        self.constant_is_fraudulent = config_rules["config_rules"]["is_fraudulent"]

    def ret_rules(self):
        return [
            self.constant_past_due_account,
            self.constant_broken_account,
            self.constant_two_broken_accounts,
            self.constant_are_three_addresses,
            self.constant_is_revolving_account,
            self.constant_is_fraudulent,
        ]

    def get_key(self, dict_t, keyName):
        return dict_t.get(keyName, "key doesn't exist")
