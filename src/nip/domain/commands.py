import re
from dataclasses import field

import marshmallow.validate
from marshmallow.exceptions import ValidationError
from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class GenerateNip(Command):
    nombre: str = field(metadata={"required": True})
    telefono: str = field(metadata={"required": True})
    curp: str = field(metadata={"required": True})

    @marshmallow.validates("nombre")
    def validate_name(self, value):
        if not value:
            raise ValidationError("El nombre no debe estar vacio")

    @marshmallow.validates("telefono")
    def validate_phone(self, value):
        if not value:
            raise marshmallow.ValidationError("El teléfono no debe estar vacío")

        if len(value) != 10 or not value.isnumeric():
            raise marshmallow.ValidationError("El teléfono debe tener 10 dígitos")

    @marshmallow.validates("curp")
    def validate_curp(self, value):
        if not value:
            raise marshmallow.ValidationError("El CURP no debe estar vacío")

        regex_curp = (
            "[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}"
            "(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])"
            "[HM]{1}"
            "(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|"
            "OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)"
            "[B-DF-HJ-NP-TV-Z]{3}"
            "[0-9A-Z]{1}[0-9]{1}$"
        )

        if not re.match(regex_curp, value):
            raise marshmallow.ValidationError("El CURP esta mal capturado")


@dataclass
class ValidateNip(Command):
    nip: str = field(metadata={"required": True})


@dataclass
class ResendNip(Command):
    nip: str = field(metadata={"required": True})
