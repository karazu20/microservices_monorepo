from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Command


@dataclass
class ADDCommentLoan(Command):
    comment: str = field(metadata={"required": True})
    id_mambu: str = field(metadata={"required": True})


@dataclass
class ADDCommentGroup(Command):
    comment: str = field(metadata={"required": True})
    id_mambu: str = field(metadata={"required": True})


@dataclass
class ADDCommentClient(Command):
    comment: str = field(metadata={"required": True})
    id_mambu: str = field(metadata={"required": True})
