from fakes.adapters import FakeBus
from setup.domain import events
from src.cdc import config
from src.cdc.adapters import file_service
from src.cdc.services_layer import handlers
from tests.cdc.utils import XML_TEST_ACCOUNTS


def test_create_and_send_pdf():
    back_cdc_email_active = config.CDC_EMAIL_ACTIVE
    fake_bus = FakeBus()
    event = events.ValidConsultaCdc(
        username="my.username",
        consejero_email="m.consejero@podemos.mx",
        tribus_usuario=["TribuEXAMPLE-1"],
        cdc_folio="876657434",
        xml_response=XML_TEST_ACCOUNTS,
    )
    fake_fileservice = file_service.FakeFileService()

    config.CDC_EMAIL_ACTIVE = True
    result = handlers.create_and_send_pdf(event, fake_bus, fake_fileservice)
    config.CDC_EMAIL_ACTIVE = back_cdc_email_active

    assert result == True
    assert fake_bus.published == True
    assert len(fake_bus.bus) > 0
    assert fake_bus.bus[-1].to == [
        "cc.example-1@podemos.mx",
        "m.consejero@podemos.mx",
        "email@separated-by.comma",
    ]
    assert fake_bus.bus[-1].cc == []
    assert fake_bus.bus[-1].subject == "CDC LIDIA PRUEBA PRUEBA 876657434 my.username"
    assert fake_bus.bus[-1].message == "Esta consulta fue generada por my.username"
    assert fake_bus.bus[-1].attachments == ["MOCKFILE.mock"]
    assert fake_fileservice.saved == True
