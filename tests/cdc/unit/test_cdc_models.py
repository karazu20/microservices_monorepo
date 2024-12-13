from datetime import datetime

import pytest
from freezegun import freeze_time

from src.cdc.config import FOLIO_LEN_ID_EMPLEADO, FOLIO_LEN_TRIBU
from src.cdc.domain.models import (
    CentroComunitario,
    ConsultaCdc,
    DireccionProspecto,
    Nip,
    Person,
    Prospecto,
    QueryCdc,
    QueryStatus,
    StatusConsultaCdC,
    Usuario,
)
from src.cdc.errors import CdcDomainError


def test_query_cdc():
    model_person = Person(
        "Andres", "Prueba", "Prueba 2", "TOGM920527HDFRNR06", "TOGM920527CI8", "MX"  # type: ignore
    )
    model = QueryCdc("archivo_prueba.xml", "CentroComunitario")
    model_person.add_query_cdc(model)
    assert model.id is None
    assert model.archivo_xml == "archivo_prueba.xml"
    assert model.centro_comunitario == "CentroComunitario"


def test_query_status():
    model = QueryStatus("PENDIENTE")
    assert model.id is None
    assert model.status == "PENDIENTE"


def test_add_direccion_prospecto():
    prospecto = Prospecto(
        "JABB810826MDFVRT01",
        "BEATRIZ",
        "LETICIA",
        "JAVIER",
        "BARRIOS",
        datetime(1981, 8, 26),
        "MEXICANA",
        "1111111111",
    )

    direccion_cero = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    direccion_uno = DireccionProspecto(
        "Cda Polvora",
        "C",
        "81",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )

    assert prospecto._direcciones == []

    prospecto.add_direccion(direccion_cero)
    assert prospecto._direcciones[0].calle == "Diagonal 2"
    assert len(prospecto._direcciones) == 1

    prospecto.add_direccion(direccion_cero)
    assert len(prospecto._direcciones) == 1

    prospecto.add_direccion(direccion_uno)
    assert prospecto._direcciones[1].calle == "Cda Polvora"
    assert len(prospecto._direcciones) == 2

    prospecto.add_direccion(direccion_cero)
    assert prospecto._direcciones[2].calle == "Diagonal 2"
    assert len(prospecto._direcciones) == 3


def test_get_direccion_prospecto():
    prospecto = Prospecto(
        "JABB810826MDFVRT01",
        "BEATRIZ",
        "LETICIA",
        "JAVIER",
        "BARRIOS",
        datetime(1981, 8, 26),
        "MEXICANA",
        "1111111111",
    )

    direccion_cero = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    direccion_uno = DireccionProspecto(
        "Cda Polvora",
        "C",
        "81",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )

    assert prospecto._direcciones == []
    prospecto.add_direccion(direccion_cero)
    prospecto.add_direccion(direccion_uno)
    assert len(prospecto._direcciones) == 2

    direcciones_prospecto = prospecto.get_direcciones()

    assert len(direcciones_prospecto) == len(prospecto._direcciones)
    assert direcciones_prospecto[0].calle == "Diagonal 2"
    assert direcciones_prospecto[0].numero_exterior == "#16"
    assert direcciones_prospecto[0].colonia == "San Fernando"
    assert direcciones_prospecto[0].ciudad == "Huixquilucan de Degollado"
    assert direcciones_prospecto[0].estado == "Mexico"
    assert direcciones_prospecto[0].pais == "Mexico"
    assert direcciones_prospecto[0].CP == "52765"
    assert direcciones_prospecto[1].calle == "Cda Polvora"
    assert direcciones_prospecto[1].numero_exterior == "C"
    assert direcciones_prospecto[1].numero_interior == "81"


def test_add_consulta_prospecto():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion_cero = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    direccion_uno = DireccionProspecto(
        "Cda Polvora",
        "C",
        "81",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion_cero)
    prospecto.add_direccion(direccion_uno)
    direcciones_prospecto = prospecto.get_direcciones()
    nip_prospecto = Nip("nip1", "AACN731113MMCLJR09")
    estatus_prospecto = StatusConsultaCdC("estuatus1")
    usuario_prospecto = Usuario("usuario1")
    centro_comunitario = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "folio001",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_prospecto,
        estatus_prospecto,
        usuario_prospecto,
        centro_comunitario,
    )

    assert prospecto._consultas == []
    prospecto.add_consulta_prospecto(consulta)

    assert prospecto.curp == "MAVK030710MDFRRRA3"
    assert len(prospecto._consultas) == 1
    assert prospecto._consultas[0].cdc_folio == "folioCdc1"
    assert prospecto._consultas[0].folio == "folio001"
    assert prospecto._consultas[0].consulta_cdc_tipo == "consulta cdc tipo 1"
    assert prospecto._consultas[0].fallo_regla == "fallo 1"
    assert prospecto._consultas[0].es_referido == False
    assert prospecto._consultas[0]._direccion.CP == "52765"
    assert prospecto._consultas[0]._nip.nip == "nip1"
    assert prospecto._consultas[0]._estatus.status == "estuatus1"
    assert prospecto._consultas[0]._usuario.username == "usuario1"
    assert prospecto._consultas[0]._centro_comunitario.name == "CCNZ"


