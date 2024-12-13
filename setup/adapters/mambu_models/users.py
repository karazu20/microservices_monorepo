from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import TYPE_CHECKING

from mambupy.api.mambuuser import MambuUser
from mambupy.orm.schema_mambu import User as ORMUser

from setup.adapters.mambu_models.model import EntityMambu, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Branches, Comments, UserRoles


@dataclass(repr=False)
class Users(EntityMambu):

    _model_rest = MambuUser
    _model_orm = ORMUser

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Users), mode, **kwargs)

    last_logged_in_date: datetime = field(
        metadata={
            "mambu_source": "lastLoggedInDate",
            "read_only": False,
            "is_required": False,
        }
    )
    access: dict = field(
        metadata={"mambu_source": "access", "read_only": False, "is_required": False}
    )
    username: str = field(
        metadata={"mambu_source": "username", "read_only": False, "is_required": False}
    )
    email: str = field(
        metadata={"mambu_source": "email", "read_only": False, "is_required": False}
    )
    title: str = field(
        metadata={"mambu_source": "title", "read_only": False, "is_required": False}
    )
    first_name: str = field(
        metadata={"mambu_source": "firstName", "read_only": False, "is_required": False}
    )
    last_name: str = field(
        metadata={"mambu_source": "lastName", "read_only": False, "is_required": False}
    )
    mobile_phone: str = field(
        metadata={"mambu_source": "mobilePhone", "read_only": False, "is_required": False}
    )
    language: str = field(
        metadata={"mambu_source": "language", "read_only": False, "is_required": False}
    )
    user_state: str = field(
        metadata={"mambu_source": "userState", "read_only": False, "is_required": False}
    )
    two_factor_authentication: bool = field(
        metadata={
            "mambu_source": "twoFactorAuthentication",
            "read_only": False,
            "is_required": False,
        }
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
    role: UserRoles = field(
        metadata={
            "mambu_source": "role",
            "is_vo": True,
            "read_only": False,
            "is_required": False,
            "model": "UserRoles",
        }
    )
    talento_usuario: dict = field(
        metadata={
            "mambu_source": "_talento_usuario",
            "read_only": False,
            "is_required": False,
        }
    )
    tribus_usuario: list[dict] = field(
        metadata={
            "mambu_source": "_tribus_usuario",
            "read_only": False,
            "is_required": False,
        }
    )
    id_empleado: str = field(
        metadata={
            "mambu_source": "id_empleado",
            "read_only": False,
            "is_required": False,
            "is_cf": True,
            "path": "/_talento_usuario/id_empleado",
        }
    )

    unidades_coordinador_0: str = field(
        metadata={
            "mambu_source": "UnidadesCoordinador_0",
            "read_only": False,
            "is_required": False,
        }
    )
    assigned_branch: Branches = field(
        metadata={
            "mambu_source": "assignedBranch",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Branches",
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

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
