from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Event


@dataclass
class CompletedColonia(Event):
    channel = "created_colonia"
    nombre: str = field(metadata={"required": True})


@dataclass
class Email(Event):
    channel = "send_email"
    to: list = field(metadata={"required": True})
    cc: list = field(metadata={"required": True})
    subject: str = field(metadata={"required": True})
    message: str = field(metadata={"required": True})
    attachments: list = field(metadata={"required": True})


@dataclass
class ValidConsultaCdc(Event):
    channel = "cdc"
    username: str = field(metadata={"required": True})
    consejero_email: str = field(metadata={"required": True})
    tribus_usuario: list = field(metadata={"required": True})
    cdc_folio: str = field(metadata={"required": True})
    xml_response: str = field(metadata={"required": True})
