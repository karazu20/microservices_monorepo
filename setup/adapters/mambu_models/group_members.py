from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING

from mambupy.api.vos import MambuGroupMember

from setup.adapters.mambu_models.model import Mode, VOMambu

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Clients, GroupRoles


@dataclass(repr=False)
class GroupMembers(VOMambu):
    _model_rest = MambuGroupMember

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(GroupMembers), mode, **kwargs)

    client_key: str = field(
        metadata={"mambu_source": "clientKey", "read_only": False, "is_required": False}
    )
    roles: list[GroupRoles] = field(
        metadata={
            "mambu_source": "roles",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "GroupRoles",
        }
    )

    client: Clients = field(
        metadata={
            "mambu_source": "client",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Clients",
        }
    )
