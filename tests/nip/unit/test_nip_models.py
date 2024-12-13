from src.nip.domain.models import Nip


def test_nip():
    model = Nip(
        nombre="JUAN PRUEBA DOS", telefono="4345234555", curp="EARJ950927MDFSBS09"
    )
    assert model.id is None
    assert model.nombre == "JUAN PRUEBA DOS"
    assert model.telefono == "4345234555"
    assert model.curp == "EARJ950927MDFSBS09"
