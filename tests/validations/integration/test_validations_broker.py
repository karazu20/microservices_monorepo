import pytest

from fakes.adapters import FakeBus, FakeCache, FakeUnitOfWork
from setup import inject
from src.validations.domain.commands import (
    ADDCustomRule,
    ADDFieldValidation,
    ADDRole,
    ADDRoleRule,
    ADDRule,
    ADDRuleException,
    ADDRuleExceptionType,
    ADDRuleExecution,
    ADDRuleExecutionStatus,
    ADDStage,
)
from src.validations.domain.queries import (
    GetCustomRuleSet,
    GetFieldValidation,
    GetRole,
    GetRoleRule,
    GetRule,
    GetRuleException,
    GetRuleExceptionType,
    GetRuleExecution,
    GetRuleExecutionStatus,
    GetStage,
)
from src.validations.services_layer import handlers


@pytest.fixture
def broker():
    broker = inject.start_broker(
        handlers=handlers,
        orm=None,
        uow=FakeUnitOfWork(),
        bus=FakeBus(),
        cache=FakeCache(),
    )
    yield broker


def test_stage(broker):
    stage = ADDStage(etapa="APROBADO")
    broker.handle(stage)
    get_stage = GetStage()
    stages = broker.handle(get_stage)

    assert len(stages) == 1


def test_rule_execution_status(broker):
    rule_status = ADDRuleExecutionStatus(estatus="INACTIVO")
    broker.handle(rule_status)
    get_rule_status = GetRuleExecutionStatus()
    rules_status = broker.handle(get_rule_status)

    assert len(rules_status) == 1


def test_rule_exception_type(broker):
    rule_exception = ADDRuleExceptionType(tipo="INTEGRANTE")
    broker.handle(rule_exception)
    get_rule_exception_type = GetRuleExceptionType()
    rules_exception = broker.handle(get_rule_exception_type)

    assert len(rules_exception) == 1


def test_rule(broker):
    rule = ADDRule(regla="VALIDA_CURP", cantidad=2)
    broker.handle(rule)
    get_rule = GetRule()
    rules = broker.handle(get_rule)

    assert len(rules) == 1


def test_rule_execution(broker):
    rule_execution = ADDRuleExecution(1, 2, 3)
    broker.handle(rule_execution)
    get_rule_execution = GetRuleExecution("ACTIVO", "APROBADO")
    rules_exc = broker.handle(get_rule_execution)

    assert len(rules_exc) == 1


def test_rule_exception(broker):
    rule_exception = ADDRuleException(1, 2, "12345")
    broker.handle(rule_exception)

    get_rule_exception = GetRuleException()
    rules_exc = broker.handle(get_rule_exception)

    assert len(rules_exc) == 1


def test_role(broker):
    role = ADDRole("admin")
    broker.handle(role)

    get_role = GetRole()
    rol = broker.handle(get_role)

    assert len(rol) == 1


def test_role_rule(broker):
    role_rule = ADDRoleRule(1, 2)
    broker.handle(role_rule)

    get_role_rule = GetRoleRule()
    rol_rule = broker.handle(get_role_rule)

    assert len(rol_rule) == 1


def test_field_validation(broker):
    field_validation = ADDFieldValidation(1, "parentesco_referencia_2", 0)
    broker.handle(field_validation)

    get_field_validation = GetFieldValidation()
    field_validation_list = broker.handle(get_field_validation)

    assert len(field_validation_list) == 1


def test_custom_rule(broker):
    custom_rule = ADDCustomRule(
        regla_id=1,
        id_object_mambu="12345",
        tipo="CREDITO",
        etapa_id=2,
        estatus_ejecucion_regla_id=3,
    )

    broker.handle(custom_rule)

    get_custom_rule = GetCustomRuleSet()
    custom_rule_set = broker.handle(get_custom_rule)

    assert len(custom_rule_set) == 1
