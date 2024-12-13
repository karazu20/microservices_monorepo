from dataclasses import dataclass, field

from flask import g

from setup.data_bases import session_pambu_scope
from shared import security


@dataclass
class User:
    username: str = ""
    email: str = ""
    pass_mambu: str = field(init=False)

    def __post_init__(self):
        with session_pambu_scope() as session_pambu:  # type: ignore
            try:
                result = session_pambu.execute(
                    """
                    SELECT pass_mambu FROM usuario WHERE email = :email
                    """,
                    dict(email=self.email),
                )

                pass_encrypted = list(result)[0][0]
                self.pass_mambu = security.decrypt_pass(pass_encrypted)
            except (IndexError, TypeError):
                self.pass_mambu = ""


def current_user():
    try:
        return g.user
    except AttributeError:
        return None