def test_get_consulta_prospecto():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion_cero = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    direccion_uno = DireccionProspecto(
        "Cda Polvora",
        "C",
        "81",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion_cero)
    prospecto.add_direccion(direccion_uno)
    direcciones_prospecto = prospecto.get_direcciones()
    nip_uno = Nip("nip1", "AACN731113MMCLJR09")
    estatus_uno = StatusConsultaCdC("estuatus1")
    usuario_uno = Usuario("usuario1")
    centro_uno = CentroComunitario("CCNZ")
    consulta_uno = ConsultaCdc(
        "folioCdc1",
        "folio001",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_uno,
        estatus_uno,
        usuario_uno,
        centro_uno,
    )

    assert prospecto.curp == "MAVK030710MDFRRRA3"
    assert prospecto._consultas == []
    prospecto.add_consulta_prospecto(consulta_uno)
    assert len(prospecto._consultas) == 1

    nip_dos = Nip("nip7", "AACN731113MMCLJR09")
    estatus_dos = StatusConsultaCdC("estuatus7")
    usuario_dos = Usuario("usuario7")
    centro_dos = CentroComunitario("CCNZ")
    consulta_dos = ConsultaCdc(
        "folioCdc2",
        "folio002",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 7",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_dos,
        estatus_dos,
        usuario_dos,
        centro_dos,
    )

    prospecto.add_consulta_prospecto(consulta_dos)
    assert len(prospecto._consultas) == 2

    consultas_totales = prospecto.get_consultas()
    assert len(consultas_totales) == len(prospecto._consultas)


def test_update_consulta_prospecto():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion_cero = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    direccion_uno = DireccionProspecto(
        "Cda Polvora",
        "C",
        "81",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion_cero)
    prospecto.add_direccion(direccion_uno)
    direcciones_prospecto = prospecto.get_direcciones()

    nip_uno = Nip("nip1", "AACN731113MMCLJR09")
    estatus_uno = StatusConsultaCdC("estuatus1")
    usuario_uno = Usuario("usuario1")
    centro_uno = CentroComunitario("CCNZ")
    consulta_uno = ConsultaCdc(
        "folioCdc1",
        "folio001",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_uno,
        estatus_uno,
        usuario_uno,
        centro_uno,
    )

    nip_dos = Nip("nip7", "AACN731113MMCLJR09")
    estatus_dos = StatusConsultaCdC("estuatus2")
    usuario_dos = Usuario("usuario2")
    centro_dos = CentroComunitario("CCNZ")
    consulta_dos = ConsultaCdc(
        "folioCdc2",
        "folio002",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 2",
        "fallo 2",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_dos,
        estatus_dos,
        usuario_dos,
        centro_dos,
    )

    nip_tres = Nip("nip7", "AACN731113MMCLJR09")
    estatus_tres = StatusConsultaCdC("estuatus3")
    usuario_tres = Usuario("usuario3")
    centro_tres = CentroComunitario("CCNZ")
    consulta_tres = ConsultaCdc(
        "folioCdc3",
        "folio003",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 3",
        "fallo 3",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_tres,
        estatus_tres,
        usuario_tres,
        centro_tres,
    )

    nip_cuatro = Nip("nip7", "AACN731113MMCLJR09")
    estatus_cuatro = StatusConsultaCdC("estuatus4")
    usuario_cuatro = Usuario("usuario4")
    centro_cuatro = CentroComunitario("CCNZ")
    consulta_cuatro = ConsultaCdc(
        "folioCdc4",
        "folio004",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 4",
        "fallo 4",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip_cuatro,
        estatus_cuatro,
        usuario_cuatro,
        centro_cuatro,
    )

    assert prospecto.curp == "MAVK030710MDFRRRA3"
    assert prospecto._consultas == []
    prospecto.add_consulta_prospecto(consulta_uno)
    prospecto.add_consulta_prospecto(consulta_dos)
    prospecto.add_consulta_prospecto(consulta_tres)
    assert prospecto._consultas[0].cdc_folio == "folioCdc1"
    assert prospecto._consultas[0].fallo_regla == "fallo 1"
    assert prospecto._consultas[0]._estatus.status == "estuatus1"
    assert len(prospecto._consultas) == 3

    estatus_dos = StatusConsultaCdC("PENDIENTE")
    prospecto._update_consulta(consulta_uno, "folioCdc2", "fallo 2", estatus_dos)

    assert prospecto._consultas[0].cdc_folio == "folioCdc2"
    assert prospecto._consultas[0].fallo_regla == "fallo 2"
    assert prospecto._consultas[0]._estatus.status == "PENDIENTE"
    assert len(prospecto._consultas) == 3

    with pytest.raises(
        CdcDomainError,
        match="Error la consulta que se intenta actualizar no existe.",
    ):
        prospecto._update_consulta(consulta_cuatro, "folioCdc3", "fallo 3", estatus_dos)


