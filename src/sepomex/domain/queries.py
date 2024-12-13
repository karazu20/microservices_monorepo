from dataclasses import field

from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetDataFromCP(Query):
    codigo_postal: str = field(metadata={"required": True})


@dataclass
class GetEstados(Query):
    pass


@dataclass
class GetMunicipios(Query):
    estado: str = field(metadata={"required": True})


@dataclass
class GetColonias(Query):
    municipio: str = field(metadata={"required": True})
