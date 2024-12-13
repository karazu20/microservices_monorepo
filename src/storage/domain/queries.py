from dataclasses import field
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetUrl(Query):
    storage_id: Optional[str] = field(metadata={"required": True})


@dataclass
class GetDocumentType(Query):
    pass


@dataclass
class GetFileType(Query):
    pass
