import logging
from typing import Any, Callable, Optional, Type

from fakeredis import FakeStrictRedis

from fakes.mambu import *
from setup import domain
from setup.adapters import bus, cache, messenger_service
from setup.adapters.data import SQLRepository, SQLView
from setup.adapters.podemos_mambu import AbstractMambu
from setup.adapters.smtp import AbstractSMTP
from setup.adapters.storage import AbstractStorage
from setup.services_layer import unit_of_work

logger = logging.getLogger(__name__)


class MunicipioRepositoryFake(SQLRepository):
    def __init__(self, municipios):
        self._municipios = municipios

    def _add(self, municipio):
        self._municipios.append(municipio)

    def _get(self, nombre):
        return next((c for c in self._municipios if c.nombre == nombre), None)

    def list(self):
        return self._municipios


class EstadoRepositoryFake(SQLRepository):
    def __init__(self, estados):
        self._estados = estados

    def _add(self, estado):
        self._estados.append(estado)

    def _get(self, nombre):
        return next((c for c in self._estados if c.nombre == nombre), None)

    def list(self):
        return self._estados


class PostalCodeViewFake(SQLView):
    def __init__(self, colonias):
        self._colonias = colonias

    def _search(self, qry: domain.Query) -> Optional[list]:
        colonias = [
            (c.nombre, "", "")
            for c in self._colonias
            if c.codigo_postal == qry.codigo_postal
        ]
        return colonias


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.committed = False
        self.rollbacked = False
        self.estados = EstadoRepositoryFake([])
        self.municipios = MunicipioRepositoryFake([])
        self.bulk_query_batch = BulkQueryBatchFake([])
        self.persons = PersonRepositoryFake([])
        self.query_status = QueryStatusRepositoryFake([])
        self.prospecto = ProspectoRepositoryFake([])
        self.stage = StageFake([])
        self.nips = NipRepositoryFake([])
        self.rule = RuleFake([])
        self.rule_execution_status = RuleExecutionStatusFake([])
        self.rule_exception_type = RuleExceptionTypeFake([])
        self.rule_execution = RuleExecutionFake([])
        self.rule_exception = RuleExceptionFake([])
        self.types = RuleExceptionTypeFake([])
        self.role = RoleFake([])
        self.role_rule = RoleRuleFake([])
        self.field_validation = FieldValidationFake([])
        self.custom_rule = CustomRuleFake([])
        self.loan_status = LoanStatusFake([])
        self.view_loan_status = LoanStatusFake([])
        self.validation_data_identifier = ValidationDataIdentifierFake([])
        self.validation_data = ValidationDataFake([])
        self.validation_rule_data = ValidationRuleDataFake([])
        self.validation_cdc = ValidationConsultCdcFake([])
        self.user = UserRepositoryFake([])
        self.view_consult = ConsultasCDCViewFake([])
        self.release_url = ReleasesRepositoryFake([])
        self.document = DocumentFake([])
        self.groups = GroupsRepositoryFake([])
        self.view_grupo = GrupoViewFake([])

    def _enter__(self):
        return super().__enter__()

    def _commit(self):
        self.committed = True

    def _rollback(self):
        self.rollbacked = True


class FakeBus(bus.AbstractBus):
    bus = []

    @classmethod
    def publish(cls, event: domain.Event):
        logger.info("event %s", event)
        cls.published = True
        cls.bus.append(event)

    @classmethod
    def subscribe(cls, event: Type[domain.Event], consumer: Callable):
        logger.info("event %s", event)
        cls.subscribed = True


class FakeCache(cache.AbstractCache):
    cache = FakeStrictRedis()

    @classmethod
    def set(cls, key: str, value: Any, expire):
        cls.cache[key] = value

    @classmethod
    def get(cls, key: str) -> Any:
        return cls.cache.get(key)


class FakeTwilioService(messenger_service.MessengerService):
    @classmethod
    def send_sms(cls, phone_number: str, message: str) -> bool:
        return True


class StageFake(SQLRepository):
    def __init__(self, stage):
        self._stage = stage

    def _add(self, stage):
        self._stage.append(stage)

    def list(self):
        return self._stage

    def _get(self, stage):
        return next((c for c in self._stage if c.etapa == stage), None)


class BulkQueryBatchFake(SQLRepository):
    def __init__(self, bulk_query_batch):
        self._bulk_query_batch = bulk_query_batch

    def _add(self, bulk_query_batch):
        self._bulk_query_batch.append(bulk_query_batch)

    def list(self):
        return self._bulk_query_batch

    def _get(self, id):
        return next((c for c in self._bulk_query_batch if c.id == id), None)

    def get_persons(self, id):
        return next((c for c in self._bulk_query_batch[0]._persons if c.id == id), None)


