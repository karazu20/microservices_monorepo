import logging
from typing import Tuple

from src.cdc.adapters.file_service import FileService
from src.cdc.config import PATH_XML

logger = logging.getLogger(__name__)


class CDCXmlService(FileService):
    file_extension = "xml"

    def get_file_name(self, folio: str, is_success: bool) -> str:  # type: ignore
        path = "fail"
        if is_success:
            path = "success"
        return "{}/{}.{}".format(path, folio, self.file_extension)

    def save(self, folio: str, xml_response: str, is_success: bool) -> Tuple[str, bool]:  # type: ignore
        try:
            logger.info("Se almacena XML del folio: %s", folio)
            filename = self.get_file_name(folio, is_success)
            xml = open(PATH_XML + filename, "w")
            xml.write(xml_response)
            xml.close()
            return filename, True
        except Exception as ex:
            logger.error("Error al guardar xml del folio: %s %s", folio, str(ex))
            return "", False
