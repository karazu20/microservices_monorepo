import pytest
from twilio.base.exceptions import TwilioRestException

from setup.adapters import messenger_service


def test_twilio_sms(mocker):
    mock_twilio_client = mocker.patch("setup.adapters.messenger_service.twilio_Client")
    data = {
        "phone_number": "5543542827",
        "message": "Hola",
    }
    messenger_service.TwilioService.send_sms("55778899011", "HOLA")
    mock_twilio_client.assert_called()

    status = 500
    uri = "/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json"
    error_message = (
        "El mensaje SMS no pudo ser enviado. "
        "Estamos solicitando ayuda de Soporte Técnico."
    )

    mock_twilio_client.side_effect = TwilioRestException(
        status, uri, code=21211, msg=error_message
    )

    with pytest.raises(messenger_service.SMSError) as e:
        assert messenger_service.TwilioService.send_sms("55778899011", "HOLA")

    mock_twilio_client.side_effect = Exception("Error en twilio")

    with pytest.raises(messenger_service.SMSError) as e:
        assert messenger_service.TwilioService.send_sms("55778899011", "HOLA")
