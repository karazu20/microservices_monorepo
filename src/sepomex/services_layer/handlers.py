from __future__ import annotations  # type: ignore

import logging
from dataclasses import asdict

from setup import domain  # type: ignore
from setup.adapters import bus
from setup.domain import events
from shared.decorators import introspect_cache
from src.sepomex.domain import commands, models, queries
from src.sepomex.services_layer import unit_of_work

from typing import Callable, Dict, Type  # isort:skip


logger = logging.getLogger(__name__)


def add_colonia(
    command: commands.ADDColonia,
    uow: unit_of_work.UnitOfWorkSepomex,
    bus: bus.AbstractBus,
) -> None:
    with uow:
        colonia = models.Colonia(
            command.nombre, command.ciudad, command.asentamiento, command.codigo_postal
        )
        municipio = uow.municipios.get(command.municipio)
        municipio.add_colonia(colonia)
        uow.commit()
        event = events.CompletedColonia(nombre=colonia.nombre)
        bus.publish(event)


def add_municipio(
    command: commands.ADDMunicipio,
    uow: unit_of_work.UnitOfWorkSepomex,
) -> None:
    with uow:
        municipio = models.Municipio(command.nombre)
        estado = uow.estados.get(command.estado)
        estado.add_municipio(municipio)
        uow.commit()


def add_estado(
    command: commands.ADDEstado,
    uow: unit_of_work.UnitOfWorkSepomex,
) -> None:
    with uow:
        estado = models.Estado(command.nombre)
        uow.estados.add(estado)
        uow.commit()


@introspect_cache
def get_colonias_from_cp(
    query: queries.GetDataFromCP,
    uow: unit_of_work.UnitOfWorkSepomex,
) -> Dict:
    with uow:
        colonias = uow.view_postal_code.search(query)
        return {
            "colonias": [row[0] for row in colonias],
            "codigo_postal": colonias[0][1],
            "municipio": colonias[0][2],
            "estado": colonias[0][3],
        }


def get_colonias(
    query: queries.GetColonias,
    uow: unit_of_work.UnitOfWorkSepomex,
) -> list:
    with uow:
        municipio = uow.municipios.get(query.municipio)
        colonias = municipio.get_colonias()
        return [asdict(col) for col in colonias]


def get_municipios(
    query: queries.GetMunicipios,
    uow: unit_of_work.UnitOfWorkSepomex,
) -> list:
    with uow:
        estado = uow.estados.get(query.estado)
        municipios = estado.get_municipios()
        return [{"nombre": mun.nombre} for mun in municipios]


def get_estados(
    query: queries.GetEstados,
    uow: unit_of_work.UnitOfWorkSepomex,
) -> list:
    with uow:
        estados = uow.estados.list()
        return [{"nombre": est.nombre} for est in estados]


def notify_sepomex(
    event: events.CompletedColonia,
):
    logger.info("Evento externo, se inserto una nueva colonia a la BD %s", event.nombre)
    return True


QUERY_HANDLERS = {
    queries.GetDataFromCP: get_colonias_from_cp,
    queries.GetEstados: get_estados,
    queries.GetMunicipios: get_municipios,
    queries.GetColonias: get_colonias,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {
    commands.ADDColonia: add_colonia,
    commands.ADDMunicipio: add_municipio,
    commands.ADDEstado: add_estado,
}  # type: Dict[Type[domain.Command], Callable]


EVENT_HANDLERS = {
    events.CompletedColonia: notify_sepomex,
}  # type: Dict[Type[domain.Event], Callable]
