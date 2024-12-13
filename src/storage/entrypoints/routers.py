import logging

from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_restful import Api

from setup.resources import PodemosResource
from src.storage import broker
from src.storage.config import DOCS_PATH_STORAGE
from src.storage.domain import commands, queries

logger = logging.getLogger(__name__)


class StorageUrlResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetUrl.Schema().load(request.args)  # type: ignore
            logger.info("StorageUrlResource: query %s", query)
            storage_url = broker.handle(query)
            return jsonify(
                {
                    "code": "STO200",
                    "data": {"storage_url": storage_url, "msg_success": "Url generada"},
                    "msg": "success",
                }
            )
        except Exception as e:
            if str(e) == "No existe el recurso solicitado":
                logger.error(
                    "No existe el recurso %s : %s",
                    str(e),
                    request.args,
                )
                return {
                    "code": "STO404",
                    "error": {
                        "error": str(e),
                        "msg_error": str(e),
                    },
                    "msg": "fail",
                }, 404

            logger.exception(
                "Existio un error al obtener la Url %s : %s",
                str(e),
                request.args,
            )
            return {
                "code": "STO500",
                "error": {
                    "error": str(e),
                    "msg_error": "Ocurrió un error vuelve a intentarlo",
                },
                "msg": "fail",
            }, 500


class StorageResource(PodemosResource):
    @swag_from(f"{DOCS_PATH_STORAGE}/create_document.yml")
    def post(self):
        try:
            cmd = commands.ADDDocument.Schema().load(request.json)  # type: ignore
            logger.info("ADDDocument Resource: command %s", cmd)
            response = broker.handle(cmd)
            return {
                "code": "STO201",
                "data": response,
                "msg": "success",
            }, 201
        except Exception as e:  # pragma: no cover
            if str(e) == "El tipo de archivo no existe":
                logger.error(
                    "No existe el recurso %s : %s",
                    str(e),
                    request.args,
                )
                return {
                    "code": "STO404",
                    "error": {
                        "error": str(e),
                        "msg_error": str(e),
                    },
                    "msg": "fail",
                }, 404

            logger.error("Error en registrar documento %s:", str(e))
            return {
                "code": "STO400",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 500


class DocumentTypeResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetDocumentType.Schema().load(request.args)  # type: ignore
            logger.info("DocumentTypeResource: query %s", query)
            document_type = broker.handle(query)
            return jsonify(
                {
                    "code": "STO200",
                    "data": document_type,
                    "msg": "success",
                }
            )
        except Exception as e:
            logger.exception(
                "Existio un error al obtener los tipos de documentos %s : %s",
                str(e),
                request.args,
            )
            return {
                "code": "STO500",
                "error": {
                    "error": str(e),
                    "msg_error": "Ocurrió un error vuelve a intentarlo",
                },
                "msg": "fail",
            }, 500

    @swag_from(f"{DOCS_PATH_STORAGE}/create_document.yml")
    def post(self):
        try:
            cmd = commands.ADDDocumentType.Schema().load(request.json)  # type: ignore
            logger.info("ADDDocumentType Resource: command %s", cmd)
            response = broker.handle(cmd)
            return {
                "code": "STO201",
                "data": response,
                "msg": "success",
            }, 201
        except Exception as e:  # pragma: no cover
            logger.error("Error en registrar documento %s:", str(e))
            return {
                "code": "STO400",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 500


class FileTypeResource(PodemosResource):
    def get(self):
        try:
            query = queries.GetFileType.Schema().load(request.args)  # type: ignore
            logger.info("FileTypeResource: query %s", query)
            filetype = broker.handle(query)
            return jsonify(
                {
                    "code": "STO200",
                    "data": filetype,
                    "msg": "success",
                }
            )
        except Exception as e:
            logger.exception(
                "Existio un error al obtener los tipos de archivos %s : %s",
                str(e),
                request.args,
            )
            return {
                "code": "STO500",
                "error": {
                    "error": str(e),
                    "msg_error": "Ocurrió un error vuelve a intentarlo",
                },
                "msg": "fail",
            }, 500

    @swag_from(f"{DOCS_PATH_STORAGE}/create_document.yml")
    def post(self):
        try:
            cmd = commands.ADDFileType.Schema().load(request.json)  # type: ignore
            logger.info("ADDFileType Resource: command %s", cmd)
            response = broker.handle(cmd)
            return {
                "code": "STO201",
                "data": response,
                "msg": "success",
            }, 201
        except Exception as e:  # pragma: no cover
            logger.error("Error en registrar documento %s:", str(e))
            return {
                "code": "STO400",
                "error": {"msg_error": str(e)},
                "msg": "fail",
            }, 500


storage_blueprint = Blueprint(
    "storage",
    __name__,
    url_prefix="/storage",
)


storage_api = Api(storage_blueprint)

storage_api.add_resource(StorageUrlResource, "/get_url")
storage_api.add_resource(StorageResource, "")
storage_api.add_resource(DocumentTypeResource, "/document_type")
storage_api.add_resource(FileTypeResource, "/filetype")
