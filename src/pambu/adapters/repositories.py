from setup.adapters.data import SQLRepository
from src.pambu.domain.models import Releases, User


class UserRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, User)  # type: ignore
        self.user = User


class ReleasesRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Releases)  # type: ignore
        self.Releases = Releases

    def _get_url_release(self):
        return (
            self.session.query(Releases.url_version)
            .filter(Releases.vigente == True)
            .order_by(Releases.id.desc())  # type: ignore
            .first()
        )
