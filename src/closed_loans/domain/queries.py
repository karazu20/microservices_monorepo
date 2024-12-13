from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetClosedLoans(Query):
    group_id: Optional[str] = field(metadata={"required": True})
