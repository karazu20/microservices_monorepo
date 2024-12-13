import abc
from typing import Tuple


class FileService(abc.ABC):
    file_extension: str = NotImplemented

    @abc.abstractmethod
    def get_file_name(self, *args, **kwargs) -> str:  # type: ignore
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, *args, **kwargs) -> Tuple[str, bool]:  # type: ignore
        raise NotImplementedError


class FakeFileService(FileService):
    file_extension: str = "mock"
    saved = False

    def get_file_name(self, *args, **kwargs) -> str:
        return "MOCKFILE." + self.file_extension

    def save(self, *args, **kwargs) -> Tuple[str, bool]:
        self.saved = True
        return "MOCKFILE.mock", True
