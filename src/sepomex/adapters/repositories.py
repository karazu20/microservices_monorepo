from setup.adapters.data import SQLRepository
from src.sepomex.domain.models import Estado, Municipio


class EstadoRepository(SQLRepository):
    def __init__(
        self,
        session,
    ):
        super().__init__(session, Estado)  # type: ignore

    def _get(self, name) -> Estado:
        return self.session.query(Estado).filter_by(nombre=name).first()


class MunicipioRepository(SQLRepository):
    def __init__(
        self,
        session,
    ):
        super().__init__(session, Municipio)  # type: ignore

    def _get(self, name) -> Municipio:
        return self.session.query(Municipio).filter_by(nombre=name).first()
