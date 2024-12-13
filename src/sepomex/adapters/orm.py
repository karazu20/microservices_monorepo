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

from src.sepomex.domain import models

mapper_registry = registry()
metadata = MetaData()

estado = Table(
    "estados",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50)),
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

municipio = Table(
    "municipios",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(50)),
    Column("id_estado", ForeignKey("estados.id")),
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

colonia = Table(
    "colonias",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nombre", String(150), nullable=False, doc="Nombre de la colonia"),
    Column("ciudad", String(50), nullable=False, doc="Nombre de la ciudad"),
    Column(
        "asentamiento",
        String(25),
        nullable=False,
        doc="Tipo de asentamiento (Colonia Fraccionamiento, Condominio, Unidad habitacional, etc)",
    ),
    Column("codigo_postal", String(5), nullable=False, doc="Codigo Postal"),
    Column("id_municipio", ForeignKey("municipios.id")),
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


def start_mappers():
    mapper_registry.map_imperatively(
        models.Estado,
        estado,
        properties={
            "_municipios": relationship(models.Municipio),
        },
    )

    mapper_registry.map_imperatively(
        models.Municipio,
        municipio,
        properties={
            "_colonias": relationship(models.Colonia),
        },
    )

    mapper_registry.map_imperatively(models.Colonia, colonia)
