import abc
import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from setup import config

logger = logging.getLogger(__name__)


class AbstractSMTP(abc.ABC):
    smtp: Any = NotImplemented

    @classmethod
    @abc.abstractmethod
    def send(cls, to: list, cc: list, subject: str, message: str, attachments: list = []):
        raise NotImplementedError


class SmtpEmail(AbstractSMTP):
    smtp = smtplib.SMTP_SSL

    @classmethod
    def _get_connection(cls):
        smtp = cls.smtp(host=config.EMAIL_HOST, port=config.EMAIL_PORT)
        smtp.login(config.EMAIL_USER, config.EMAIL_PASS)
        return smtp

    @classmethod
    def _get_attachment(cls, filename: str) -> Any:
        _file = open(filename, "rb")

        part = MIMEBase("application", "octet-stream")
        part.set_payload(_file.read())

        encoders.encode_base64(part)

        filename = os.path.basename(filename)

        part.add_header("Content-Disposition", "attachment", filename=filename)
        return part

    @classmethod
    def send(cls, to: list, cc: list, subject: str, message: str, attachments: list = []):
        try:
            logger.info(
                "Correo: to=%s cc=%s message=%s attachments=%s",
                str(to),
                str(cc),
                message,
                str(attachments),
            )

            _from = config.EMAIL_SENDER

            multipart = MIMEMultipart()
            multipart["Subject"] = subject
            multipart["From"] = _from
            multipart["To"] = ", ".join(to)
            multipart["CC"] = ", ".join(cc)

            plain_part = MIMEText(message, "plain")

            multipart.attach(plain_part)

            for filename in attachments:
                _file = cls._get_attachment(filename)
                multipart.attach(_file)

            smtp = cls._get_connection()
            smtp.sendmail(_from, to, multipart.as_string())
            smtp.quit()

            for filename in attachments:
                os.remove(filename)
        except Exception as ex:
            logger.error("Error al enviar correo a %s: %s", str(to), str(ex))
