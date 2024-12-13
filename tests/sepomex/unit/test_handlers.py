from fakes.adapters import FakeBus, FakeUnitOfWork
from src.sepomex.domain.commands import ADDColonia, ADDEstado, ADDMunicipio
from src.sepomex.domain.models import Municipio
from src.sepomex.domain.queries import GetMunicipios
from src.sepomex.services_layer import handlers


def test_add_municipio():
    uow = FakeUnitOfWork()
    edomex = ADDEstado("Edomex")
    handlers.add_estado(edomex, uow)
    cmd_mun = ADDMunicipio("Chalco", "Edomex")
    handlers.add_municipio(cmd_mun, uow)
    # cmd_col = ADDColonia("Valle", "78965", "Chalco")
    # handlers.add_colonia(cmd_col, uow, FakeBus())
    assert uow.committed
    # assert FakeBus.published


def test_get_municipios():
    uow = FakeUnitOfWork()
    edomex = ADDEstado("Edomex")
    handlers.add_estado(edomex, uow)
    cmd_mun = ADDMunicipio("Chalco", "Edomex")
    handlers.add_municipio(cmd_mun, uow)
    qry = GetMunicipios("Edomex")
    municipios = handlers.get_municipios(qry, uow)
    assert len(municipios) == 1


def test_add_colonia():
    uow = FakeUnitOfWork()
    municipio = Municipio("Chalco")
    uow.municipios.add(municipio)
    cmd_col = ADDColonia("Valle", "78965", "Chalco")
    handlers.add_colonia(cmd_col, uow, FakeBus())
    assert uow.committed
    assert FakeBus.published
