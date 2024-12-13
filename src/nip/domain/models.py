from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from setup.domain import Model
from src.nip.config import HOURS_BEFORE_NIP_CREATION, MAX_NIP, MAX_RESEND_NIPS
from src.nip.errors import NipError

logger = logging.getLogger(__name__)


@dataclass
class Nip(Model):
    id: int = field(init=False)
    nombre: str = field(default="")
    telefono: str = field(default="")
    curp: str = field(default="")
    nip: str = field(default="")
    vigente: int = field(default=1)
    fecha: date = field(default=datetime.now().date())
    created: datetime = field(default=datetime.now())
    timestamp_validado: datetime = field(default=None)  # type: ignore
    validado: int = field(default=0)
    num_envios: int = field(default=0)
    num_consultas: int = field(default=0)

    def __post_init__(self):
        today = datetime.now()
        self.fecha = today.date()
        self.created = today

    def __repr__(self):
        return "NipCdC(nip: {0}, telefono: {1}, curp: {2})".format(
            self.nip, self.telefono, self.curp
        )

    def send_nip(self, messenger_service):
        logger.info(
            "Send SMS curp: {}, nip: {}, date: {}".format(self.curp, self.nip, self.fecha)
        )
        message = (
            "Tu NIP de Podemos Progresar es {} compártelo con tu CE. "
            "Revisa nuestro aviso de privacidad http://bit.ly/3Qgi4os".format(self.nip)
        )
        messenger_service.send_sms(self.telefono, message)
        self.num_envios = self.num_envios + 1

    def validate_nip(self):
        """Valida un nip vigente."""
        logger.info("function validate_nip: {}".format(self.nip))
        if not self._isnt_expirate_nip():
            logger.error("This NIP cant´n be valid %s, expired" % (self.nip))
            raise NipError(
                "El código que ingresaste ha expirado. Envía un nuevo código a la emprendedora"
            )
        self.validado = 1
        self.timestamp_validado = datetime.now()

    def resend_nip(self, messenger_service):
        """Utiliza un nip.

        Como requisito, el nip debe estar vigente y no estar validado

        reenviar un nip llama la funcion send nip siempre y cuando el renvio de nips no sea excedido
        """
        logger.info("Method resend_nip: {}".format(self.nip))
        if self.is_valid_expirate_nip():
            logger.error("Cant send NIP %s, is consulted" % (self.nip))
            raise NipError(
                "No se puede reenviar el NIP {}, ya se encuentra consultado".format(
                    self.nip
                )
            )
        if not self._isnt_expirate_nip():
            logger.error("Cant send NIP %s, this expired" % (self.nip))
            raise NipError(
                "No se puede reenviar el NIP {}, no se encuentra vigente".format(self.nip)
            )
        if self.num_envios is None:
            self.num_envios = 0
        if self.num_envios <= MAX_RESEND_NIPS:
            self.send_nip(messenger_service)
        else:
            logger.error(
                "Cant send NIP {}, the number of sends by sms was reached {}".format(
                    self.nip, self.telefono
                )
            )
            raise NipError(
                "No se puede reenviar el NIP {}, ya se alcanzó el número máximo de reenvios para la integrante".format(
                    self.nip
                )
            )

    def is_valid_expirate_nip(self):
        """Comprueba que un nip exista y no tenga mas de dos consultas.
        Un nip se considera valido si:
        - Su flag vigente esta en True (default)
        - Su fecha coincide con el dia de hoy
        - Su fecha de creacion no fue hace mas de 2 horas
        - Las veces que ha sido usado no excede MAX_NIP veces
        """
        logger.info("Method is_valid_nip: {}".format(self.nip))
        if self.num_consultas > MAX_NIP and self._isnt_expirate_nip():
            logger.info("Method is_valid_expirate_nip: True")
            return True
        logger.info("Method is_valid_expirate_nip: False")
        return False

    def _isnt_expirate_nip(self) -> bool:
        """Comprueba que un nip sea vigente
        El nip se considera vigente si:
        - Su fecha coincide con el dia de hoy
        - Su fecha de creacion no fue hace mas de x horas configuradas en la variable HOURS_BEFORE_NIP_CREATION
        - Las veces que ha sido usado no excede MAX_NIP veces
        """
        logger.debug("Start function is_valid_nip {} ".format(self.nip))
        if self.vigente:
            logger.debug("IF is_valid_nip: %s" % (self.vigente))
            logger.debug(
                "IF this info %s : %s"
                % (
                    self.fecha.strftime("%Y%m%d"),
                    date.today().strftime("%Y%m%d"),
                )
            )
            if self.fecha.strftime("%Y%m%d") == date.today().strftime("%Y%m%d"):
                logger.debug(
                    "If this INFO %s : %s"
                    % (
                        self.fecha.strftime("%Y%m%d"),
                        date.today().strftime("%Y%m%d"),
                    )
                )
                logger.debug(
                    "If this Info %s : %s"
                    % (
                        (
                            self.created + timedelta(hours=HOURS_BEFORE_NIP_CREATION)
                        ).strftime("%Y%m%d%H%M%S"),
                        (datetime.now().strftime("%Y%m%d%H%M%S")),
                    )
                )
                if (self.created + timedelta(hours=HOURS_BEFORE_NIP_CREATION)).strftime(
                    "%Y%m%d%H%M%S"
                ) >= (datetime.now().strftime("%Y%m%d%H%M%S")):
                    logger.debug(
                        "If this Info %s : %s"
                        % (
                            (
                                self.created + timedelta(hours=HOURS_BEFORE_NIP_CREATION)
                            ).strftime("%Y%m%d%H%M%S"),
                            (datetime.now().strftime("%Y%m%d%H%M%S")),
                        )
                    )
                    logger.debug("If this Info %s : %s" % (self.num_consultas, MAX_NIP))
                    if self.num_consultas < MAX_NIP:
                        logger.debug(
                            "If this info %s : %s" % (self.num_consultas, MAX_NIP)
                        )
                        return True

        return False
