import logging
from dataclasses import dataclass, field, fields
from typing import Any, List, Optional

from shared.utils import get_full_name, xml_to_dict

logger = logging.getLogger(__name__)


@dataclass
class BaseCDCResponse:
    def __init__(self, **kwargs):
        names = set([f.metadata.get("cdc_source") for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                item = [
                    f.name for f in fields(self) if k == f.metadata.get("cdc_source")
                ][0]
                setattr(self, item, v)


@dataclass
class DescriptionErrorData(BaseCDCResponse):
    descripcion_error: Optional[List[str]] = field(
        default=None, metadata={"cdc_source": "DescripcionError"}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class ErrorData(BaseCDCResponse):
    clave_otorgante: Optional[str] = field(
        default="", metadata={"cdc_source": "ClaveOtorgante"}
    )
    folio_consulta_otorgante: Optional[str] = field(
        default="", metadata={"cdc_source": "FolioConsultaOtorgante"}
    )
    producto_requerido: Optional[str] = field(
        default="", metadata={"cdc_source": "ProductoRequerido"}
    )
    errores: Optional[DescriptionErrorData] = field(
        default=None, metadata={"cdc_source": "Errores"}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.errores is not None:
            self.errores = DescriptionErrorData(**self.errores)  # type: ignore


@dataclass
class EncabezadoData(BaseCDCResponse):
    folio_consulta_otorgante: str = field(
        default="", metadata={"cdc_source": "FolioConsultaOtorgante"}
    )
    clave_otorgante: str = field(default="", metadata={"cdc_source": "ClaveOtorgante"})
    expediente_encontrado: str = field(
        default="", metadata={"cdc_source": "ExpedienteEncontrado"}
    )
    folio_consulta: str = field(default="", metadata={"cdc_source": "FolioConsulta"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class DomicilioData(BaseCDCResponse):
    direccion: str = field(default="", metadata={"cdc_source": "Direccion"})
    colonia_poblacion: str = field(
        default="", metadata={"cdc_source": "ColoniaPoblacion"}
    )
    delegacion_municipio: str = field(
        default="", metadata={"cdc_source": "DelegacionMunicipio"}
    )
    ciudad: str = field(default="", metadata={"cdc_source": "Ciudad"})
    estado: str = field(default="", metadata={"cdc_source": "Estado"})
    cp: str = field(default="", metadata={"cdc_source": "CP"})
    fecha_residencia: str = field(default="", metadata={"cdc_source": "FechaResidencia"})
    numero_telefono: str = field(default="", metadata={"cdc_source": "NumeroTelefono"})
    tipo_domicilio: str = field(default="", metadata={"cdc_source": "TipoDomicilio"})
    tipo_asentamiento: str = field(
        default="", metadata={"cdc_source": "TipoAsentamiento"}
    )
    fecha_registro_domicilio: str = field(
        default="", metadata={"cdc_source": "FechaRegistroDomicilio"}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class NombreData(BaseCDCResponse):
    apellido_paterno: str = field(default="", metadata={"cdc_source": "ApellidoPaterno"})
    apellido_materno: str = field(default="", metadata={"cdc_source": "ApellidoMaterno"})
    apellido_adicional: str = field(
        default="", metadata={"cdc_source": "ApellidoAdicional"}
    )
    nombres: str = field(default="", metadata={"cdc_source": "Nombres"})
    fecha_nacimiento: str = field(default="", metadata={"cdc_source": "FechaNacimiento"})
    rfc: str = field(default="", metadata={"cdc_source": "RFC"})
    curp: str = field(default="", metadata={"cdc_source": "CURP"})
    nacionalidad: str = field(default="", metadata={"cdc_source": "Nacionalidad"})
    residencia: str = field(default="", metadata={"cdc_source": "Residencia"})
    estado_civil: str = field(default="", metadata={"cdc_source": "EstadoCivil"})
    sexo: str = field(default="", metadata={"cdc_source": "Sexo"})
    clave_elector_ife: str = field(default="", metadata={"cdc_source": "ClaveElectorIFE"})
    numero_dependientes: str = field(
        default="", metadata={"cdc_source": "NumeroDependientes"}
    )
    fecha_defuncion: str = field(default="", metadata={"cdc_source": "FechaDefuncion"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def full_name(self):
        return get_full_name(self.nombres, self.apellido_paterno, self.apellido_materno)


@dataclass
class CuentaData(BaseCDCResponse):
    fecha_actualizacion: str = field(
        default="", metadata={"cdc_source": "FechaActualizacion"}
    )
    registro_impugnado: str = field(
        default="", metadata={"cdc_source": "RegistroImpugnado"}
    )
    clave_otorgante: str = field(default="", metadata={"cdc_source": "ClaveOtorgante"})
    nombre_otorgante: str = field(default="", metadata={"cdc_source": "NombreOtorgante"})
    cuenta_actual: str = field(default="", metadata={"cdc_source": "CuentaActual"})
    tipo_responsabilidad: str = field(
        default="", metadata={"cdc_source": "TipoResponsabilidad"}
    )
    tipo_cuenta: str = field(default="", metadata={"cdc_source": "TipoCuenta"})
    tipo_credito: str = field(default="", metadata={"cdc_source": "TipoCredito"})
    clave_unidad_monetaria: str = field(
        default="", metadata={"cdc_source": "ClaveUnidadMonetaria"}
    )
    valor_activo_valuacion: str = field(
        default="", metadata={"cdc_source": "ValorActivoValuacion"}
    )
    numero_pagos: str = field(default="", metadata={"cdc_source": "NumeroPagos"})
    frecuencia_pagos: str = field(default="", metadata={"cdc_source": "FrecuenciaPagos"})
    monto_pagar: str = field(default="", metadata={"cdc_source": "MontoPagar"})
    fecha_apertura_cuenta: str = field(
        default="", metadata={"cdc_source": "FechaAperturaCuenta"}
    )
    fecha_ultimo_pago: str = field(default="", metadata={"cdc_source": "FechaUltimoPago"})
    fecha_ultima_compra: str = field(
        default="", metadata={"cdc_source": "FechaUltimaCompra"}
    )
    fecha_cierre_cuenta: str = field(
        default="", metadata={"cdc_source": "FechaCierreCuenta"}
    )
    fecha_reporte: str = field(default="", metadata={"cdc_source": "FechaReporte"})
    ultima_fecha_saldo_cero: str = field(
        default="", metadata={"cdc_source": "UltimaFechaSaldoCero"}
    )
    garantia: str = field(default="", metadata={"cdc_source": "Garantia"})
    credito_maximo: str = field(default="", metadata={"cdc_source": "CreditoMaximo"})
    saldo_actual: str = field(default="", metadata={"cdc_source": "SaldoActual"})
    limite_credito: str = field(default="", metadata={"cdc_source": "LimiteCredito"})
    saldo_vencido: str = field(default="", metadata={"cdc_source": "SaldoVencido"})
    numero_pagos_vencidos: str = field(
        default="", metadata={"cdc_source": "NumeroPagosVencidos"}
    )
    pago_actual: str = field(default="", metadata={"cdc_source": "PagoActual"})
    historico_pagos: str = field(default="", metadata={"cdc_source": "HistoricoPagos"})
    fecha_reciente_historico_pagos: str = field(
        default="", metadata={"cdc_source": "FechaRecienteHistoricoPagos"}
    )
    fecha_antigua_historico_pagos: str = field(
        default="", metadata={"cdc_source": "FechaAntiguaHistoricoPagos"}
    )
    clave_prevencion: str = field(default="", metadata={"cdc_source": "ClavePrevencion"})
    total_pagos_reportados: str = field(
        default="", metadata={"cdc_source": "TotalPagosReportados"}
    )
    peor_atraso: str = field(default="", metadata={"cdc_source": "PeorAtraso"})
    fecha_peor_atraso: str = field(default="", metadata={"cdc_source": "FechaPeorAtraso"})
    saldo_vencido_peor_atraso: str = field(
        default="", metadata={"cdc_source": "SaldoVencidoPeorAtraso"}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class ConsultaEfectuadaData(BaseCDCResponse):
    fecha_consulta: str = field(default="", metadata={"cdc_source": "FechaConsulta"})
    clave_otorgante: str = field(default="", metadata={"cdc_source": "ClaveOtorgante"})
    nombre_otorgante: str = field(default="", metadata={"cdc_source": "NombreOtorgante"})
    telefono_otorgante: str = field(
        default="", metadata={"cdc_source": "TelefonoOtorgante"}
    )
    tipo_credito: str = field(default="", metadata={"cdc_source": "TipoCredito"})
    clave_unidad_monetaria: str = field(
        default="", metadata={"cdc_source": "ClaveUnidadMonetaria"}
    )
    importe_credito: str = field(default="", metadata={"cdc_source": "ImporteCredito"})
    tipo_responsabilidad: str = field(
        default="", metadata={"cdc_source": "TipoResponsabilidad"}
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class CDCResponse(BaseCDCResponse):
    encabezado: Optional[EncabezadoData] = field(
        default=None, metadata={"cdc_source": "Encabezado"}
    )
    nombre: Optional[NombreData] = field(default=None, metadata={"cdc_source": "Nombre"})
    domicilios: Optional[List[DomicilioData]] = field(
        default=None, metadata={"cdc_source": "Domicilios"}
    )
    cuentas: Optional[List[CuentaData]] = field(
        default=None, metadata={"cdc_source": "Cuentas"}
    )
    consultas_efectuadas: Optional[List[ConsultaEfectuadaData]] = field(
        default=None, metadata={"cdc_source": "ConsultasEfectuadas"}
    )
    error: Optional[ErrorData] = field(default=None, metadata={"cdc_source": "Error"})
    xml_response: str = field(default="")

    def _set_list(self, lista: Optional[List[Any]], key: str, clazz: Any) -> list:
        if lista is not None:
            tmp_list = lista[key]  # type: ignore
            if isinstance(tmp_list, list):
                lista = [clazz(**it) for it in tmp_list]  # type: ignore
            else:
                lista = [clazz(**tmp_list)]  # type: ignore
        else:  # pragma: no cover
            lista = []
        return lista

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.encabezado is not None:
            self.encabezado = EncabezadoData(**self.encabezado)  # type: ignore
        if self.nombre is not None:
            self.nombre = NombreData(**self.nombre)  # type: ignore

        self.domicilios = self._set_list(
            lista=self.domicilios, key="Domicilio", clazz=DomicilioData
        )
        self.cuentas = self._set_list(lista=self.cuentas, key="Cuenta", clazz=CuentaData)
        self.consultas_efectuadas = self._set_list(
            lista=self.consultas_efectuadas,
            key="ConsultaEfectuada",
            clazz=ConsultaEfectuadaData,
        )

        if self.error is not None:
            self.error = ErrorData(**self.error)  # type: ignore

    @classmethod
    def _exclude_keys(
        cls, cuentas: List[CuentaData], claves_permitidas: List[str]
    ) -> List[CuentaData]:
        list_cuenta = []
        for cta in cuentas:
            if not (
                cta.fecha_cierre_cuenta
                and not (cta.clave_prevencion in claves_permitidas)
            ):
                list_cuenta.append(cta)
        return list_cuenta

    @classmethod
    def from_response(cls, response: str, claves_permitidas: List[str], exclude=True):  # type: ignore
        xml_dict = xml_to_dict(response)
        try:
            this_data = xml_dict["Respuesta"]["Personas"]["Persona"]
        except KeyError:
            this_data = xml_dict
        except Exception as ex:  # pragma: no cover
            this_data = {}
            logger.error("XML response: %s", str(xml_dict))
            logger.error("Error: %s", str(ex))

        cls.xml_response = response
        _instance = cls(**this_data)
        if exclude:
            _instance.cuentas = cls._exclude_keys(_instance.cuentas, claves_permitidas)  # type: ignore

        return _instance
