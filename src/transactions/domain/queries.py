from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetTransactions(Query):
    loan_id: Optional[str] = field(metadata={"required": True})


@dataclass
class GetInstallments(Query):
    loan_id: Optional[str] = field(metadata={"required": True})
