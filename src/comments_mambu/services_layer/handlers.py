import logging

from setup import domain  # type:ignore
from setup.adapters import podemos_mambu
from src.comments_mambu.domain import commands, queries

from typing import Callable, Dict, Type  # isort:skip


logger = logging.getLogger(__name__)


def add_loan_comment(
    cmd: commands.ADDCommentLoan,
    mambu: podemos_mambu.PodemosMambu,
):
    try:
        loan = mambu.loans.get(id=cmd.id_mambu)
        loan.add_comment(cmd.comment)
    except Exception as ex:
        logger.error(
            "Ocurrió un error al obtener el ID de Mambu Credito: %s: %s o agregar el comentario: %s"
            % (cmd.id_mambu, repr(ex), cmd.comment)
        )
        return {
            "status": False,
            "message": "Ocurrió un error al obtener el ID de Mambu o agregar el comentario",
        }

    return {
        "status": True,
        "message": "Mensaje agregado con éxito",
    }


def add_group_comment(
    cmd: commands.ADDCommentGroup,
    mambu: podemos_mambu.PodemosMambu,
):
    try:
        group = mambu.groups.get(id=cmd.id_mambu)
        group.add_comment(cmd.comment)
    except Exception as ex:
        logger.error(
            "Ocurrió un error al obtener el ID de Mambu Grupo: %s: %s o agregar el comentario: %s"
            % (cmd.id_mambu, repr(ex), cmd.comment)
        )
        return {
            "status": False,
            "message": "Ocurrió un error al obtener el ID de Mambu o agregar el comentario",
        }

    return {
        "status": True,
        "message": "Mensaje agregado con éxito",
    }


def add_client_comment(
    cmd: commands.ADDCommentClient,
    mambu: podemos_mambu.PodemosMambu,
):
    try:
        client = mambu.clients.get(id=cmd.id_mambu)
        client.add_comment(cmd.comment)
    except Exception as ex:
        logger.error(
            "Ocurrió un error al obtener el ID de Mambu Cliente: %s: %s o agregar el comentario: %s"
            % (cmd.id_mambu, repr(ex), cmd.comment)
        )
        return {
            "status": False,
            "message": "Ocurrió un error al obtener el ID de Mambu o agregar el comentario",
        }

    return {
        "status": True,
        "message": "Mensaje agregado con éxito",
    }


def get_loan_comments(qry: queries.GetLoanComments, mambu: podemos_mambu.PodemosMambu):
    loan = mambu.loans.get(id=qry.loan_id)

    if not loan.comments:
        return []

    return [
        {
            "created": value.creation_date,
            "comment": value.text,
            "user": mambu.users.get(id=value.user_key).full_name,
        }
        for value in loan.comments
    ]


def get_group_comments(qry: queries.GetGroupComments, mambu: podemos_mambu.PodemosMambu):
    group = mambu.groups.get(id=qry.group_id)

    if not group.comments:
        return []

    return [
        {
            "created": value.creation_date,
            "comment": value.text,
            "user": mambu.users.get(id=value.user_key).full_name,
        }
        for value in group.comments
    ]


def get_client_comments(
    qry: queries.GetClientComments, mambu: podemos_mambu.PodemosMambu
):
    client = mambu.clients.get(id=qry.client_id)

    if not client.comments:
        return []

    return [
        {
            "created": value.creation_date,
            "comment": value.text,
            "user": mambu.users.get(id=value.user_key).full_name,
        }
        for value in client.comments
    ]


QUERY_HANDLERS = {
    queries.GetLoanComments: get_loan_comments,
    queries.GetGroupComments: get_group_comments,
    queries.GetClientComments: get_client_comments,
}  # type: ignore


COMMAND_HANDLERS = {
    commands.ADDCommentLoan: add_loan_comment,
    commands.ADDCommentGroup: add_group_comment,
    commands.ADDCommentClient: add_client_comment,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {}  # type: ignore
