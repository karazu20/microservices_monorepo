from src.cdc.entrypoints import consumers
from tests.cdc.utils import XML_TEST_ACCOUNTS


def test_consumer_sent_mail():
    data = {
        "to": ["user.fake@fakedomain.com"],
        "cc": ["fake@domain.com"],
        "subject": "CDC User_Fake FAKE_FOLIO user.fake",
        "message": "Esta consulta fue generada por user.fake",
        "attachments": ["/fake/path/file.pdf"],
    }
    response = consumers.email_sent(data)
    assert response == True


def test_consumer_valid_consulta_cdc_generated():
    data = {
        "cdc_folio": "876657434",
        "username": "my.username",
        "consejero_email": "m.consejero@podemos.mx",
        "tribus_usuario": ["TribuEXAMPLE-1"],
        "xml_response": XML_TEST_ACCOUNTS,
    }
    response = consumers.valid_consulta_cdc_generated(data)
    assert response == True
