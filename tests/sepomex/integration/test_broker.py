import pytest

from fakes.adapters import FakeBus, FakeCache, FakePodemosMambu, FakeUnitOfWork
from setup import inject
from setup.domain.events import CompletedColonia
from src.sepomex.domain.commands import ADDEstado, ADDMunicipio
from src.sepomex.domain.queries import GetEstados, GetMunicipios
from src.sepomex.services_layer import handlers


@pytest.fixture
def broker():
    broker = inject.start_broker(
        handlers=handlers,
        orm=None,
        uow=FakeUnitOfWork(),
        bus=FakeBus(),
        cache=FakeCache(),
        mambu=FakePodemosMambu(),
    )
    yield broker


def test_broker(broker):
    edomex = ADDEstado("Edomex")
    broker.handle(edomex)
    edos = GetEstados()
    estados = broker.handle(edos)

    assert len(estados) == 1

    ixtapaluca = ADDMunicipio("Ixtapaluca", "Edomex")
    broker.handle(ixtapaluca)
    muns = GetMunicipios("Edomex")
    municipios = broker.handle(muns)
    assert len(municipios) == 1

    completed_colonia = CompletedColonia("Valle")
    completed = broker.handle(completed_colonia)
    assert completed
