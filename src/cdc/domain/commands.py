from dataclasses import field
from datetime import date, datetime
from typing import Optional

from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDPerson(Command):
    nombre: str = field(metadata={"required": True})
    apellido_paterno: str = field(metadata={"required": True})
    apellido_materno: str = field(metadata={"required": True})
    fecha_nacimiento: Optional[date] = field(metadata={"required": True})
    curp: str = field(metadata={"required": True})
    rfc: str = field(metadata={"required": True})
    nacionalidad: str = field(metadata={"required": False})
    direccion: str = field(metadata={"required": True})
    colonia: str = field(metadata={"required": True})
    delegacion: str = field(metadata={"required": True})
    ciudad: str = field(metadata={"required": True})
    estado: str = field(metadata={"required": True})
    codigo_postal: str = field(metadata={"required": True})
    es_referida: bool = field(metadata={"required": True})
    nip: Optional[str] = field(metadata={"required": False})
    timestamp_aprobacion_consulta: datetime = field(metadata={"required": False})
    timestamp_aprobacion_tyc: datetime = field(metadata={"required": False})
    grupo_id: Optional[int] = field(metadata={"required": False}, default=None)


# V2
@dataclass
class ValidateConsultaCDC(Command):
    nombre: str = field(metadata={"required": True})
    apellido_paterno: str = field(metadata={"required": True})
    apellido_materno: str = field(metadata={"required": True})
    fecha_nacimiento: Optional[date] = field(metadata={"required": True})
    curp: str = field(metadata={"required": True})
    nacionalidad: str = field(metadata={"required": False})
    direccion: str = field(metadata={"required": True})
    colonia: str = field(metadata={"required": True})
    codigo_postal: str = field(metadata={"required": True})
    es_referida: bool = field(metadata={"required": True})
    nip: Optional[str] = field(metadata={"required": False})
    timestamp_aprobacion_consulta: datetime = field(metadata={"required": False})
    timestamp_aprobacion_tyc: datetime = field(metadata={"required": False})
