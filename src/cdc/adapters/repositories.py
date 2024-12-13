from setup.adapters.data import SQLRepository
from src.cdc.domain.models import Grupo, Person, Prospecto, QueryCdc, QueryStatus


class PersonRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Person)  # type: ignore
        self.Person = Person

    def add_person(self, id_grupo, person):
        get_group = self.session.query(Grupo).filter_by(grupo_id=id_grupo).first()
        person._grupo = get_group
        self.session.add(person)


class QueryStatusRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, QueryStatus)  # type: ignore
        self.query_status = QueryStatus

    def _get(self, estatus) -> QueryStatus:
        return self.session.query(QueryStatus).filter_by(estatus=estatus).first()

    def get_folios(self, username, fecha) -> QueryCdc:
        fecha_inicial = fecha.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_final = fecha.replace(hour=23, minute=59, second=59, microsecond=0)
        return (
            self.session.query(
                QueryCdc.folio,
            )
            .filter(QueryCdc.username == username)
            .filter(QueryCdc.created.between(fecha_inicial, fecha_final))  # type: ignore
            .all()
        )


class ProspectoRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Prospecto)  # type: ignore
        self.prospecto = Prospecto

    def add_prospecto(self, prospecto: Prospecto):
        self.session.add(prospecto)

    def get_prospecto(self, curp: str) -> Prospecto:
        return self.session.query(Prospecto).filter_by(curp=curp).one()
