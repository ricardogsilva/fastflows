import abc
import typing
from pathlib import Path

import pydantic
from loguru import logger

from ...schemas.prefect.flow_data import FlowDataFromFile
from .reader import FlowFileReader


class FlowsStorageBase(abc.ABC):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    # TODO: this ought to be async
    @abc.abstractmethod
    def list(self):
        ...

    # TODO: this ought to be async
    @abc.abstractmethod
    def read(self):
        ...


class LocalStorage(FlowsStorageBase):
    def __init__(self, storage_path: str):
        super().__init__(storage_path)
        self.storage_path = Path(self.storage_path)

    def old_list(self):
        if not self.storage_path.is_dir():
            raise ValueError(
                f"Flows Home must be a folder. You provided: {self.storage_path}"
            )
        return list(self.storage_path.iterdir())

    def list(self) -> typing.Iterable[FlowDataFromFile]:
        for file_path in (p for p in self.storage_path.iterdir() if p.is_file()):
            logger.debug(f"processing: {file_path}...")
            contents = file_path.read_text()
            if contents != "":
                try:
                    read = FlowFileReader(flow_data=contents)
                    for flow_definition in read.flows:
                        yield flow_definition
                except NotADirectoryError:
                    logger.exception("Invalid storage path: {!r}", self.storage_path)
                except pydantic.ValidationError:
                    logger.exception("Could not validate file {}", file_path)
                except AttributeError:
                    logger.exception("Could not parse file {}", file_path)

    def read(self):
        pass
