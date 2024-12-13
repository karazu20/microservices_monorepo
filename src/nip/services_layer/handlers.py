import logging

from setup.adapters import messenger_service
from setup.sessions import current_user
from src.nip.config import LEN_NIP, MAX_NIPS_POR_TEL, MAX_RETRIES
from src.nip.domain import commands, models
from src.nip.errors import NipError
from src.nip.services_layer import unit_of_work
from src.nip.utils import generate_random_nip

from typing import Callable, Dict, List, Type  # isort:skip
from setup import domain  # isort:skip

logger = logging.getLogger(__name__)


def generate_nip(
    command: commands.GenerateNip,
    uow: unit_of_work.UnitOfWorkNip,
    messenger_service: messenger_service.TwilioService,
):
    with uow:
        user = current_user()
        logger.info("{} - Generando NIP: {}".format(user.username, command.curp))
        nip = models.Nip(
            nombre=command.nombre, telefono=command.telefono, curp=command.curp
        )
        # Busqueda DB
        total_nips_by_phone = uow.nips.get_count_nip(nip.telefono)
        if total_nips_by_phone >= MAX_NIPS_POR_TEL:
            logger.error(
                "Se generó el máximo de NIPs para el teléfono %s" % (nip.telefono)
            )
            raise NipError(
                "Se generó el máximo de NIPs para el teléfono {}".format(nip.telefono)
            )
        if total_nips_by_phone:
            nip_resend = uow.nips.get_last_nip(nip.telefono, nip.curp)
            nip = nip_resend if nip_resend else nip

        # Try generate random nip
        if not nip.id:
            retries = 0
            while retries <= MAX_RETRIES:
                random_nip = generate_random_nip(LEN_NIP)
                previous_nip = uow.nips.get(random_nip)
                if not previous_nip:
                    nip.nip = random_nip
                    break

            if retries > MAX_RETRIES:
                logger.error(
                    "Se generó el máximo número de intentos de generación de Nips"
                )
                raise NipError(
                    "Se generó el máximo número de intentos de generación de Nips, "
                    "comunique a su admin de servicio e intente de nuevo"
                )

        uow.nips.add(nip)
        if nip.id:
            logger.info("{} - Reenvio del nip".format(user.username))
            nip.resend_nip(messenger_service)
        else:
            # INSERT DB random_nip
            logger.info("{} - Enviando NIP: {}".format(user.username, command.curp))
            nip.send_nip(messenger_service)
        logger.info(
            "NIP generado exitosamente: {} numero: {} CURP: {}".format(
                nip.nip, nip.telefono, nip.curp
            )
        )
        uow.commit()
        return nip.nip


def validate_nip(
    command: commands.ValidateNip,
    uow: unit_of_work.UnitOfWorkNip,
):
    with uow:
        user = current_user()
        logger.info("{} - Validando NIP: {}".format(user.username, command.nip))
        nip = uow.nips.get(command.nip)
        if nip:
            nip.validate_nip()
            uow.commit()
            return nip.nip
        else:
            logger.info("This Nip dont exist: {}".format(command.nip))
            raise NipError(
                "El código de NIP que ingresaste no es correcto, favor de verificar los dígitos."
            )


def resend_nip(
    command: commands.ResendNip,
    uow: unit_of_work.UnitOfWorkNip,
    messenger_service: messenger_service.TwilioService,
):
    with uow:
        user = current_user()
        logger.info("{} - Reenviado NIP: {}".format(user.username, command.nip))
        nip = uow.nips.get(command.nip)
        if nip:
            nip.resend_nip(messenger_service)
            uow.commit()
            return nip.nip
        else:
            logger.info("{}, This Nip dont exist: {}".format(user.username, command.nip))
            raise NipError(
                "El código de NIP que ingresaste no es correcto, favor de verificar los dígitos."
            )


QUERY_HANDLERS = {}  # type: Dict[Type[domain.Query], Callable]

COMMAND_HANDLERS = {
    commands.GenerateNip: generate_nip,
    commands.ValidateNip: validate_nip,
    commands.ResendNip: resend_nip,
}  # type: Dict[Type[domain.Command], Callable]

EVENT_HANDLERS = {}  # type: Dict[Type[domain.Event], List[Callable]]