@freeze_time("2023-03-07")
def test_generate_folio_uno():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    tribu = "TribuAZ-2".rjust(FOLIO_LEN_TRIBU, "0").replace("Tribu", "").replace("-", "")
    folio_generate = prospecto.generate_folio(consultas[0], [], num_empleado, tribu)

    assert folio_generate == "00AZ2PPP42983230307001"
    assert prospecto._consultas[0].folio == folio_generate


@freeze_time("2023-03-07")
def test_generate_folio_consecutivo():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    tribu = "TribuAZ-2".rjust(FOLIO_LEN_TRIBU, "0").replace("Tribu", "").replace("-", "")
    folio_generate = prospecto.generate_folio(
        consultas[0],
        ["00AZ2PPP42983230306001", "00AZ2PPP42983230306002"],
        num_empleado,
        tribu,
    )

    assert folio_generate == "00AZ2PPP42983230307003"
    assert prospecto._consultas[0].folio == folio_generate


@freeze_time("2023-03-07")
def test_generate_folio_no_tribu():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    folio_generate = prospecto.generate_folio(consultas[0], [], num_empleado, "")

    assert folio_generate == "000000PPPPP42983230307001"
    assert prospecto._consultas[0].folio == folio_generate


@freeze_time("2023-03-07")
def test_generate_folio_no_tribu_consecutivo():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    folio_generate = prospecto.generate_folio(
        consultas[0], ["000000PPPPP42983230306001"], num_empleado, ""
    )

    assert folio_generate == "000000PPPPP42983230307002"
    assert prospecto._consultas[0].folio == folio_generate


@freeze_time("2023-03-07")
def test_generate_folio_folios_mixtos():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    tribu = "TribuAZ-2".rjust(FOLIO_LEN_TRIBU, "0").replace("Tribu", "").replace("-", "")
    folio_generate = prospecto.generate_folio(
        consultas[0],
        ["00AZ2PPP42983230306009", "000000PPPPP42983230306001"],
        num_empleado,
        tribu,
    )

    assert folio_generate == "00AZ2PPP42983230307010"
    assert prospecto._consultas[0].folio == folio_generate


@freeze_time("2023-03-07")
def test_generate_folio_folios_mixtos_sin_tribu():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    folio_generate = prospecto.generate_folio(
        consultas[0],
        ["00AZ1PPP42983230306009", "000000PPPPP42983230306001"],
        num_empleado,
        "",
    )

    assert folio_generate == "000000PPPPP42983230307002"
    assert prospecto._consultas[0].folio == folio_generate


@freeze_time("2023-03-07")
def test_generate_folio_folios_mixtos_diferentes_tribus():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )
    prospecto.add_consulta_prospecto(consulta)
    consultas = prospecto.get_consultas()

    assert prospecto._consultas[0].folio == ""

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    tribu = "TribuAZ-2".rjust(FOLIO_LEN_TRIBU, "0").replace("Tribu", "").replace("-", "")
    folio_generate = prospecto.generate_folio(
        consultas[0],
        ["00AZ1PPP42983230306009", "00AZ2PPP42983230306003", "000000PPPPP42983230306001"],
        num_empleado,
        tribu,
    )

    assert folio_generate == "00AZ2PPP42983230307004"
    assert prospecto._consultas[0].folio == folio_generate


def test_generate_folio_la_consulta_no_pertenece_a_la_prospecto():
    prospecto = Prospecto(
        "MAVK030710MDFRRRA3",
        "KARLA",
        "RUBY",
        "MARQUEZ",
        "VERA",
        datetime(2003, 7, 10),
        "MEXICANA",
        "1111111111",
    )
    direccion = DireccionProspecto(
        "Diagonal 2",
        "#16",
        "",
        "San Fernando",
        "Huixquilucan de Degollado",
        "Mexico",
        "Mexico",
        "52765",
    )
    prospecto.add_direccion(direccion)
    direcciones_prospecto = prospecto.get_direcciones()

    nip = Nip("nip1", "AACN731113MMCLJR09")
    estatus = StatusConsultaCdC("estuatus1")
    usuario = Usuario("usuario1")
    centro = CentroComunitario("CCNZ")
    consulta = ConsultaCdc(
        "folioCdc1",
        "",
        datetime.now(),
        datetime.now(),
        datetime.now(),
        "consulta cdc tipo 1",
        "fallo 1",
        False,
        prospecto,
        direcciones_prospecto[0],
        nip,
        estatus,
        usuario,
        centro,
    )

    num_empleado = "42983".rjust(FOLIO_LEN_ID_EMPLEADO, "P")
    tribu = "TribuAZ-2".rjust(FOLIO_LEN_TRIBU, "0").replace("Tribu", "").replace("-", "")

    with pytest.raises(
        CdcDomainError,
        match="Error la consulta a la que intentas asignar folio, no existe dentro de las consultas de la Prospecto.",
    ):
        prospecto.generate_folio(consulta, [], num_empleado, tribu)
