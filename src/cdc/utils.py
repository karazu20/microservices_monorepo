from typing import Callable, List

from src.cdc import config


def _gen_tribus_usuario(tribus_usuario: list):
    for tribu in tribus_usuario:
        yield tribu["UnidadesCoordinador"]


def _gen_tribus_usuario_2(tribus_usuario: list):
    for tribu in tribus_usuario:
        yield tribu


def get_recipients_email(
    tribus_usuario: list, consejeros: list, gen_tribus: Callable = _gen_tribus_usuario
) -> List[str]:
    tribus_emails: list = []
    if tribus_usuario is not None:
        tribus_emails = [
            "cc." + n.lower().replace("tribu", "") + "@podemos.mx"
            for n in gen_tribus(tribus_usuario)
        ]

    emails = tribus_emails + consejeros

    if config.CDC_EMAIL_HUB.count(""):
        config.CDC_EMAIL_HUB.remove("")

    return emails + config.CDC_EMAIL_HUB
