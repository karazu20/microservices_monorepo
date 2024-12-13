from flask import g

from fakes.adapters import FakeUnitOfWork
from setup import sessions
from src.cdc.domain.queries import GetConsultCDC
from src.cdc.services_layer import handlers


def test_get_consult_cdc(postgres_db):
    uow = FakeUnitOfWork()
    qry = GetConsultCDC()
    g.user = sessions.User("user.fake", "user.fake@fakedomain.com")
    consultas = handlers.get_consult_cdc(qry, uow)
    assert len(consultas) == 0
