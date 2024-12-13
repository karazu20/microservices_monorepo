from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetStage(Query):
    pass


@dataclass
class GetRule(Query):
    pass


@dataclass
class GetRuleExecutionStatus(Query):
    pass


@dataclass
class GetRuleExceptionType(Query):
    pass


@dataclass
class GetRuleExecution(Query):
    estatus: Optional[str] = field(metadata={"required": False}, default=None)
    etapa: Optional[str] = field(metadata={"required": False}, default=None)


@dataclass
class GetRuleException(Query):
    id_mambu: Optional[str] = field(metadata={"required": False}, default=None)


@dataclass
class GetRole(Query):
    pass


@dataclass
class GetRoleRule(Query):
    pass


@dataclass
class GetCustomRuleSet(Query):
    id: Optional[int] = field(metadata={"required": False}, default=None)


@dataclass
class GetFieldValidation(Query):
    pass


@dataclass
class GetExecutionRules(Query):
    id_mambu: str = field(metadata={"required": True})
    etapa: str = field(metadata={"required": True})
    estatus: str = field(metadata={"required": True})
