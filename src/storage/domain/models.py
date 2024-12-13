from __future__ import annotations  # type: ignore

import base64
from dataclasses import dataclass, field
from datetime import datetime
from mimetypes import guess_extension

from setup.domain import Model
from src.storage.config import PATH_S3


@dataclass
class FileType(Model):
    id: int = field(init=False)
    tipo: str = ""


@dataclass
class DocumentType(Model):
    id: int = field(init=False)
    tipo: str = ""
    descripcion: str = ""


@dataclass
class Document(Model):
    id: int = field(init=False)
    tipo_documento_id: int = field(init=False)
    tipo_archivo_id: int = field(init=False)
    storage_id: str = ""
    podemos_id: str = ""
    comentario: str = ""
    tipo_entidad: str = ""

    def save_file(
        self, file: str, filetype: FileType, document_type: DocumentType
    ) -> str:
        doc_decode = base64.b64decode(file, validate=True)
        extention = guess_extension(filetype.tipo)

        self.storage_id = self.key_id(
            document_type=document_type, extention=extention  # type: ignore
        )
        path_file = PATH_S3 + self.storage_id + extention  # type: ignore
        file = open(path_file, "wb")  # type: ignore
        file.write(doc_decode)  # type: ignore
        file.close()  # type: ignore

        return path_file

    def key_id(self, document_type: DocumentType, extention: str) -> str:
        return (
            self.podemos_id
            + datetime.now().strftime("%Y%m%d%H%I%s")
            + document_type.tipo.lower()
            + extention
        )
