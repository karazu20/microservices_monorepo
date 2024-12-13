from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime

from mambupy.api.vos import MambuComment

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class Comments(VOMambu):
    _model_rest = MambuComment

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Comments), mode, **kwargs)

    owner_key: str = field(
        metadata={"mambu_source": "ownerKey", "read_only": True, "is_required": False}
    )
    owner_type: str = field(
        metadata={"mambu_source": "ownerType", "read_only": True, "is_required": False}
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
    text: str = field(
        metadata={"mambu_source": "text", "read_only": False, "is_required": True}
    )
    user_key: str = field(
        metadata={"mambu_source": "userKey", "read_only": True, "is_required": False}
    )
