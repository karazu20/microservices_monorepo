from __future__ import annotations

import abc
import logging

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as twilio_Client

from setup.config import TWILIO_ACCOUNTSID, TWILIO_AUTHTOKEN, TWILIO_FROMNUMBER

logger = logging.getLogger(__name__)


class SMSError(Exception):
    def __init__(self, message):
        self.message = message


class MessageErrorResponse:
    errors = {
        "0": "El mensaje SMS no pudo ser enviado. Estamos solicitando ayuda de Soporte Técnico.",
        "21211": "El número de teléfono ingresado no es un número valido",
        "21614": (
            "El mensaje SMS no pudo ser enviado "
            "debido a que el #{} no es un número de teléfono celular."
        ),
    }

    def get(self, code=None, phone_number=None):
        try:
            err = self.errors[str(code)]
        except KeyError:
            err = self.errors["0"]
        if phone_number is None:
            return err
        return err.format(phone_number)


class MessengerService(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def send_sms(cls, phone_number: str, message: str) -> bool:
        raise NotImplementedError


class TwilioService(MessengerService):
    @classmethod
    def send_sms(cls, phone_number: str, message: str) -> bool:
        "Send SMS el NIP"
        logger.info("Sending sms: {} to phone: {}".format(message, phone_number))
        try:
            twilio_client = twilio_Client(TWILIO_ACCOUNTSID, TWILIO_AUTHTOKEN)
            response = twilio_client.messages.create(
                body=message,
                from_=TWILIO_FROMNUMBER,
                to="+52{}".format(phone_number),
            )
            logger.info(
                "Sms sent to phone %s with SID %s.", phone_number, str(response.sid)
            )
            return response.sid
        except TwilioRestException as twex:
            error_message = MessageErrorResponse().get(twex.code, phone_number)
            logger.error("TwilioRestException: {}".format(error_message))
            raise SMSError(error_message)
        except Exception as ex:
            logger.error("Error en twilio: {}".format(ex))
            raise SMSError("Error en twilio {}".format(ex))
