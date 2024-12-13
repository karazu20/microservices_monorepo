from sqlalchemy import (
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
from sqlalchemy.orm import registry, relationship

from src.storage.config import TIPO_ENTIDAD
from src.storage.domain import models

mapper_registry = registry()
metadata = MetaData()


filetype = Table(
    "tipo_archivo",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tipo", String(128)),
)

document_type = Table(
    "tipo_documentos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tipo", String(64)),
    Column("descripcion", String(128), nullable=True),
)

document = Table(
    "documentos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tipo_documento_id", ForeignKey("tipo_documentos.id"), nullable=False),
    Column("tipo_archivo_id", ForeignKey("tipo_archivo.id"), nullable=False),
    Column(
        "storage_id",
        String(256),
        unique=True,
        index=True,
    ),
    Column("podemos_id", String(16), nullable=False),
    Column("comentario", String(256), nullable=True),
    Column(
        "tipo_entidad",
        Enum(*TIPO_ENTIDAD, name="enum_documentos_tipo_entidad"),
        nullable=False,
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
        onupdate=func.now(),
        doc="Timestamp en que se modifico por ultima vez el registro",
    ),
)


def start_mappers():
    mapper_registry.map_imperatively(models.FileType, filetype)
    mapper_registry.map_imperatively(models.DocumentType, document_type)

    mapper_registry.map_imperatively(
        models.Document,
        document,
        properties={
            "_tipo_archivo": relationship(models.FileType),
            "_tipo_documento": relationship(models.DocumentType),
        },
    )
