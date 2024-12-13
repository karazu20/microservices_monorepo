from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetLoanComments(Query):
    loan_id: str = field(metadata={"required": True})


@dataclass
class GetGroupComments(Query):
    group_id: str = field(metadata={"required": True})


@dataclass
class GetClientComments(Query):
    client_id: str = field(metadata={"required": True})
