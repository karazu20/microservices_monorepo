""" Modelo del µservicio de Mintos.
"""

import datetime as dt
from dataclasses import dataclass, field
from typing import Any, List


class MintosException(Exception):
    """Excepcion base"""


class CantSendInException(MintosException):
    """Cuando no se puede fondear con Mintos"""


class MambuModel:
    """Clase padre de los modelos de Mambu"""


@dataclass
class MambuRepayment(MambuModel):
    """Ficha de pago en cuenta de Mambu"""

    ord_num: int = 0
    due_date: dt.date = dt.date.today()
    state: str = ""


@dataclass
class MambuLoan(MambuModel):
    """Cuenta Mambu"""

    id: str = ""
    account_state: str = ""
    fondeador: str = field(init=False)
    _repayments: List[MambuRepayment] = field(default_factory=list)


class MintosModel:
    """Clase padre de los modelos del µservicio de Mintos"""


@dataclass
class CuentaMintos(MintosModel):
    """Cuenta de credito fondeada por Mintos"""

    id_mambu: str = ""
    id_mintos: str = field(init=False)
    fondeador: str = ""
    interes_mintos: float = 0.0
    exchange_rage: float = 0.0
    currency: str = ""
    _mambu_loan: MambuLoan = field(init=False)
    _details: List[Any] = field(default_factory=list, init=False)

    def rebuy(self):
        """Recompra la cuenta a Mintos"""

    def payment(self):
        """Envia un pago a Mintos"""

    def get_details(self):
        """Obtiene los detalles de la cuenta"""
        return self._details


def sendin(
    cuenta_mintos: CuentaMintos,
    interes_mintos: float,
    exchante_rate: float,
    currency: str,
):
    """Envia la cuenta para solicitar fondeo en Mintos"""
    if cuenta_mintos._mambu_loan.account_state != "ACTIVE":
        raise CantSendInException(
            "La cuenta {} no tiene status ACTIVE".format(cuenta_mintos._mambu_loan.id)
        )

    if cuenta_mintos._mambu_loan.fondeador != "PODEMOS":
        raise CantSendInException(
            "La cuenta {} no esta fondeada por PODEMOS".format(
                cuenta_mintos._mambu_loan.id
            )
        )

    if cuenta_mintos._mambu_loan._repayments[0].state != "PENDING":
        raise CantSendInException(
            "La cuenta {} ya tiene pagos hechos".format(cuenta_mintos._mambu_loan.id)
        )

    # send in a Mintos
    # obtiene el id_mintos y se lo asigna a cuenta_mintos
    # envia PDF con agreement
