from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetLoanStatus(Query):
    id_mambu: Optional[list] = field(metadata={"required": False}, default=None)
    estatus: Optional[list] = field(metadata={"required": False}, default=None)
