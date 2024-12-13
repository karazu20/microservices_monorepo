from datetime import datetime

from src.cdc.adapters.repositories import ProspectoRepository
from src.cdc.domain.models import Prospecto


def test_add_prospecto_repository(digitalization_session):
    pr = ProspectoRepository(digitalization_session)
    prospectos = pr.session.query(Prospecto).all()
    assert prospectos == []

    prospecto_add_prospecto_repository = Prospecto(
        "ZACA860827MDFLMD00",
        "ADRIANA",
        "",
        "ZALDIVAR",
        "CAMACHO",
        datetime(1986, 8, 27),
        "MX",
        "1111111111",
    )

    pr.add_prospecto(prospecto_add_prospecto_repository)

    prospectos = pr.session.query(Prospecto).all()
    registros_insertados = pr.session.query(Prospecto).count()

    assert prospectos[0].curp == "ZACA860827MDFLMD00"
    assert prospectos[0].nombre == "ADRIANA"
    assert prospectos[0].apellido_materno == "CAMACHO"
    assert registros_insertados == 1

    pr.session.commit()


def test_get_prospecto_repository(digitalization_session):
    pr = ProspectoRepository(digitalization_session)
    pr.session.query(Prospecto).delete()
    prospectos = pr.session.query(Prospecto).all()
    assert prospectos == []

    prospecto_uno_get_prospecto_repository = Prospecto(
        "JABB810826MDFVRT01",
        "BEATRIZ",
        "LETICIA",
        "JAVIER",
        "BARRIOS",
        datetime(1981, 8, 26),
        "MX",
        "1111111111",
    )
    prospecto_dos_get_prospecto_repository = Prospecto(
        "DUHP680622MHGRRL09",
        "PAULINA",
        "",
        "DURAN",
        "HERNANDEZ",
        datetime(1968, 6, 22),
        "MX",
        "2222222222",
    )
    pr.add_prospecto(prospecto_uno_get_prospecto_repository)
    pr.add_prospecto(prospecto_dos_get_prospecto_repository)
    prospectos = pr.session.query(Prospecto).all()
    registros_insertados = pr.session.query(Prospecto).count()

    prospecto = pr.get_prospecto(prospectos[0].curp)

    assert prospectos[0].curp == "JABB810826MDFVRT01"
    assert prospectos[1].curp == "DUHP680622MHGRRL09"
    assert prospectos[0].curp == prospecto.curp
    assert len(prospecto._direcciones) == 0
    assert prospecto.nombre == "BEATRIZ"
    assert prospecto._consultas == []
    assert registros_insertados == 2

    pr.session.commit()
