from src.storage.domain.commands import ADDDocumentType, ADDFileType


def test_add_file():
    cmd = ADDFileType("application/pdf")
    assert cmd.tipo == "application/pdf"

    cmd = ADDDocumentType("INE", "Documento Oficial")
    assert cmd.tipo == "INE"
    assert cmd.descripcion == "Documento Oficial"
