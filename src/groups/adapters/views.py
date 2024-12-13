from typing import Optional

from setup.adapters.data import SQLView
from src.groups.domain import queries
from src.groups.domain.models import Grupo, Usuario


class GrupoView(SQLView):
    def _search(
        self,
        qry: queries.GetGrupo,
    ) -> Optional[list]:
        return (
            self.session.query(
                Grupo.grupo_id,
                Grupo.nombre,
                Grupo.mambu_id,
                Grupo.insert_date,
            )
            .join(Usuario, Usuario.usuario_id == Grupo.usuario_id)
            .filter(Usuario.username == qry.username)
            .all()
        )
