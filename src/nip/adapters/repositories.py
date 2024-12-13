from datetime import datetime, timedelta

from setup.adapters.data import SQLRepository
from src.nip.config import HOURS_LIMT_TO_CREATE_NEW_NIPS
from src.nip.domain.models import Nip


class NipRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Nip)  # type: ignore

    def _get(self, nip):
        nip = self.session.query(Nip).filter_by(nip=nip).first()
        return nip

    def get_count_nip(self, phone_number):
        now = datetime.now()
        now_24 = now - timedelta(hours=HOURS_LIMT_TO_CREATE_NEW_NIPS)
        total_nips = (
            self.session.query(Nip)
            .filter(Nip.telefono == phone_number, Nip.created > now_24)
            .count()
        )
        return total_nips

    def get_last_nip(self, phone_number, curp):
        now = datetime.now()
        now_24 = now - timedelta(hours=HOURS_LIMT_TO_CREATE_NEW_NIPS)
        last_nip = (
            self.session.query(Nip)
            .filter(Nip.telefono == phone_number, Nip.created > now_24, Nip.curp == curp)
            .first()
        )
        return last_nip
