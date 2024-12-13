import logging

from setup import domain  # type: ignore
from src.loans_status.domain import commands, models, queries
from src.loans_status.services_layer import unit_of_work

from typing import Callable, Dict, Type  # isort:skip


logger = logging.getLogger(__name__)


def add_loan_status(
    cmd: commands.ADDLoanStatus,
    uow: unit_of_work.UnitOfWorkLoansStatus,
):
    with uow:
        find_loan_status = uow.loan_status.get(cmd.id_mambu)
        if find_loan_status:
            find_loan_status.estatus = cmd.estatus
            find_loan_status.comentarios = cmd.comentarios
            logger.info("Estatus crédito actualizado %s: %s", cmd.id_mambu, cmd.estatus)
        else:
            loan_status = models.LoanStatus(cmd.id_mambu, cmd.estatus, cmd.comentarios)
            uow.loan_status.add(loan_status)
            logger.info("Estatus crédito guardados %s: %s", cmd.id_mambu, cmd.estatus)
        uow.commit()


def get_loan_status(
    qry: queries.GetLoanStatus,
    uow: unit_of_work.UnitOfWorkLoansStatus,
):
    with uow:
        logger.info("Obtiene los estatus de los créditos")
        loans_status = uow.view_loan_status.search(qry)  # type: ignore
        return [
            {
                "id": loans.id,
                "id_mambu": loans.id_mambu,
                "estatus": loans.estatus,
                "comentarios": loans.comentarios,
            }
            for loans in loans_status
        ]


QUERY_HANDLERS = {
    queries.GetLoanStatus: get_loan_status,
}  # type: Dict[Type[domain.Query], Callable]

COMMAND_HANDLERS = {
    commands.ADDLoanStatus: add_loan_status,
}  # type: Dict[Type[domain.Command], Callable]

EVENT_HANDLERS = {}  # type: Dict[Type[domain.Event], Callable]
