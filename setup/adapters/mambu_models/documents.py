from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime

from mambupy.api.vos import MambuDocument

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class Documents(VOMambu):
    _model_rest = MambuDocument

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Documents), mode, **kwargs)

    id: str = field(
        metadata={"mambu_source": "id", "read_only": True, "is_required": False}
    )

    creation_date: datetime = field(
        metadata={
            "mambu_source": "creationDate",
            "read_only": True,
            "is_required": False,
        }
    )
    last_modified_date: datetime = field(
        metadata={
            "mambu_source": "lastModifiedDate",
            "read_only": True,
            "is_required": False,
        }
    )

    file_name: str = field(
        metadata={"mambu_source": "fileName", "read_only": False, "is_required": False}
    )
    file_size: int = field(
        metadata={"mambu_source": "fileSize", "read_only": False, "is_required": False}
    )
    location: str = field(
        metadata={"mambu_source": "location", "read_only": False, "is_required": False}
    )
    name: str = field(
        metadata={"mambu_source": "name", "read_only": False, "is_required": False}
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    owner_key: str = field(
        metadata={"mambu_source": "ownerKey", "read_only": False, "is_required": False}
    )
    owner_type: str = field(
        metadata={"mambu_source": "ownerType", "read_only": False, "is_required": False}
    )
    type_document: str = field(
        metadata={"mambu_source": "type", "read_only": False, "is_required": False}
    )
