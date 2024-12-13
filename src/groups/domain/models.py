from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from setup.domain import Model


@dataclass
class Usuario(Model):
    usuario_id: int = field(init=False)
    username: str = field(default="")


@dataclass
class Grupo(Model):
    grupo_id: str = field(init=False)
    nombre: str = ""
    usuario_id: int = field(init=False)
    mambu_id: Optional[str] = ""
    insert_date: Optional[datetime] = None  # type: ignore
    _usuario: Usuario = field(default_factory=Usuario)