class PersonRepositoryFake(SQLRepository):
    def __init__(self, persons):
        self._persons = persons

    def add_person(self, id_grupo, person):
        self._persons.append(person)

    def _add(self, persons):
        self._persons.append(persons)

    def list(self):
        return self._persons


class QueryStatusRepositoryFake(SQLRepository):
    def __init__(self, query_status):
        self._query_status = query_status

    def _get(self, estatus):
        class status:
            id = 1

        return next((c for c in self._query_status if c.estatus == estatus), status())

    def get_folios(self, username=None, today=None):
        return [(value.folio) for value in self._query_status]


class ProspectoRepositoryFake(SQLRepository):
    def __init__(self, prospecto):
        self.prospecto = prospecto

    def add_prospecto(self, prospecto):
        self.prospecto.append(prospecto)

    def get_prospecto(self, curp):
        return next((c for c in self.prospecto if c.curp == curp), None)


class NipRepositoryFake(SQLRepository):
    def __init__(self, nips):
        self._nips = nips

    def _add(self, nip):
        self._nips.append(nip)

    def list(self):
        return self._nips

    def _get(self, nip):
        return next((c for c in self._nips if c.nip == nip), None)

    def get_count_nip(self, phone_number):
        return 1

    def get_last_nip(self, phone_number, curp):
        return self._nips


class RuleFake(SQLRepository):
    def __init__(self, rule):
        self._rule = rule

    def _add(self, rule):
        self._rule.append(rule)

    def list(self):
        return self._rule

    def _get(self, rule):
        return next((c for c in self._rule if c.regla == rule), None)


class RuleExecutionStatusFake(SQLRepository):
    def __init__(self, status):
        self._status = status

    def _add(self, status):
        self._status.append(status)

    def list(self):
        return self._status

    def _get(self, stage):
        return next((c for c in self._status if c.estatus == status), None)


class RuleExceptionTypeFake(SQLRepository):
    def __init__(self, types):
        self._type = types

    def _add(self, types):
        self._type.append(types)

    def list(self):
        return self._type

    def _get(self, types):
        return next((c for c in self._type if c.tipo == types), None)


class RuleExecutionFake(SQLRepository):
    def __init__(self, rule_execution):
        self._rule_execution = rule_execution

    def _add(self, rule_execution):
        self._rule_execution.append(rule_execution)

    def list(self, status=None, stage=None):
        return [
            (
                value.id,
                value.etapa_id,
                value.regla_id,
                value.estatus_ejecucion_regla_id,
            )
            for value in self._rule_execution
        ]


class RuleExceptionFake(SQLRepository):
    def __init__(self, rule_exception):
        self._rule_exception = rule_exception

    def _add(self, rule_exception):
        self._rule_exception.append(rule_exception)

    def list(self, id_mambu=None):
        return [
            (
                value.id,
                value.regla_id,
                value.tipo_excepcion_regla_id,
                value.id_mambu,
                value.id_mambu,
            )
            for value in self._rule_exception
        ]


class RoleFake(SQLRepository):
    def __init__(self, role):
        self._role = role

    def _add(self, role):
        self._role.append(role)

    def list(self):
        return self._role


class RoleRuleFake(SQLRepository):
    def __init__(self, role_rule):
        self._role_rule = role_rule

    def _add(self, role_rule):
        self._role_rule.append(role_rule)

    def list(self):
        return self._role_rule


class FieldValidationFake(SQLRepository):
    def __init__(self, field_validation):
        self._field_validation = field_validation

    def _add(self, field_validation):
        self._field_validation.append(field_validation)

    def list(self):
        return self._field_validation


class CustomRuleFake(SQLRepository):
    def __init__(self, custom_rule):
        self._custom_rule = custom_rule

    def _get(self, custom_rule):
        return next((c for c in self._custom_rule if c.id == custom_rule), None)

    def _add(self, custom_rule):
        self._custom_rule.append(custom_rule)

    def list(self):
        return self._custom_rule


class LoanStatusFake(SQLRepository):
    def __init__(self, loan_status):
        self._loan_status = loan_status

    def _add(self, loan_status):
        self._loan_status.append(loan_status)

    def _get(self, id_mambu):
        return next((c for c in self._loan_status if c.id_mambu == id_mambu), None)

    def search(self, qry: domain.Query) -> Optional[list]:
        loans_status = [
            c
            for c in self._loan_status
            if c.id_mambu == qry.id_mambu and c.estatus == qry.estatus
        ]
        return loans_status


