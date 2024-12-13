from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
from typing import Any, List

from setup.domain import Model


@dataclass
class Estado(Model):
    id: int = field(init=False)
    nombre: str = ""
    _municipios: List[Any] = field(default_factory=list, init=False)

    def add_municipio(self, municipio: Municipio):
        self._municipios.append(municipio)

    def get_municipios(self):
        return self._municipios


@dataclass
class Municipio(Model):
    id: int = field(init=False)
    nombre: str = ""
    _colonias: List[Any] = field(default_factory=list, init=False)
    id_estado: int = field(init=False)

    def add_colonia(self, colonia: Colonia):
        self._colonias.append(colonia)

    def get_colonias(self):
        return self._colonias


@dataclass
class Colonia(Model):
    id: int = field(init=False)
    nombre: str = ""
    ciudad: str = ""
    asentamiento: str = ""
    codigo_postal: str = ""
    id_municipio: int = field(init=False)
