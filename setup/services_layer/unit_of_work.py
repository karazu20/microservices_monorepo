# pylint: disable=attribute-defined-outside-init
from __future__ import annotations  # type: ignore

import abc


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def rollback(self):
        self._rollback()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self._enter()
        return super().__enter__()

    @abc.abstractmethod
    def _enter(self):
        raise NotImplementedError

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def _rollback(self):
        self.session.rollback()


class SqlAlchemyUnitOfWorkVal(AbstractUnitOfWork):
    def __init__(
        self,
        session_factory_validations=None,
        session_factory_digitalization=None,
    ):
        self.session_factory_validations = session_factory_validations
        self.session_factory_digitalization = session_factory_digitalization

    def __enter__(self):
        self.session_validations = self.session_factory_validations()
        self.session_digitalization = self.session_factory_digitalization()

        self._enter()
        return super().__enter__()

    @abc.abstractmethod
    def _enter(self):
        raise NotImplementedError

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session_validations.close()
        self.session_digitalization.close()

    def _commit(self):
        self.session_validations.commit()
        self.session_digitalization.commit()

    def _rollback(self):
        self.session_validations.rollback()
        self.session_digitalization.rollback()
