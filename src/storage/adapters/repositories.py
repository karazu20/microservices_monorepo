from setup.adapters.data import SQLRepository
from src.storage.domain.models import Document, DocumentType, FileType


class DocumentRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Document)  # type: ignore
        self.document = Document

    def _get(self, storage_id) -> Document:
        return (
            self.session.query(self.document)
            .filter(self.document.storage_id == storage_id)
            .first()
        )

    def get_filetype(self, tipo) -> FileType:
        return self.session.query(FileType).filter(FileType.tipo == tipo).first()

    def get_document_type(self, id) -> DocumentType:
        return self.session.query(DocumentType).filter(DocumentType.id == id).first()

    def list_filetype(self) -> FileType:
        return self.session.query(FileType).all()

    def list_document_type(self) -> DocumentType:
        return self.session.query(DocumentType).all()
