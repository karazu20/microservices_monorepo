from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDApproval(Command):
    id_mambu: str = field(metadata={"required": True})
