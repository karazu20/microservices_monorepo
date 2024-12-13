import logging

from setup import domain  # type: ignore
from setup.sessions import current_user
from src.groups.domain import commands, models, queries
from src.groups.errors import GroupsError
from src.groups.services_layer import unit_of_work

from typing import Callable, Dict, Type  # isort:skip

logger = logging.getLogger(__name__)


def get_grupo(
    query: queries.GetGrupo,
    uow: unit_of_work.UnitOfWorkGroups,
) -> list:
    with uow:
        user = current_user()
        query.username = user.username
        list_grupo = uow.view_grupo.search(query)
        return [
            {
                "grupo_id": row[0],
                "nombre": row[1],
                "mambu_id": row[2],
                "created_at": row[3].strftime("%Y-%m-%d"),
            }
            for row in list_grupo  # type: ignore
        ]


def add_group(
    command: commands.ADDGroup,
    uow: unit_of_work.UnitOfWorkGroups,
) -> str:
    with uow:
        user = current_user()
        get_groups = uow.groups.get_grupos(user.username, command.nombre)
        if get_groups:
            logger.info("Grupo duplicado: {}".format(command.nombre))
            raise GroupsError("Grupo existe para usuario {}".format(user.username))
        grupo = models.Grupo(command.nombre)
        uow.groups.add_group(user.username, grupo)
        uow.commit()
        return grupo.grupo_id


QUERY_HANDLERS = {
    queries.GetGrupo: get_grupo,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {
    commands.ADDGroup: add_group,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {}  # type: ignore
