class CdcError(Exception):  # pragma: no cover
    def __init__(
        self, id, estatus, curp, folio, timestamp_consulta, fallo_regla, msg_error
    ):
        self.id = id
        self.estatus = estatus
        self.curp = curp
        self.folio = folio
        self.timestamp_consulta = timestamp_consulta
        self.fallo_regla = fallo_regla
        self.msg_error = msg_error

    def __str__(self):
        return "id: {}, estatus: {}, curp: {}, folio: {}, timestamp_consulta: {}, fallo_regla: {}".format(
            self.id,
            self.estatus,
            self.curp,
            self.folio,
            self.timestamp_consulta,
            self.fallo_regla,
        )


class CdcServiceFallo(Exception):
    pass


class CdcServiceError(Exception):
    pass


class CdcDomainError(Exception):
    pass
