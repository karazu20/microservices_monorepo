from dataclasses import dataclass, field

from setup.domain import Model


@dataclass
class User(Model):
    id: int = field(init=False)
    username: str = ""
    email: str = ""
    id_rol: str = ""


@dataclass
class Releases(Model):
    id: int = field(init=False)
    url_version: str = ""
    vigente: bool = True
