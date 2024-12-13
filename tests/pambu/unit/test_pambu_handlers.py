from fakes.adapters import FakeUnitOfWork
from src.pambu.domain.commands import ADDUser
from src.pambu.services_layer import handlers


def test_personas(mambu):
    user = mambu.users.build(id="batman", username="batman", email="baticueva@testo.mx")
    mambu.users.add(user)
    uow = FakeUnitOfWork()
    model_user = ADDUser(
        username="batman",
        email="baticueva@testo.mx",
        id_rol="2",
    )
    handlers.add_user(model_user, uow, mambu)
    assert uow.committed
