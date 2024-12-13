from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDUser(Command):
    username: str = field(metadata={"required": True})
    email: str = field(metadata={"required": True})
    id_rol: str = field(metadata={"required": True})
