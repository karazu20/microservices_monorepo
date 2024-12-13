from sqlalchemy import Column, Date, DateTime, Integer, MetaData, String, Table, func
from sqlalchemy.orm import registry

from src.nip.domain import models

mapper_registry = registry()
metadata = MetaData()
nip_table = Table(
    "nip_cdc",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("nip", String(25), nullable=False),
    Column("nombre", String(112), nullable=False),
    Column("telefono", String(16), nullable=False),
    Column("curp", String(18), nullable=False),
    Column("fecha", Date, nullable=False),
    Column("vigente", Integer, nullable=False, default=1),
    Column("validado", Integer, nullable=False, default=0),
    Column("num_consultas", Integer, nullable=False, default=0),
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
        nullable=True,
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
    Column("timestamp_validado", DateTime, nullable=True),
    Column("num_envios", Integer, nullable=True, default=0),
)


def start_mappers():
    mapper_registry.map_imperatively(models.Nip, nip_table)
