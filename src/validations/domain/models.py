from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
from typing import Set  # type: ignore

from setup.domain import Model


class BaseMambuTypes(Model):
    CREDITO = "CREDITO"
    INTEGRANTE = "INTEGRANTE"
    GRUPO = "GRUPO"
    CENTRO_COMUNITARIO = "CENTRO_COMUNITARIO"
    TRIBU = "TRIBU"


class BaseStageTypes(Model):
    PENDIENTE_DE_APROBACION = "PENDIENTE DE APROBACION"
    APROBADO = "APROBADO"
    DESEMBOLSO = "DESEMBOLSO"
    ACTIVO = "ACTIVO"
    CONSULTA_CDC = "CONSULTA CDC"


@dataclass
class Stage(BaseStageTypes):
    id: int = field(init=False)
    etapa: str = ""


@dataclass
class Rule(Model):
    id: int = field(init=False)
    regla: str = ""
    cantidad: int = 0


@dataclass
class RuleExecutionStatus(Model):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

    id: int = field(init=False)
    estatus: str = ""


@dataclass
class RuleExceptionType(BaseMambuTypes):
    id: int = field(init=False)
    tipo: str = ""


@dataclass
class RuleExecution(Model):
    id: int = field(init=False)
    etapa_id: int = field(init=False)
    regla_id: int = field(init=False)
    estatus_ejecucion_regla_id: int = field(init=False)
    _rule = set()  # type: Set[Rule]
    _stage = set()  # type: Set[Stage]
    _rule_execution_status = set()  # type: Set[RuleExecutionStatus]


@dataclass
class RuleException(Model):
    id: int = field(init=False)
    regla_id: int = field(init=False)
    tipo_excepcion_regla_id: int = field(init=False)
    id_mambu: str = ""
    _rule = set()  # type: Set[Rule]
    _rule_exception_type = set()  # type: Set[RuleExceptionType]


@dataclass
class RuleExecutionLog(Model):
    id: int = field(init=False)
    ejecucion_regla_id: int = field(init=False)
    id_mambu: str = ""
    _rule_execution = set()  # type: Set[RuleExecution]


@dataclass
class Role(Model):
    id: int = field(init=False)
    rol: str = ""


@dataclass
class RoleRule(Model):
    id: int = field(init=False)
    regla_id: int = field(init=False)
    rol_id: int = field(init=False)
    _role = set()  # type: Set[Role]
    _rule = set()  # type: Set[Rule]


@dataclass
class FieldValidation(Model):
    id: int = field(init=False)
    regla_id: int = field(init=False)
    campo: str = ""
    requerido: bool = False
    _rule = set()  # type: Set[Rule]


@dataclass
class CustomRuleSet(BaseMambuTypes):
    id: int = field(init=False)
    regla_id: int = field(init=False)
    id_object_mambu: str = ""
    tipo: str = ""
    etapa_id: int = field(init=False)
    estatus_ejecucion_regla_personalizada_id: int = field(init=False)
    _rule = set()  # type: Set[Rule]
    _stage = set()  # type: Set[Stage]
    _custom_rule_execution_status = set()  # type: Set[RuleExecutionStatus]


@dataclass
class ValidationDataIdentifier(Model):
    id: int = field(init=False)
    identificador: str = ""
    descripcion: str = ""


@dataclass
class ValidationData(Model):
    id: int = field(init=False)
    identificador_dato_validacion_id: int = field(init=False)
    llave: str = ""
    valor: str = ""
    tipo_dato: str = ""
    _validation_data_identifier = set()  # type: Set[ValidationDataIdentifier]


@dataclass
class ValidationRuleData(Model):
    id: int = field(init=False)
    regla_id: int = field(init=False)
    identificador_dato_validacion_id: int = field(init=False)
    _rule = set()  # type: Set[Rule]
    _validation_data_identifier = set()  # type: Set[ValidationDataIdentifier]


@dataclass
class InitClient(Model):
    id: str = ""
    curp: str = ""
    first_name: str = ""
    last_name: str = ""
    middle_name: str = ""
    birth_date: str = ""
    state: str = ""
