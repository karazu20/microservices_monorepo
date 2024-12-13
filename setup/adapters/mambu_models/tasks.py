from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from datetime import datetime
from typing import TYPE_CHECKING

from mambupy.api.mambutask import MambuTask
from mambupy.orm import schema_orm as orm
from mambupy.orm.schema_mambu import Task as ORMTask

from setup.adapters.mambu_models.model import EntityMambu, MambuModel, Mode

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Groups, Users


@dataclass(repr=False)
class Tasks(EntityMambu):

    _model_rest = MambuTask
    _model_orm = ORMTask

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(Tasks), mode, **kwargs)

    due_date: datetime = field(
        metadata={"mambu_source": "dueDate", "read_only": False, "is_required": False}
    )
    title: str = field(
        metadata={"mambu_source": "title", "read_only": False, "is_required": False}
    )
    description: str = field(
        metadata={"mambu_source": "description", "read_only": False, "is_required": False}
    )
    created_by_user_key: str = field(
        metadata={
            "mambu_source": "createdByUserKey",
            "read_only": False,
            "is_required": False,
        }
    )
    status: str = field(
        metadata={"mambu_source": "status", "read_only": False, "is_required": False}
    )
    assigned_user_key: str = field(
        metadata={
            "mambu_source": "assignedUserKey",
            "read_only": False,
            "is_required": False,
        }
    )
    task_link_key: str = field(
        metadata={"mambu_source": "taskLinkKey", "read_only": False, "is_required": False}
    )
    task_link_type: str = field(
        metadata={
            "mambu_source": "taskLinkType",
            "read_only": False,
            "is_required": False,
        }
    )
    assigned_user: Users = field(
        metadata={
            "mambu_source": "assignedUser",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Users",
        }
    )
    task_link: Groups = field(
        metadata={
            "mambu_source": "taskLink",
            "is_entity": True,
            "read_only": False,
            "is_required": False,
            "model": "Groups",
        }
    )

    @classmethod
    def get(cls, id, mode=Mode.REST) -> MambuModel:

        if mode == Mode.REST:
            instance_mambu = cls._model_rest.get(taskId=id)
        else:
            session = orm.Session()
            instance_mambu = session.query(cls._model_orm).filter_by(id=id).first()

        return cls(instance_mambu, mode)
