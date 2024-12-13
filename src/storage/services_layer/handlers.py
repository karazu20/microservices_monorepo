import logging

from setup import domain  # type: ignore
from setup.adapters import storage
from src.storage.config import BUCKET
from src.storage.domain import commands, queries
from src.storage.domain.models import Document, DocumentType, FileType
from src.storage.services_layer import unit_of_work

from typing import Callable, Dict, Type  # isort:skip


logger = logging.getLogger(__name__)


def get_url(
    query: queries.GetUrl,
    uow: unit_of_work.UnitOfWorkDocument,
    storage: storage.S3,
):
    with uow:
        model = uow.document._get(storage_id=query.storage_id)
        uow.commit()
        if not model:
            raise Exception("No existe el recurso solicitado")

        storage_url = storage.get_url(bucket=BUCKET, key_file=model.storage_id)
        logger.info("URL generada: %s" % storage_url)
        return storage_url


def add_document(
    command: commands.ADDDocument,
    uow: unit_of_work.UnitOfWorkDocument,
    storage: storage.S3,
):
    with uow:
        query_filetype = uow.document.get_filetype(tipo=command.tipo_archivo)
        if not query_filetype:
            raise Exception("El tipo de archivo no existe")
        query_document_type = uow.document.get_document_type(id=command.tipo_documento_id)
        model_filetype = FileType()
        model_filetype.id = query_filetype.id
        model_filetype.tipo = query_filetype.tipo

        model_document_type = DocumentType()
        model_document_type.id = query_document_type.id
        model_document_type.tipo = query_document_type.tipo
        model_document_type.descripcion = query_document_type.descripcion

        documents = Document(
            podemos_id=command.podemos_id,
            comentario=command.comentario,  # type: ignore
            tipo_entidad=command.tipo_entidad,
        )
        documents.tipo_documento_id = command.tipo_documento_id
        documents.tipo_archivo_id = model_filetype.id
        path_file = documents.save_file(
            file=command.file, filetype=model_filetype, document_type=model_document_type
        )
        uow.document.add(documents)
        uow.commit()

        storage.put(bucket=BUCKET, path_file_name=path_file, key=documents.storage_id)
        logger.info("Guardado en storage con id: %s" % documents.storage_id)

        return {"storage_id": documents.storage_id}


def add_document_type(
    command: commands.ADDDocumentType,
    uow: unit_of_work.UnitOfWorkDocument,
):
    with uow:
        model = DocumentType()
        model.tipo = command.tipo
        model.descripcion = command.descripcion
        uow.document.add(model)
        uow.commit()
        return {"message": "Ok"}


def add_filetype(
    command: commands.ADDFileType,
    uow: unit_of_work.UnitOfWorkDocument,
):
    with uow:
        model = FileType()
        model.tipo = command.tipo
        uow.document.add(model)
        uow.commit()
        return {"message": "Ok"}


def get_document_type(
    queries: queries.GetDocumentType,
    uow: unit_of_work.UnitOfWorkDocument,
):
    with uow:
        list_document_type = uow.document.list_document_type()
        return [
            {
                "id": value.id,
                "tipo": value.tipo,
                "descripcion": value.descripcion,
            }
            for value in list_document_type  # type: ignore
        ]


def get_filetype(
    queries: queries.GetFileType,
    uow: unit_of_work.UnitOfWorkDocument,
):
    with uow:
        list_filetype = uow.document.list_filetype()
        return [
            {
                "id": value.id,
                "tipo": value.tipo,
            }
            for value in list_filetype  # type: ignore
        ]


QUERY_HANDLERS = {
    queries.GetUrl: get_url,
    queries.GetDocumentType: get_document_type,
    queries.GetFileType: get_filetype,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {
    commands.ADDDocument: add_document,
    commands.ADDDocumentType: add_document_type,
    commands.ADDFileType: add_filetype,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {}  # type: ignore
