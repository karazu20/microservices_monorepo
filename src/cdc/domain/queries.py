from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetPerson(Query):
    pass


@dataclass
class GetConsultCDC(Query):
    username: Optional[str] = field(metadata={"required": False}, default=None)
    periodo: Optional[int] = field(metadata={"required": False}, default=None)
    group_id: Optional[int] = field(metadata={"required": False}, default=None)
    folio: Optional[int] = field(metadata={"required": False}, default=None)
