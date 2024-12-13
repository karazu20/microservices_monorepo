from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetGrupo(Query):
    group_id: Optional[int] = field(metadata={"required": False}, default=None)
    username: Optional[str] = field(metadata={"required": False}, default=None)
