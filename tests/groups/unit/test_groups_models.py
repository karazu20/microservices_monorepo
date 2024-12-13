from src.groups.domain.models import Grupo, Usuario


def test_usuario():
    model = Usuario(
        "prueba_podemos",
    )
    assert model.usuario_id is None
    assert model.username == "prueba_podemos"


def test_grupo():
    model = Grupo(
        "prueba_grupo_podemos",
    )
    assert model.grupo_id is None
    assert model.nombre == "prueba_grupo_podemos"
