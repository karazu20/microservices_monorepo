from dataclasses import field
from typing import Optional

import marshmallow.validate
from marshmallow_dataclass import dataclass

from setup.domain import Command
from src.storage.config import TIPO_ENTIDAD as TIPO_ENTIDAD_DATA


@dataclass
class ADDDocument(Command):
    tipo_documento_id: int = field(metadata={"required": True})
    tipo_archivo: str = field(metadata={"required": True})
    podemos_id: str = field(metadata={"required": True})
    comentario: Optional[str] = field(metadata={"required": False})
    tipo_entidad: str = field(metadata={"required": True})
    file: str = field(metadata={"required": True})

    @marshmallow.validates("tipo_entidad")
    def validates(self, value):
        if value not in TIPO_ENTIDAD_DATA:
            raise marshmallow.ValidationError(
                "El Tipo de Entidad enviado no se encuentra en las entidades válidas"
            )


@dataclass
class ADDFileType(Command):
    tipo: str = field(metadata={"required": True})


@dataclass
class ADDDocumentType(Command):
    tipo: str = field(metadata={"required": True})
    descripcion: str = field(metadata={"required": True})
