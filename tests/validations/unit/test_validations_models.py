from src.validations.domain.models import (
    CustomRuleSet,
    FieldValidation,
    Role,
    RoleRule,
    Rule,
    RuleException,
    RuleExceptionType,
    RuleExecution,
    RuleExecutionLog,
    RuleExecutionStatus,
    Stage,
    ValidationData,
    ValidationDataIdentifier,
    ValidationRuleData,
)


def test_stage():
    model = Stage("APROBADO")
    assert model.id is None
    assert model.etapa == "APROBADO"


def test_rule():
    model = Rule("ReglaCURP", 2)
    assert model.id is None
    assert model.regla == "ReglaCURP"
    assert model.cantidad == 2


def test_rule_execution_status():
    model = RuleExecutionStatus("ACTIVO")
    assert model.id is None
    assert model.estatus == "ACTIVO"


def test_rule_execution():
    model = RuleExecution()
    assert model.id is None
    assert model.etapa_id is None
    assert model.regla_id is None
    assert model.estatus_ejecucion_regla_id is None


def test_rule_exception():
    model = RuleException("123456")
    assert model.id is None
    assert model.regla_id is None
    assert model.tipo_excepcion_regla_id is None
    assert model.id_mambu == "123456"


def test_rule_execution_log():
    model = RuleExecutionLog("654321")
    assert model.id is None
    assert model.ejecucion_regla_id is None
    assert model.id_mambu == "654321"


def test_rule():
    model = Role("admin")
    assert model.id is None
    assert model.rol == "admin"


def test_role_rule():
    model = RoleRule()
    assert model.id is None
    assert model.rol_id is None
    assert model.regla_id is None


def test_rule_exception_type():
    model = RuleExceptionType("INTEGRANTE")
    assert model.id is None
    assert model.tipo == "INTEGRANTE"


def test_rule_exception_type():
    model = FieldValidation("parentesco_referencia_2", 1)
    assert model.id is None
    assert model.regla_id is None
    assert model.campo == "parentesco_referencia_2"
    assert model.requerido == 1


def test_custom_rule():
    id_object_mambu = "12345"
    tipo = "GRUPO"

    model = CustomRuleSet(id_object_mambu=id_object_mambu, tipo=tipo)

    assert model.id_object_mambu is id_object_mambu
    assert model.tipo is tipo
    assert model.id is None
    assert model.regla_id is None
    assert model.etapa_id is None
    assert model.estatus_ejecucion_regla_personalizada_id is None


def test_validation_data_identifier():
    model = ValidationDataIdentifier("data_curp", "prueba")
    assert model.id is None
    assert model.identificador == "data_curp"
    assert model.descripcion == "prueba"


def test_validation_data():
    model = ValidationData("prueba_key", "prueba", "str")
    assert model.id is None
    assert model.identificador_dato_validacion_id is None
    assert model.llave == "prueba_key"
    assert model.valor == "prueba"
    assert model.tipo_dato == "str"


def test_validation_rule_data():
    model = ValidationRuleData()
    assert model.id is None
    assert model.regla_id is None
    assert model.identificador_dato_validacion_id is None
