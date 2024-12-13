from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from setup.domain import Model


@dataclass
class LoanStatus(Model):
    PENDIENTE_VALIDACION = "PENDIENTE_VALIDACION"
    VALIDADO = "VALIDADO"
    PENDIENTE_APROBACION = "PENDIENTE_APROBACION"
    APROBADO = "APROBADO"
    PENDIENTE_DESEMBOLSO = "PENDIENTE_DESEMBOLSO"
    DESEMBOLSADO = "DESEMBOLSADO"
    ACTIVO = "ACTIVO"
    CANCELADO = "CANCELADO"
    RECHAZADO = "RECHAZADO"
    INCIDENCIAS = "INCIDENCIAS"

    ALL_STATUS = (
        PENDIENTE_VALIDACION,
        VALIDADO,
        PENDIENTE_APROBACION,
        APROBADO,
        PENDIENTE_DESEMBOLSO,
        DESEMBOLSADO,
        ACTIVO,
        CANCELADO,
        RECHAZADO,
        INCIDENCIAS,
    )

    id: int = field(init=False)
    id_mambu: str = ""
    estatus: str = ""
    comentarios: str = ""
