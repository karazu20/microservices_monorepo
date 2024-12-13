from setup.adapters.data import SQLRepository
from src.cdc.domain.models import Person, QueryCdc
from src.validations.domain.models import (
    CustomRuleSet,
    FieldValidation,
    Role,
    RoleRule,
    Rule,
    RuleException,
    RuleExceptionType,
    RuleExecution,
    RuleExecutionStatus,
    Stage,
    ValidationData,
    ValidationDataIdentifier,
    ValidationRuleData,
)


class StageRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Stage)  # type: ignore
        self.stage = Stage

    def _get(self, stage) -> Stage:
        return self.session.query(Stage).filter_by(etapa=stage).first()


class RuleRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Rule)  # type: ignore
        self.rule = Rule


class RuleExecutionStatusRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, RuleExecutionStatus)  # type: ignore
        self.rule_execution_status = RuleExecutionStatus


class RuleExceptionTypeRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, RuleExceptionType)  # type: ignore
        self.rule_exception_type = RuleExceptionType


class RuleExecutionRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, RuleExecution)  # type: ignore
        self.rule_execution = RuleExecution

    def list(self, status=None, stage=None):
        if not status:
            status = RuleExecutionStatus.ACTIVO

        query = (
            self.session.query(
                RuleExecution.id, Rule.regla, RuleExecutionStatus.estatus, Stage.etapa
            )
            .join(Rule, Rule.id == RuleExecution.regla_id)
            .join(Stage, Stage.id == RuleExecution.etapa_id)
            .join(
                RuleExecutionStatus,
                RuleExecutionStatus.id == RuleExecution.estatus_ejecucion_regla_id,
            )
            .filter(RuleExecutionStatus.estatus == status)
        )

        if stage:
            query = query.filter(Stage.etapa == stage)

        return query.all()


class RuleExceptionRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, RuleException)  # type: ignore
        self.rule_exception = RuleException

    def list(self, id_mambu=None):
        query = (
            self.session.query(
                RuleException.id,
                RuleException.id_mambu,
                Rule.regla,
                RuleExceptionType.tipo,
                Rule.id,
            )
            .join(
                Rule,
                RuleException.regla_id == Rule.id,
            )
            .join(
                RuleExceptionType,
                RuleException.tipo_excepcion_regla_id == RuleExceptionType.id,
            )
        )

        if id_mambu:
            query = query.filter(RuleException.id_mambu == id_mambu)

        return query.all()


class RoleRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Role)  # type: ignore
        self.role = Role


class RoleRuleRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, RoleRule)  # type: ignore
        self.role_rule = RoleRule


class FieldValidationRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, FieldValidation)  # type: ignore
        self.field_validation = FieldValidation

    def _get_field_validation_rules(self, rule_id):
        return (
            self.session.query(FieldValidation)
            .filter(FieldValidation.regla_id == rule_id)
            .all()
        )


class CustomRuleRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, CustomRuleSet)  # type: ignore
        self.custom_rule = CustomRuleSet


class ValidationDataIdentifierRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, ValidationDataIdentifier)  # type: ignore
        self.validation_data_identifier = ValidationDataIdentifier


class ValidationDataRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, ValidationData)  # type: ignore
        self.validation_data = ValidationData


class ValidationRuleDataRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, ValidationRuleData)  # type: ignore
        self.validation_rule_data = ValidationRuleData

    def _get_field_validation_rule_data(self, rule_id):
        return (
            self.session.query(ValidationData)
            .join(
                ValidationDataIdentifier,
                ValidationDataIdentifier.id
                == ValidationData.identificador_dato_validacion_id,
            )
            .join(
                ValidationRuleData,
                ValidationRuleData.identificador_dato_validacion_id
                == ValidationDataIdentifier.id,
            )
            .join(Rule, ValidationRuleData.regla_id == Rule.id)
            .filter(Rule.id == rule_id)
            .all()
        )


class ValidationConsultCdc(SQLRepository):
    def __init__(self, session):
        super().__init__(session, QueryCdc)  # type: ignore
        self.query_cdc = QueryCdc

    def _get_consult(self, curp, fecha_inicial, today):

        return (
            self.session.query(QueryCdc)
            .join(Person, Person.id == QueryCdc.persona_id)
            .filter(Person.curp == curp)
            .filter(QueryCdc.timestamp_consulta.between(fecha_inicial, today))  # type: ignore
            .order_by(QueryCdc.id.desc())  # type: ignore
            .first()
        )
