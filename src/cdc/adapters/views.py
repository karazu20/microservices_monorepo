from datetime import datetime, timedelta
from typing import Optional

from setup.adapters.data import SQLView
from src.cdc.domain import queries
from src.cdc.domain.models import Person, QueryCdc


class ConsultasCDCView(SQLView):
    def _search(
        self,
        qry: queries.GetConsultCDC,
    ) -> Optional[list]:
        today = datetime.today()
        fecha_inicial = today - timedelta(days=qry.periodo)  # type: ignore
        return (
            self.session.query(
                QueryCdc.folio,
                QueryCdc.timestamp_consulta,
                Person.curp,
                Person.nombre,
                Person.apellido_paterno,
                Person.apellido_materno,
                QueryCdc.estatus_consulta_id,
                Person.grupo_id,
            )
            .join(QueryCdc, QueryCdc.persona_id == Person.id)
            .filter(QueryCdc.username == qry.username)
            .filter(QueryCdc.timestamp_consulta.between(fecha_inicial, today))  # type: ignore
            .all()
        )
