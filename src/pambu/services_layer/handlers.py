from typing import Callable, Dict, Type  # isort:skip


from setup import domain  # type: ignore
from setup.adapters import podemos_mambu
from src.pambu.domain import commands, models, queries
from src.pambu.services_layer import unit_of_work


class PambuException(Exception):
    """Excepcion base"""


class EmailException(PambuException):
    """Error en el email del usuario"""


def add_user(
    command: commands.ADDUser,
    uow: unit_of_work.UnitOfWorkPambu,
    mambu: podemos_mambu.PodemosMambu,
) -> None:
    with uow:
        user_mambu = mambu.users.get(id=command.username)
        if user_mambu.email.strip() == command.email.strip():
            user_model = models.User(
                command.username,
                command.email,
                command.id_rol,
            )
            uow.user.add(user_model)
            uow.commit()
        else:
            raise EmailException("Email error")


def get_release(
    query: queries.GetRelease,
    uow: unit_of_work.UnitOfWorkPambu,
) -> list:
    with uow:
        last_release = uow.release_url._get_url_release()
        return last_release[0] if last_release else ""


COMMAND_HANDLERS = {
    commands.ADDUser: add_user,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {}  # type: ignore


QUERY_HANDLERS = {
    queries.GetRelease: get_release
}  # type: Dict[Type[domain.Query], Callable]
