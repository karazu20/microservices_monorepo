from dataclasses import field

import marshmallow.validate
from marshmallow_dataclass import dataclass

from setup.domain import Command
from src.loans_status.domain.models import LoanStatus


@dataclass
class ADDLoanStatus(Command):
    id_mambu: str = field(metadata={"required": True})
    estatus: str = field(metadata={"required": True})
    comentarios: str = field(metadata={"required": False})

    @marshmallow.validates("estatus")
    def validates(self, value):
        if value not in LoanStatus.ALL_STATUS:
            raise marshmallow.ValidationError(
                "El Estatus enviado no se encuentra en los estatus válidos"
            )
