from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields

from mambupy.api.vos import MambuUserRole

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class UserRoles(VOMambu):

    _model_rest = MambuUserRole

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(UserRoles), mode, **kwargs)

    id: str = field(
        metadata={"mambu_source": "id", "read_only": True, "is_required": False}
    )
