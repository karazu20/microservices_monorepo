# pylint: disable=attribute-defined-outside-init
from __future__ import annotations  # type: ignore

from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWorkVal
from src.validations import config
from src.validations.adapters import repositories, views


class UnitOfWorkValidations(SqlAlchemyUnitOfWorkVal):
    def __init__(
        self,
        session_factory_validations=config.DEFAULT_SESSION_FACTORY_VALIDATIONS,
        session_factory_digitalization=config.DEFAULT_SESSION_FACTORY_DIGITALIZATION,
    ):
        super().__init__(
            session_factory_validations,
            session_factory_digitalization,
        )

    def _enter(self):
        self.stage = repositories.StageRepository(self.session_validations)
        self.rule = repositories.RuleRepository(self.session_validations)
        self.rule_execution_status = repositories.RuleExecutionStatusRepository(
            self.session_validations
        )
        self.rule_execution = repositories.RuleExecutionRepository(
            self.session_validations
        )
        self.rule_exception_type = repositories.RuleExceptionTypeRepository(
            self.session_validations
        )
        self.rule_exception = repositories.RuleExceptionRepository(
            self.session_validations
        )
        self.role = repositories.RoleRepository(self.session_validations)
        self.role_rule = repositories.RoleRuleRepository(self.session_validations)
        self.field_validation = repositories.FieldValidationRepository(
            self.session_validations
        )
        self.custom_rule = repositories.CustomRuleRepository(self.session_validations)
        self.view_execution_rules = views.ExecutionRulesView(self.session_validations)
        self.view_custom_rule = views.CustomRuleMambuObjectsView(self.session_validations)
        self.validation_data_identifier = repositories.ValidationDataIdentifierRepository(
            self.session_validations
        )
        self.validation_data = repositories.ValidationDataRepository(
            self.session_validations
        )
        self.validation_rule_data = repositories.ValidationRuleDataRepository(
            self.session_validations
        )
        self.validation_cdc = repositories.ValidationConsultCdc(
            self.session_digitalization
        )
