from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    func,
)
from sqlalchemy.orm import registry

from src.pambu.domain import models

mapper_registry = registry()
metadata = MetaData()

rol = Table(
    "rol",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "nombre",
        String(32),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "nombre_corto",
        String(64),
        nullable=True,
        unique=True,
        index=True,
    ),
    Column(
        "notas",
        String(32),
        nullable=True,
    ),
    Column(
        "active",
        Boolean,
        nullable=False,
        default=True,
    ),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)


user = Table(
    "usuario",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "username",
        String(32),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "email",
        String(64),
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "google_id",
        String(32),
        nullable=True,
        unique=True,
        index=True,
    ),
    Column(
        "google_picture",
        String(128),
        nullable=True,
        unique=True,
        index=True,
    ),
    Column(
        "notas",
        String(256),
        nullable=True,
        unique=True,
        index=True,
    ),
    Column(
        "active",
        Boolean,
        nullable=False,
        default=True,
    ),
    Column("pass_mambu", String(256)),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    # Foreign keys
    Column("id_rol", Integer, ForeignKey("rol.id"), nullable=False),
)

sistemas_podemos = Table(
    "sistemas_podemos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "nombre_sistema",
        String(25),
        nullable=False,
        unique=True,
    ),
    Column(
        "id_sistema",
        String(64),
        nullable=False,
        unique=True,
    ),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se creo el registro",
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)


releases = Table(
    "releases",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "id_version",
        String(25),
        nullable=False,
        unique=True,
    ),
    Column(
        "url_version",
        String(128),
        nullable=False,
        unique=True,
    ),
    Column(
        "tipo_release",
        Enum(
            *(
                "ALFA",
                "BETA",
                "CANDIDATES",
                "PRODUCTION",
            ),
            name="enum_versiones_spore"
        ),
    ),
    Column(
        "vigente",
        Boolean,
        nullable=False,
        default=True,
    ),
    Column("pass_mambu", String(256)),
    Column(
        "created",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    Column(
        "updated",
        DateTime,
        nullable=False,
        default=func.now(),
    ),
    # Foreign keys
    Column("id_sistema", Integer, ForeignKey("sistemas_podemos.id"), nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(models.User, user)
    mapper_registry.map_imperatively(models.Releases, releases)
