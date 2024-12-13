from typing import Optional

from setup.adapters.data import SQLView
from src.sepomex.domain import queries
from src.sepomex.domain.models import Colonia, Estado, Municipio


class PostalCodeView(SQLView):
    def _search(
        self,
        qry: queries.GetDataFromCP,
    ) -> Optional[list]:
        return (
            self.session.query(
                Colonia.nombre, Colonia.codigo_postal, Municipio.nombre, Estado.nombre
            )
            .join(Municipio, Municipio.id == Colonia.id_municipio)
            .join(Estado, Estado.id == Municipio.id_estado)
            .filter(Colonia.codigo_postal == qry.codigo_postal)
            .all()
        )
