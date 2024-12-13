from setup.services_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.pambu import config
from src.pambu.adapters import repositories


class UnitOfWorkPambu(SqlAlchemyUnitOfWork):
    def __init__(self, session_factory=config.DEFAULT_SESSION_FACTORY):
        super().__init__(session_factory)

    def _enter(self):
        self.user = repositories.UserRepository(self.session)
        self.release_url = repositories.ReleasesRepository(self.session)
