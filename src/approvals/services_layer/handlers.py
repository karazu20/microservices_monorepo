import logging

from setup import domain  # type: ignore
from setup.adapters import podemos_mambu
from src.approvals.domain import commands

from typing import Callable, Dict, Type  # isort:skip


logger = logging.getLogger(__name__)


def add_change_status_approval(
    cmd: commands.ADDApproval,
    mambu: podemos_mambu.PodemosMambu,
):

    messages = []
    status = False
    try:
        mambu_loan = mambu.loans.get(id=cmd.id_mambu)
    except Exception:
        messages.append({"Error al obtener el ID en Mambu " + cmd.id_mambu})
        return {
            "id_mambu": cmd.id_mambu,
            "status": status,
            "messages": messages,
        }

    if mambu_loan.account_state != "PENDING_APPROVAL":
        logger.info(
            "Cuenta tiene diferente estatus a PENDING_APPROVAL: %s", mambu_loan.id
        )
        return {
            "id_mambu": cmd.id_mambu,
            "status": status,
            "messages": "La cuenta debe estar en Pendiente de Aprobación (PENDING_APPROVAL)",
        }

    try:
        mambu_loan.update_state(
            "APPROVE",
            "Approved via API",
        )
        status = True
        logger.info("Cuenta aprobada con éxito %s", mambu_loan.id)
    except Exception as ex:
        logger.error("Error al aprobar la cuenta %s", ex)
        messages.append({"Error al aprobar la cuenta " + cmd.id_mambu})
        return {
            "id_mambu": cmd.id_mambu,
            "status": status,
            "messages": messages,
        }

    return {
        "id_mambu": cmd.id_mambu,
        "status": status,
        "messages": messages,
    }


QUERY_HANDLERS = {}  # type: ignore


COMMAND_HANDLERS = {
    commands.ADDApproval: add_change_status_approval,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {}  # type: ignore
