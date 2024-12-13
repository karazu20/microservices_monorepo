import abc
from typing import Union

from setup.domain import Model, Query

ID = Union[int, str]


class AbstractRepository(abc.ABC):
    def add(self, model: Model):
        self._add(model)

    def get(self, id: ID):
        model = self._get(id)
        return model

    @abc.abstractmethod
    def _add(self, model: Model):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: ID):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self):
        raise NotImplementedError


class SQLRepository(AbstractRepository):
    def __init__(self, session, model: Model):
        super().__init__()
        self.session = session
        self.model = model

    def _add(self, model: Model):
        self.session.add(model)

    def _get(self, id: ID):
        return self.session.query(self.model).filter_by(id=id).first()

    def list(self):
        return self.session.query(self.model).all()


class AbstractView(abc.ABC):
    @abc.abstractmethod
    def search(self, qry: Query):
        raise NotImplementedError


class SQLView(abc.ABC):
    def __init__(self, session):
        self.session = session

    def search(self, qry: Query):
        return self._search(qry)

    @abc.abstractmethod
    def _search(self, qry):
        raise NotImplementedError
