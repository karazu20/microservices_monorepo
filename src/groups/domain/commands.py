from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDGroup(Command):
    nombre: str = field(metadata={"required": True})
