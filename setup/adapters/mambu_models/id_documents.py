from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING

from mambupy.api.vos import MambuIDDocument

from setup.adapters.mambu_models.model import Mode, VOMambu

if TYPE_CHECKING:
    from setup.adapters.mambu_models import Documents


@dataclass(repr=False)
class IDDocuments(VOMambu):
    _model_rest = MambuIDDocument

    def __init__(self, instance_mambu=None, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields(IDDocuments), mode, **kwargs)

    client_key: str = field(
        metadata={"mambu_source": "clientKey", "read_only": False, "is_required": False}
    )
    document_type: str = field(
        metadata={
            "mambu_source": "documentType",
            "read_only": False,
            "is_required": False,
        }
    )
    document_id: str = field(
        metadata={"mambu_source": "documentId", "read_only": False, "is_required": False}
    )
    issuing_authority: str = field(
        metadata={
            "mambu_source": "issuingAuthority",
            "read_only": False,
            "is_required": False,
        }
    )
    index_in_list: int = field(
        metadata={"mambu_source": "indexInList", "read_only": False, "is_required": False}
    )
    identification_document_template_key: str = field(
        metadata={
            "mambu_source": "identificationDocumentTemplateKey",
            "read_only": False,
            "is_required": False,
        }
    )
    attachments: list[Documents] = field(
        metadata={
            "mambu_source": "attachments",
            "is_vo": True,
            "is_many": True,
            "read_only": False,
            "is_required": False,
            "model": "Documents",
        }
    )
