import os
from contextlib import contextmanager
from enum import Enum
from typing import Type, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PodemosDBsMysql(Enum):

    utils = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_UTILS", "podemos"),
        password=os.environ.get("DB_PASS_UTILS", "podemos"),
        host=os.environ.get("DB_HOST_UTILS", "enola"),
        port=os.environ.get("DB_PORT_UTILS", 3306),
        db_name=os.environ.get("DB_NAME_UTILS", "podemos_utils"),
    )

    pambu = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_PAMBU", "podemos"),
        password=os.environ.get("DB_PASS_PAMBU", "podemos"),
        host=os.environ.get("DB_HOST_PAMBU", "enola"),
        port=os.environ.get("DB_PORT_PAMBU", 3306),
        db_name=os.environ.get("DB_NAME_PAMBU", "podemos_pambu"),
    )

    validations = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_VALIDATIONS", "podemos"),
        password=os.environ.get("DB_PASS_VALIDATIONS", "podemos"),
        host=os.environ.get("DB_HOST_VALIDATIONS", "enola"),
        port=os.environ.get("DB_PORT_VALIDATIONS", 3306),
        db_name=os.environ.get("DB_NAME_VALIDATIONS", "podemos_validaciones"),
    )

    digitalization = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_DIGITALIZACION", "podemos"),
        password=os.environ.get("DB_PASS_DIGITALIZACION", "podemos"),
        host=os.environ.get("DB_HOST_DIGITALIZACION", "enola"),
        port=os.environ.get("DB_PORT_DIGITALIZACION", 3306),
        db_name=os.environ.get("DB_NAME_DIGITALIZACION", "podemos_digitalizacion"),
    )

    documents = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_DOCUMENT", "podemos"),
        password=os.environ.get("DB_PASS_DOCUMENT", "podemos"),
        host=os.environ.get("DB_HOST_DOCUMENT", "enola"),
        port=os.environ.get("DB_PORT_DOCUMENT", 3306),
        db_name=os.environ.get("DB_NAME_DOCUMENT", "podemos_documentos"),
    )


class PodemosDBsAurora(Enum):

    utils = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_UTILS", "podemos"),
        password=os.environ.get("DB_PASS_UTILS", "podemos"),
        host=os.environ.get("DB_HOST_UTILS", "enola"),
        port=os.environ.get("DB_PORT_UTILS", 5432),
        db_name=os.environ.get("DB_NAME_UTILS", "podemos_utils"),
    )

    # Schema with legacy dependency
    pambu = (
        "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}".format(
            user=os.environ.get("DB_USER_PAMBU", "podemos"),
            password=os.environ.get("DB_PASS_PAMBU", "podemos"),
            host=os.environ.get("DB_HOST_PAMBU", "enola"),
            port=os.environ.get("DB_PORT_PAMBU", 3306),
            db_name=os.environ.get("DB_NAME_PAMBU", "podemos_pambu"),
        )
        if os.environ.get("ENV", "dev") != "test"
        else "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}".format(
            user=os.environ.get("DB_USER_PAMBU", "podemos"),
            password=os.environ.get("DB_PASS_PAMBU", "podemos"),
            host=os.environ.get("DB_HOST_PAMBU", "enola"),
            port=os.environ.get("DB_PORT_UTILS", 5432),
            db_name=os.environ.get("DB_NAME_PAMBU", "podemos_pambu"),
        )
    )

    validations = (
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}".format(
            user=os.environ.get("DB_USER_VALIDATIONS", "podemos"),
            password=os.environ.get("DB_PASS_VALIDATIONS", "podemos"),
            host=os.environ.get("DB_HOST_VALIDATIONS", "enola"),
            port=os.environ.get("DB_PORT_VALIDATIONS", 5432),
            db_name=os.environ.get("DB_NAME_VALIDATIONS", "podemos_validaciones"),
        )
    )

    digitalization = (
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}".format(
            user=os.environ.get("DB_USER_DIGITALIZACION", "podemos"),
            password=os.environ.get("DB_PASS_DIGITALIZACION", "podemos"),
            host=os.environ.get("DB_HOST_DIGITALIZACION", "enola"),
            port=os.environ.get("DB_PORT_DIGITALIZACION", 5432),
            db_name=os.environ.get("DB_NAME_DIGITALIZACION", "podemos_digitalizacion"),
        )
    )

    documents = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}".format(
        user=os.environ.get("DB_USER_DOCUMENT", "podemos"),
        password=os.environ.get("DB_PASS_DOCUMENT", "podemos"),
        host=os.environ.get("DB_HOST_DOCUMENT", "enola"),
        port=os.environ.get("DB_PORT_DOCUMENT", 5432),
        db_name=os.environ.get("DB_NAME_DOCUMENT", "podemos_documentos"),
    )


EnumDBs = Union[Type[PodemosDBsMysql], Type[PodemosDBsAurora]]


PodemosDBs = (
    PodemosDBsMysql if os.environ.get("SCHEMAS", "Mysql") == "Mysql" else PodemosDBsAurora
)  # type: EnumDBs


def engine_podemos(podemos_db):
    return create_engine(
        podemos_db.value,
        isolation_level="SERIALIZABLE",
        pool_size=10,
        pool_recycle=3600,
    )


def get_session(podemos_db):
    return sessionmaker(bind=engine_podemos(podemos_db))


@contextmanager
def session_pambu_scope():
    session = get_session(PodemosDBs.pambu)()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
