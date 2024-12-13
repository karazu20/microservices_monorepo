from flask import g

from fakes.adapters import FakeUnitOfWork
from setup import sessions
from src.groups.domain.commands import ADDGroup
from src.groups.domain.queries import GetGrupo
from src.groups.services_layer import handlers


def test_add_grupo(postgres_db):
    uow = FakeUnitOfWork()
    model_groups = ADDGroup(
        nombre="marvel",
    )
    g.user = sessions.User("user.fake", "user.fake@fakedomain.com")
    handlers.add_group(model_groups, uow)


def test_get_grupo(postgres_db):
    uow = FakeUnitOfWork()
    qry = GetGrupo()
    g.user = sessions.User("user.fake", "user.fake@fakedomain.com")
    grupos = handlers.get_grupo(qry, uow)
    assert len(grupos) == 0
