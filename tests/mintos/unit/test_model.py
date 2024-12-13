"""Pruebas unitarias del modelo"""
import datetime as dt

import pytest

from src.mintos.domain.models import (
    CantSendInException,
    CuentaMintos,
    MambuLoan,
    MambuRepayment,
    sendin,
)


def make_mambuloan(entid="", account_state="", fondeador="", repayments=None):
    """Construye un MambuLoan.

    Los repayments se construyen a partir de una lista de diccionarios
    """
    loan = MambuLoan(id=entid, account_state=account_state)
    loan.fondeador = fondeador
    if repayments:
        for num, repayment in enumerate(repayments):
            rep = MambuRepayment(num, repayment["due_date"], state=repayment["state"])
            loan._repayments.append(rep)

    return loan


def make_cuentamintos(id_mambu, fondeador, account_state, repayments=None):
    """Construye una CuentaMintos"""
    loan = make_mambuloan(
        entid=id_mambu,
        account_state=account_state,
        fondeador=fondeador,
        repayments=repayments,
    )

    cuenta_mintos = CuentaMintos(id_mambu=id_mambu, fondeador=fondeador)
    cuenta_mintos._mambu_loan = loan

    return cuenta_mintos


def test_can_sendin():
    """Un sendin se puede mandar a mintos, bajo ciertas condiciones"""
    make_cuentamintos(
        "12345", "PODEMOS", "ACTIVE", [{"state": "PENDING", "due_date": dt.date.today()}]
    )

    cuentamintos_atrasada = make_cuentamintos(
        "12345",
        "PODEMOS",
        "ACTIVE_IN_ARREARS",
        [{"state": "PENDING", "due_date": dt.date.today()}],
    )
    with pytest.raises(
        CantSendInException, match=r"La cuenta [\d]+ no tiene status ACTIVE"
    ):
        sendin(cuentamintos_atrasada, 0.0, 0.0, "$$$")

    cuentamintos_fondeada_por_otro = make_cuentamintos(
        "12345",
        "BANCO DE MONTECARLO",
        "ACTIVE",
        [{"state": "PENDING", "due_date": dt.date.today()}],
    )
    with pytest.raises(
        CantSendInException, match=r"La cuenta [\d]+ no esta fondeada por PODEMOS"
    ):
        sendin(cuentamintos_fondeada_por_otro, 0.0, 0.0, "$$$")

    cuentamintos_ya_pagada = make_cuentamintos(
        "12345", "PODEMOS", "ACTIVE", [{"state": "PAID", "due_date": dt.date.today()}]
    )
    with pytest.raises(
        CantSendInException, match=r"La cuenta [\d]+ ya tiene pagos hechos"
    ):
        sendin(cuentamintos_ya_pagada, 0.0, 0.0, "$$$")
