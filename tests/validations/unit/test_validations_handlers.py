from fakes.adapters import FakeUnitOfWork
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
    ADDValidationData,
    ADDValidationDataIdentifier,
    ADDValidationRuleData,
)
from src.validations.services_layer import handlers


def test_add_stage():
    uow = FakeUnitOfWork()
    model = ADDStage(etapa="APROBADO")
    handlers.add_stage(model, uow)
    assert uow.committed


def test_add_rule():
    uow = FakeUnitOfWork()
    model = ADDRule(regla="LoanClientesRepetidos", cantidad=2)
    handlers.add_rule(model, uow)
    assert uow.committed


def test_add_rule_execution_status():
    uow = FakeUnitOfWork()
    model = ADDRuleExecutionStatus(estatus="ACTIVO")
    handlers.add_rule_execution_status(model, uow)
    assert uow.committed


def test_add_rule_exception_type():
    uow = FakeUnitOfWork()
    model = ADDRuleExceptionType(tipo="INTEGRANTE")
    handlers.add_rule_exception_type(model, uow)
    assert uow.committed


def test_rule_execution():
    uow = FakeUnitOfWork()
    model = ADDRuleExecution(1, 2, 3)
    handlers.add_rule_execution(model, uow)
    assert uow.committed


def test_rule_exception():
    uow = FakeUnitOfWork()
    model = ADDRuleException(1, 2, "12345")
    handlers.add_rule_exception(model, uow)
    assert uow.committed


def test_role():
    uow = FakeUnitOfWork()
    model = ADDRole("admin")
    handlers.add_role(model, uow)
    assert uow.committed


def test_role_rule():
    uow = FakeUnitOfWork()
    model = ADDRoleRule(1, 2)
    handlers.add_role_rule(model, uow)
    assert uow.committed


def test_field_validation():
    uow = FakeUnitOfWork()
    model = ADDFieldValidation(1, "parentesco_referencia_2", 1)
    handlers.add_field_validation(model, uow)
    assert uow.committed


def test_add_custom_rule_set():
    uow = FakeUnitOfWork()
    model = ADDCustomRule(
        regla_id=1,
        id_object_mambu="12345",
        tipo="CREDITO",
        etapa_id=2,
        estatus_ejecucion_regla_id=3,
    )

    handlers.add_custom_rule_set(model, uow)
    assert uow.committed


def test_add_validation_data_identifier():
    uow = FakeUnitOfWork()
    model = ADDValidationDataIdentifier(
        identificador="prueba_curp",
        descripcion="Prueba",
    )

    handlers.add_validation_data_identifier(model, uow)
    assert uow.committed


def test_add_validation_data():
    uow = FakeUnitOfWork()
    model = ADDValidationData(
        identificador_dato_validacion_id=1,
        llave="Prueba_key",
        valor="Prueba",
        tipo_dato="str",
    )

    handlers.add_validation_data(model, uow)
    assert uow.committed


def test_add_validation_rule_data():
    uow = FakeUnitOfWork()
    model = ADDValidationRuleData(
        identificador_dato_validacion_id=1,
        regla_id=2,
    )

    handlers.add_validation_rule_data(model, uow)
    assert uow.committed
