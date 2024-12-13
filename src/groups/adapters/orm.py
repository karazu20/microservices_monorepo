from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry, relationship

from src.groups.domain import models

mapper_registry = registry()
metadata = MetaData()


usuario = Table(
    "usuario",
    metadata,
    Column("usuario_id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(64), unique=True, nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("middle_name", String(50)),
    Column("first_surname", String(50), nullable=False),
    Column("second_surname", String(50)),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)

grupo = Table(
    "grupo",
    metadata,
    Column("grupo_id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(64)),
    Column("mambu_id", String(50), unique=True, nullable=False),
    Column("usuario_id", ForeignKey("usuario.usuario_id"), nullable=False),
    Column(
        "insert_date",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "update_date",
        DateTime,
        onupdate=func.now(),
    ),
    Column(
        "delete_date",
        DateTime,
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(
        models.Usuario,
        usuario,
        properties={"username": usuario.c.username, "usuario_id": usuario.c.usuario_id},
    )
    mapper_registry.map_imperatively(
        models.Grupo,
        grupo,
        properties={
            "nombre": grupo.c.nombre,
            "_usuario": relationship(models.Usuario),
        },
    )
