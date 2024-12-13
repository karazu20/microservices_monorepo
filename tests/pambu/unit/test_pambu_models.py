from src.pambu.domain.models import Releases, User


def test_user():
    model = User(
        "Ines",
        "ines@prueba.mx",
    )
    assert model.id is None
    assert model.username == "Ines"
    assert model.email == "ines@prueba.mx"


def test_realease():
    model = Releases(
        "fakeurl.com",
        True,
    )
    assert model.id is None
    assert model.url_version == "fakeurl.com"
    assert model.vigente == True
