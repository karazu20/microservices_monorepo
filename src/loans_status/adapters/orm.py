from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.orm import registry

from src.loans_status.domain import models

mapper_registry = registry()
metadata = MetaData()


ENUM_STATUS = (
    "PENDIENTE_VALIDACION",
    "VALIDADO",
    "PENDIENTE_APROBACION",
    "APROBADO",
    "PENDIENTE_DESEMBOLSO",
    "DESEMBOLSADO",
    "ACTIVO",
    "CANCELADO",
    "INCIDENCIAS",
    "RECHAZADO",
)


loan_status = Table(
    "estatus_credito",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("id_mambu", String(10)),
    Column("estatus", Enum(*ENUM_STATUS, name="enum_estatus_credito_estatus")),
    Column("comentarios", Text()),
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
    mapper_registry.map_imperatively(models.LoanStatus, loan_status)
