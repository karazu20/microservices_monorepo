from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields

from mambupy.api.vos import MambuGroupRole

from setup.adapters.mambu_models.model import Mode, VOMambu


@dataclass(repr=False)
class GroupRoles(VOMambu):
    _model_rest = MambuGroupRole

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(GroupRoles), mode, **kwargs)

    group_role_name_key: str = field(
        metadata={
            "mambu_source": "groupRoleNameKey",
            "read_only": False,
            "is_required": False,
        }
    )
    role_name: str = field(
        metadata={"mambu_source": "roleName", "read_only": False, "is_required": False}
    )
    role_name_id: str = field(
        metadata={"mambu_source": "roleNameId", "read_only": False, "is_required": False}
    )
