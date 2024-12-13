from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetRelease(Query):
    pass
