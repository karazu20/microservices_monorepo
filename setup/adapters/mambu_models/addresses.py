from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields

from mambupy.api.vos import MambuAddress

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class Addresses(VOMambu):
    _model_rest = MambuAddress

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Addresses), mode, **kwargs)

    parent_key: str = field(
        metadata={"mambu_source": "parentKey", "read_only": False, "is_required": False}
    )
    line_1: str = field(
        metadata={"mambu_source": "line1", "read_only": False, "is_required": False}
    )
    line_2: str = field(
        metadata={"mambu_source": "line2", "read_only": False, "is_required": False}
    )
    city: str = field(
        metadata={"mambu_source": "city", "read_only": False, "is_required": False}
    )
    region: str = field(
        metadata={"mambu_source": "region", "read_only": False, "is_required": False}
    )
    postcode: str = field(
        metadata={"mambu_source": "postcode", "read_only": False, "is_required": False}
    )
    country: str = field(
        metadata={"mambu_source": "country", "read_only": False, "is_required": False}
    )
    index_in_list: int = field(
        metadata={"mambu_source": "indexInList", "read_only": False, "is_required": False}
    )
