from setup.adapters.data import SQLRepository
from src.groups.domain.models import Grupo, Usuario


class GroupRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Grupo)  # type: ignore
        self.grupo = Grupo

    def get_grupos(self, username, nombre):
        return (
            self.session.query(Grupo)
            .join(Usuario, Usuario.usuario_id == Grupo.usuario_id)
            .filter(Usuario.username == username)
            .filter(Grupo.nombre == nombre)
        ).all()

    def add_group(self, username, grupo):
        get_user = self.session.query(Usuario).filter_by(username=username).first()
        grupo._usuario = get_user
        self.session.add(grupo)