class FakePodemosMambu(AbstractMambu):
    loans = LoansFake
    groups = GroupsFake
    clients = ClientsFake
    centres = CentresFake
    branches = BranchesFake
    products = ProductsFake
    tasks = TasksFake
    transactions = TransactionsFake
    users = UsersFake
    addresses = AddressesFake
    documents = DocumentsFake
    id_documents = IDDocumentsFake
    disbursements_details = DisbursementsDetailsFake
    group_members = GroupMembersFake
    group_roles = GroupRolesFake
    user_roles = UserRolesFake
    comments = CommentsFake

    @classmethod
    def clear(cls):
        cls.loans._objects_mambu = []
        cls.groups._objects_mambu = []
        cls.clients._objects_mambu = []
        cls.centres._objects_mambu = []
        cls.branches._objects_mambu = []
        cls.products._objects_mambu = []
        cls.tasks._objects_mambu = []
        cls.transactions._objects_mambu = []
        cls.users._objects_mambu = []
        cls.addresses._objects_mambu = []
        cls.documents._objects_mambu = []
        cls.id_documents._objects_mambu = []
        cls.disbursements_details._objects_mambu = []
        cls.group_members._objects_mambu = []
        cls.group_roles._objects_mambu = []
        cls.user_roles._objects_mambu = []
        cls.comments._objects_mambu = []


class ValidationDataIdentifierFake(SQLRepository):
    def __init__(self, validation_data_identifier):
        self._validation_data_identifier = validation_data_identifier

    def _add(self, validation_data_identifier):
        self._validation_data_identifier.append(validation_data_identifier)


class ValidationDataFake(SQLRepository):
    def __init__(self, validation_data):
        self._validation_data = validation_data

    def _add(self, validation_data):
        self._validation_data.append(validation_data)


class ValidationRuleDataFake(SQLRepository):
    def __init__(self, validation_rule_data):
        self._validation_rule_data = validation_rule_data

    def _add(self, validation_rule_data):
        self._validation_rule_data.append(validation_rule_data)


class ValidationConsultCdcFake(SQLRepository):
    def __init__(self, validation_data):
        self._validation_data = validation_data

    def _get_consult(self, validation_data):
        self._validation_data.append(validation_data)


class UserRepositoryFake(SQLRepository):
    def __init__(self, user):
        self._user = user

    def _add(self, user):
        self._user.append(user)


class ConsultasCDCViewFake(SQLRepository):
    def __init__(self, consultas):
        self._consultas = consultas

    def search(self, qry: domain.Query) -> Optional[list]:
        return []


class GroupsRepositoryFake(SQLRepository):
    def __init__(self, groups):
        self._groups = groups

    def get_grupos(self, username, nombre):
        return []

    def add_group(self, username, group):
        self._groups.append(group)


class GrupoViewFake(SQLView):
    def __init__(self, grupos):
        self._grupos = grupos

    def _search(self, qry: domain.Query) -> Optional[list]:
        return []


class ReleasesRepositoryFake(SQLRepository):
    def __init__(self, releases):
        self._releases = releases

    def _get_url_release(self):
        return next((c for c in self._releases if c.vigente == True), None)


class FakeStorage(AbstractStorage):
    service_name: str = "TEST"
    aws_access_key_id: str = "TEST_KEY_ID"
    aws_secret_access_key: str = "TEST_SECRET"
    path_s3: str = "/tmp/"
    expires_in: int = 3600

    @classmethod
    def get(cls, bucket: str, key_file: str) -> str:
        return cls.path_s3 + key_file

    @classmethod
    def get_url(cls, bucket: str, key_file: str) -> str:
        return "http://" + key_file

    @classmethod
    def put(cls, bucket: str, path_file_name: str, key: str) -> bool:
        return True


class DocumentFake(SQLRepository):
    def __init__(self, documents):
        self._documents = documents

    def _add(self, documents):
        self._documents.append(documents)

    def list(self):
        return self._documents

    def _get(self, storage_id):
        return self._documents


class FakeEmail(AbstractSMTP):
    smtp = []

    @classmethod
    def send(cls, to: list, cc: list, subject: str, message: str, attachments: list = []):
        try:
            msg = (
                "Correo: to=%s cc=%s message=%s attachments=%s",
                str(to),
                str(cc),
                message,
                str(attachments),
            )
            logger.info(msg)
            cls.smtp.append(msg)

        except Exception as ex:
            logger.error("Error al enviar correo a %s: %s", str(to), str(ex))
