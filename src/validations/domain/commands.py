from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDStage(Command):
    etapa: str = field(metadata={"required": True})


@dataclass
class ADDRule(Command):
    regla: str = field(metadata={"required": True})
    cantidad: int = field(metadata={"required": False})


@dataclass
class ADDRuleExecutionStatus(Command):
    estatus: str = field(metadata={"required": True})


@dataclass
class ADDRuleExceptionType(Command):
    tipo: str = field(metadata={"required": True})


@dataclass
class ADDRuleExecution(Command):
    etapa_id: int = field(metadata={"required": True})
    regla_id: int = field(metadata={"required": True})
    estatus_ejecucion_regla_id: int = field(metadata={"required": True})


@dataclass
class ADDRuleException(Command):
    regla_id: int = field(metadata={"required": True})
    tipo_excepcion_regla_id: int = field(metadata={"required": True})
    id_mambu: str = field(metadata={"required": True})


@dataclass
class ADDRole(Command):
    rol: str = field(metadata={"required": True})


@dataclass
class ADDRoleRule(Command):
    regla_id: int = field(metadata={"required": True})
    rol_id: int = field(metadata={"required": True})


@dataclass
class ADDFieldValidation(Command):
    regla_id: int = field(metadata={"required": True})
    campo: str = field(metadata={"required": True})
    requerido: bool = field(metadata={"required": False})


@dataclass
class ADDCustomRule(Command):
    regla_id: int = field(metadata={"required": True})
    id_object_mambu: str = field(metadata={"required": True})
    tipo: str = field(metadata={"required": True})
    etapa_id: int = field(metadata={"required": True})
    estatus_ejecucion_regla_id: int = field(metadata={"required": True})


@dataclass
class ADDExcValidation(Command):
    id_mambu: str = field(metadata={"required": True})
    etapa: str = field(metadata={"required": True})
    tipo: str = field(metadata={"required": True})


@dataclass
class ADDValidationDataIdentifier(Command):
    identificador: str = field(metadata={"required": True})
    descripcion: str = field(metadata={"required": True})


@dataclass
class ADDValidationData(Command):
    identificador_dato_validacion_id: int = field(metadata={"required": True})
    llave: Optional[str] = field(metadata={"required": False})
    valor: str = field(metadata={"required": True})
    tipo_dato: str = field(metadata={"required": True})


@dataclass
class ADDValidationRuleData(Command):
    regla_id: int = field(metadata={"required": True})
    identificador_dato_validacion_id: int = field(metadata={"required": True})


@dataclass
class ADDExcValidationCDC(Command):
    id: Optional[str] = field(metadata={"required": False})
    id_mambu: Optional[str] = field(metadata={"required": False})
    etapa: Optional[str] = field(metadata={"required": False})
    tipo: Optional[str] = field(metadata={"required": False})
    curp: str = field(metadata={"required": True})
    first_name: str = field(metadata={"required": True})
    last_name: str = field(metadata={"required": True})
    middle_name: str = field(metadata={"required": False})
    birth_date: str = field(metadata={"required": True})
    state: Optional[str] = field(metadata={"required": False})
    numero: Optional[str] = field(metadata={"required": False})
