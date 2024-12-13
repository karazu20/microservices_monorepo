from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING

from mambupy.api.mambucentre import MambuCentre
from mambupy.orm.schema_mambu import Centre as ORMCentre

from setup.adapters.mambu_models.model import EntityMambu, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Addresses, Comments, Users


@dataclass(repr=False)
class Centres(EntityMambu):

    _model_rest = MambuCentre
    _model_orm = ORMCentre

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Centres), mode, **kwargs)

    name: str = field(
        metadata={"mambu_source": "name", "read_only": False, "is_required": False}
    )
    state: str = field(
        metadata={"mambu_source": "state", "read_only": False, "is_required": False}
    )
    notes: str = field(
        metadata={"mambu_source": "notes", "read_only": False, "is_required": False}
    )
    assigned_branch_key: str = field(
        metadata={
            "mambu_source": "assignedBranchKey",
            "read_only": False,
            "is_required": False,
        }
    )

    addresses: list[Addresses] = field(
        metadata={
            "mambu_source": "addresses",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "Addresses",
        }
    )
    comments: list[Comments] = field(
        metadata={
            "mambu_source": "_comments",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "lazy_from_method": "get_comments",
            "model": "Comments",
        }
    )

    consejero: Users = field(
        metadata={
            "mambu_source": "consejero",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_customfields_centre/consejero",
            "model": "Users",
        }
    )
