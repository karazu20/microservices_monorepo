from dataclasses import field

import marshmallow.validate
from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDColonia(Command):
    nombre: str = field(metadata={"required": True})
    codigo_postal: str = field(metadata={"required": True})
    municipio: str = field(metadata={"required": True})
    ciudad: str = ""
    asentamiento: str = ""

    @marshmallow.validates("codigo_postal")
    def validates(self, value):
        if len(value) > 5:
            raise marshmallow.ValidationError("CP too long")
        if not value.isdigit():
            raise marshmallow.ValidationError("CP should only digits")


@dataclass
class ADDMunicipio(Command):
    nombre: str = field(metadata={"required": True})
    estado: str = field(metadata={"required": True})


@dataclass
class ADDEstado(Command):
    nombre: str = field(metadata={"required": True})
