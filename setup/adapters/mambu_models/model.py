from __future__ import annotations  # type: ignore

import abc
import logging
from dataclasses import Field, asdict, dataclass, field, fields
from datetime import datetime
from enum import Enum
from functools import wraps

from mambupy.api.entities import (
    MambuEntity,
    MambuEntityAttachable,
    MambuEntityCommentable,
    MambuEntitySearchable,
)
from mambupy.mambuutil import MambuCommError, MambuError, MambuPyError
from mambupy.orm import schema_orm as orm
from mambupy.orm.schema_orm import Base as BaseMambu

from setup.adapters import mambu_models as models
from setup.sessions import current_user

logger = logging.getLogger(__name__)


SEARCH_FILTER_CRITERIAS = {
    "=": {
        "operators": ("EQUALS", "ON", "EQUALS_CASE_SENSITIVE"),
        "types": (("int", "float", "bool"), ("date", "datetime"), ("str")),
        "items": 3,
        "values": 1,
    },
    "!=": {
        "operators": ("DIFFERENT_THAN",),
        "types": (("int", "float", "str", "bool"),),
        "items": 3,
        "values": 1,
    },
    ">": {
        "operators": ("MORE_THAN", "AFTER"),
        "types": (("int", "float"), ("date", "datetime")),
        "items": 3,
        "values": 1,
    },
    "<": {
        "operators": ("LESS_THAN", "BEFORE"),
        "types": (("int", "float"), ("date", "datetime")),
        "items": 3,
        "values": 1,
    },
    "<=": {
        "operators": ("BEFORE_INCLUSIVE",),
        "types": (("date", "datetime"),),
        "items": 3,
        "values": 1,
    },
    "between": {
        "operators": ("BETWEEN",),
        "types": (("int", "float", "date", "datetime"),),
        "items": 4,
        "values": 2,
    },
    "startwith": {
        "operators": ("STARTS_WITH_CASE_SENSITIVE",),
        "types": (("str"),),
        "items": 3,
        "values": 1,
    },
    "in": {"operators": ("IN",), "types": (("int", "str"),), "items": 3, "values": 1},
}


SEARCH_SORT_CRITERIAS = {
    "desc": "DESC",
    "asc": "ASC",
}


def handler_mambu_error(func):  # pragma: no cover
    @wraps(func)
    def wrapper(*args, **kwargs):
        if Mode.ORM not in args:
            try:
                return func(*args, **kwargs)
            except MambuCommError as e:
                logger.error("Error to connect with mambu: {}".format(e))
                raise e
            except MambuError as e:
                logger.error("Mambu Error: {}".format(e))
                raise e
            except MambuPyError as e:
                logger.error("Mambupy Error: {}".format(e))
                raise e
            except Exception as e:
                logger.error("Exception in mambupy: {}".format(e))
                raise e

        else:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error("Exception in orm mambu: {}".format(e))
                raise e

    return wrapper


class Mode(Enum):
    REST = "REST"
    ORM = "ORM"


class Details(Enum):
    BASIC = "BASIC"
    FULL = "FULL"


class Pagination(Enum):
    OFF = "OFF"
    ON = "ON"


class DateOperators(Enum):
    today = "TODAY"
    week = "THIS_WEEK"
    month = "THIS_MONTH"
    year = "THIS_YEAR"


BASE_FIELDS = [
    "_model_rest",
    "_model_orm",
    "_mode",
    "_instance_mambu",
    "_fields",
    "_violations_readonly_rule",
    "_is_init",
    "_is_new",
    "save",
    "write",
    "update_state",
]


def reloaded_attrs(attrs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            instance_model = args[0]
            for attr in attrs:
                instance_model._fields[attr]["loaded"] = False
            return response

        return wrapper

    return decorator


class MambuModel(abc.ABC):
    _model_rest: MambuEntity = NotImplemented
    _model_orm: BaseMambu = NotImplemented

    def _get_entity_value(self, metadata):
        getattr(
            self._instance_mambu,
            f"get_{metadata['mambu_source']}",
        )()
        try:
            response_mambu = getattr(
                self._instance_mambu,
                metadata["mambu_source"],
            )
        except AttributeError:
            return None
        return (
            [getattr(models, metadata["model"]).get(o.id) for o in response_mambu]
            if metadata.get("is_many")
            else getattr(models, metadata["model"]).get(response_mambu.id)
        )

    def _get_vo_value(self, metadata):
        if metadata.get("lazy_from_method"):
            getattr(
                self._instance_mambu,
                metadata.get("lazy_from_method"),
            )()
        try:
            response_mambu = getattr(
                self._instance_mambu,
                metadata["mambu_source"],
            )
        except AttributeError:
            return None
        return (
            [getattr(models, metadata["model"])(o) for o in response_mambu]
            if metadata.get("is_many")
            else getattr(models, metadata["model"])(response_mambu)
        )

    def __getattribute__(self, attr):
        if attr in BASE_FIELDS or self._is_new:
            return super().__getattribute__(attr)
        elif attr in self._fields and not self._fields[attr]["loaded"]:
            metadata = self._fields[attr]["field"].metadata  # type: ignore
            if metadata.get("is_entity") and not self._is_new:
                value = self._get_entity_value(metadata)
            elif metadata.get("is_vo"):
                value = self._get_vo_value(metadata)
            else:
                try:
                    value = self._instance_mambu[metadata["mambu_source"]]
                except KeyError:
                    value = None

            self._fields[attr]["setted"] = 1
            setattr(self, attr, value)
            self._fields[attr]["loaded"] = True
            return value
        return super().__getattribute__(attr)

    def __getattr__(self, attr):
        if attr in self._fields:
            return None
        else:
            raise AttributeError(f"Not exist '{attr}' in '{self.__class__.__name__}'")

    def __setattr__(self, attr, value):
        if attr in BASE_FIELDS:
            super().__setattr__(attr, value)
        elif attr in self._fields:
            metadata = self._fields[attr]["field"].metadata  # type: ignore
            if self._is_init or self._is_new:
                setattr(self._instance_mambu, metadata["mambu_source"], value)
                super().__setattr__(attr, value)
                self._fields[attr]["loaded"] = True
                self._fields[attr]["setted"] = 1
            elif (self._fields[attr]["loaded"] or self._fields[attr]["setted"] == 0) and (
                metadata.get("read_only")
                or metadata.get("is_entity")
                or metadata.get("is_vo")
            ):
                self._violations_readonly_rule = True
                raise Exception(
                    f"The attribute '{attr}' of '{self.__class__.__name__}' is read only or is relations to entity"
                )
            elif not metadata.get("is_entity") and not metadata.get("is_vo"):
                self._instance_mambu[metadata["mambu_source"]] = value
            super().__setattr__(attr, value)
            self._fields[attr]["loaded"] = True
            self._fields[attr]["setted"] = 1

        else:
            raise Exception(
                f"The attribute '{attr}' not exist in '{self.__class__.__name__}'"
            )

    def __init__(
        self,
        instance_mambu,
        fields_model: list[Field],
        mode=Mode.REST,
        is_vo=False,
        **kwargs,
    ):
        self._fields = {}
        for f in fields_model:
            self._fields[f.name] = {"loaded": False, "field": f, "setted": 0}
        if instance_mambu:
            self._instance_mambu = instance_mambu
            self._is_new = False
        else:
            self._is_init = True
            self._is_new = True
            if mode == Mode.REST:
                self._instance_mambu = self._model_rest()
            else:
                self._instance_mambu = self._model_orm()
            for k, v in kwargs.items():
                setattr(self, k, v)
        self._mode = mode
        self._violations_readonly_rule = False
        self._is_init = False

    def to_dict(self):
        return asdict(self)

    @classmethod
    def get(cls, id, mode=Mode.REST) -> MambuModel:
        """get a entity record for id or encoded_key from mambu

        Args:
          id (str): id or encoded_key of entity mambu
          mode (Enum): option REST if is necessary online or ORM in case offline

        Returns:
          object: object entity mambu
        """
        if issubclass(cls, VOMambu):
            raise Exception(
                f"This object '{cls.__name__}' is a VO, not support get operation"
            )
        if mode == Mode.REST:
            user = current_user()
            if user and user.pass_mambu:
                try:
                    instance_mambu = cls._model_rest.get(
                        entid=id,
                        detailsLevel=Details.FULL.value,
                        get_entities=False,
                        user=user.username,
                        pwd=user.pass_mambu,
                    )
                except MambuError:
                    instance_mambu = cls._model_rest.get(
                        entid=id, detailsLevel=Details.FULL.value, get_entities=False
                    )
            else:
                instance_mambu = cls._model_rest.get(
                    entid=id, detailsLevel=Details.FULL.value, get_entities=False
                )
        else:
            session = orm.Session()
            instance_mambu = session.query(cls._model_orm).filter_by(id=id).first()

        return cls(instance_mambu, mode)

    @classmethod
    def _parse_sort_criteria(cls, criteria, _fields):
        if criteria:
            sort_criterias = criteria.split()
            if len(sort_criterias) > 2:
                raise Exception(
                    f"arg sortby not valid {criteria}, please use an valid format 'field' or 'field desc' "
                )

            for f in _fields:
                if f.name == sort_criterias[0]:
                    _field = f
                    break
            else:
                raise Exception(
                    f"arg sortby not valid, the field {sort_criterias[0]}"
                    f" not exist in entity {cls.__name__}"
                )

            order = SEARCH_SORT_CRITERIAS["asc"]
            if len(sort_criterias) > 1:
                try:
                    order = SEARCH_SORT_CRITERIAS[sort_criterias[1]]
                except KeyError:
                    raise Exception(
                        f"arg sortby not valid, invalid order '{sort_criterias[1]}'"
                    )

            return {"field": _field.metadata["mambu_source"], "order": order}

    @classmethod
    def _get_operation_from_type(cls, type_field, search_criteria):
        for types in search_criteria["types"]:
            if type_field in types:
                return search_criteria["operators"][search_criteria["types"].index(types)]
        raise Exception(
            (
                f"Not support mambu operation for this type '{type_field}'"
                f" and mambu criteria  '{search_criteria}' in entity {cls.__name__}"
            )
        )

    @classmethod
    def _validate_format_criteria(cls, criteria: tuple, _fields):
        if len(criteria) < 3:
            raise Exception(
                (
                    f"Criteria not valid {criteria}, please use an valid format "
                    "('field', 'operation', 'value') or ('field', 'operation', 'value', 'second_value')"
                )
            )
        try:
            search_criteria = SEARCH_FILTER_CRITERIAS[criteria[1]]
        except KeyError:
            raise Exception(
                f"Criteria not valid, only supports this operations [{SEARCH_FILTER_CRITERIAS.keys()} ]"
            )
        for f in _fields:
            if f.name == criteria[0]:
                _field = f
                break
        else:
            raise Exception(
                f"Criteria not valid, the field '{criteria[0]}' not exist in entity {cls.__name__}"
            )
        if criteria[1] == "in" and not isinstance(criteria[2], list):
            raise Exception(
                f"Criteria not valid, the operation '{criteria[1]}' required a list values"
            )
        if criteria[1] == "between" and len(criteria) != 4:
            raise Exception(
                (
                    f"Criteria not valid, the operation '{criteria[1]}'"
                    " required 4 items ('field', 'between', 'value', 'second_value')"
                )
            )

        return search_criteria, _field

    @classmethod
    def _parser_field_criteria(cls, _field):
        if _field.metadata.get("is_cf"):
            return _field.metadata["path"].replace("/", ".")[1:]
        else:
            return _field.metadata["mambu_source"]

    @classmethod
    def _parse_filter_criteria(cls, criterias, _fields):
        mambu_criterias = []
        if not criterias or not isinstance(criterias, list):
            raise Exception(
                "criterias search, only supports a list with at least one criterias"
            )

        for criteria in criterias:
            search_criteria, _field = cls._validate_format_criteria(criteria, _fields)
            if criteria[1] == "in":
                mambu_criteria = {
                    "field": cls._parser_field_criteria(_field),
                    "operator": cls._get_operation_from_type(
                        _field.type, search_criteria
                    ),
                    "values": criteria[2],
                }
            elif criteria[1] == "between":
                mambu_criteria = {
                    "field": cls._parser_field_criteria(_field),
                    "operator": cls._get_operation_from_type(
                        _field.type, search_criteria
                    ),
                    "value": criteria[2],
                    "secondValue": criteria[3],
                }

            else:
                mambu_criteria = {
                    "field": cls._parser_field_criteria(_field),
                    "operator": cls._get_operation_from_type(
                        _field.type, search_criteria
                    ),
                    "value": criteria[2],
                }

            mambu_criterias.append(mambu_criteria)

        return mambu_criterias

    @classmethod
    def _get_filters_for_all(cls, criterias, _fields):
        filters_str = []
        if not criterias or not isinstance(criterias, list):
            raise Exception(
                "criterias search, only supports a list with at least one criterias"
            )
        for criteria in criterias:
            search_criteria, _field = cls._validate_format_criteria(criteria, _fields)

            if criteria[1] == "between":
                filter_str = (
                    f"obj.{_field.metadata['mambu_source']} >= {criteria[2]}"
                    f" and {_field.metadata['mambu_source']} <= {criteria[3]}"
                )
            elif criteria[1] == "=":
                filter_str = (
                    f"obj.{_field.metadata['mambu_source']} == '{criteria[2]}'"
                    if _field.type == "str"
                    else f"obj.{_field.metadata['mambu_source']} == {criteria[2]}"
                )
            elif criteria[1] == "startwith":
                filter_str = f"str(obj.{_field.metadata['mambu_source']}).startswith('{criteria[2]}')"
            else:
                filter_str = (
                    f"obj.{_field.metadata['mambu_source']} {criteria[1]} {criteria[2]}"
                )

            filters_str.append(filter_str)
        return filters_str

    @classmethod
    def search(
        cls,
        criterias: list[tuple],
        orderby: str = None,
        offset: int = None,
        limit: int = None,
        pagination_details: Enum = Pagination.OFF,
    ) -> list[MambuModel]:
        """search retrieve data from mambu online,

        Args:
          criterias (list(tuples)): list of tuples for apply in search
            - Use criterias criterias with next in next formats
                ('field_name', 'operation', value)
                or
                ('field_name', 'operation', value, value_second) in case between

            - Operations availables for searchs:
                    '=': field equal to value
                    '!=': field different than value
                    '>': field more than value
                    '<': field less than value
                    '<=': field less than value, only apply for dates
                    'between': field between value and second_values, for this operation the format is
                               ('field_name', 'operation', value, second_value)
                    'start_with': field start with value, this operations only apply for strins and is case sensitive
                    'in': field in list value
            - Valid format for dates 'YYYY-MM-DD'

          orderby (str): string with name field and type order 'name' or 'name desc', by default the order is 'asc'
          offset (int): pagination, index to start searching
          limit (int): pagination, number of elements to retrieve
          pagination_details (str ON/OFF): ask for details on pagination

        search operation is only supported by REST mode and only Entities.

        Returns:
          list: Objects list mambu entities.
        """

        if issubclass(cls, VOMambu):
            raise Exception(
                f"This object '{cls.__name__}' is a VO, not support search operations"
            )

        if issubclass(cls._model_rest, MambuEntitySearchable):
            filter_criterias = cls._parse_filter_criteria(criterias, fields(cls))
            sorting_criteria = cls._parse_sort_criteria(orderby, fields(cls))
            instances_mambu = cls._model_rest.search(
                filterCriteria=filter_criterias,
                sortingCriteria=sorting_criteria,
                offset=offset,
                limit=limit,
                paginationDetails=pagination_details.value,
                detailsLevel=Details.FULL.value,
            )
        else:
            filters = cls._get_filters_for_all(criterias, fields(cls))
            sorting_criteria = cls._parse_sort_criteria(orderby, fields(cls))
            try:
                instances_mambu = cls._model_rest.get_all(
                    offset=offset,
                    limit=limit,
                    paginationDetails=pagination_details.value,
                    detailsLevel=Details.FULL.value,
                )
            except TypeError:
                instances_mambu = cls._model_rest.get_all(
                    offset=offset,
                    limit=limit,
                    paginationDetails=pagination_details.value,
                )

            def apply_eval(condition, obj):
                try:
                    return eval(condition)
                except AttributeError:
                    return False

            for f in filters:
                instances_mambu = list(
                    filter(lambda obj, condition=f: apply_eval(condition, obj), instances_mambu)  # type: ignore
                )
        objects = []
        for instance_mambu in instances_mambu:
            _object = cls(instance_mambu, Mode.REST)  # type: ignore
            objects.append(_object)
        if sorting_criteria:
            objects.sort(
                key=lambda o: getattr(o, sorting_criteria["field"]),
                reverse=sorting_criteria["order"] == "DESC",
            )
        return objects

    def write(self, data: dict) -> bool:
        """writes (patches) changes on a Mambu object

        BEWARE: the mambu object will be changed after this operation

        Args:
          data (dict): dict of fields-values to apply to the Mambu object

        write operation is only supported by REST mode.

        Returns:
          bool: True if succesful operation applied.
        """

        if isinstance(self, VOMambu):
            raise Exception(
                f"This object '{self.__class__.__name__}' is a VO, not support write operations"
            )

        if self._mode == Mode.ORM:
            raise Exception("ORM mode does not support write operations")

        for k, v in data.items():
            setattr(self, k, v)
        fields_to_update = [
            self._fields.get(key)["field"].metadata["mambu_source"] for key in data.keys()  # type: ignore
        ]
        self._instance_mambu.patch(fields=fields_to_update)
        return True

    def save(self):
        """saves (creates or updates) changes on a Mambu object

        BEWARE: when creating, the mambu object will be changed after this
        operation

        BEWARE: when updating, EVERYTHING on the mambu object will be uploaded
        to Mambu

        - create is applied for NEW objects, with no encodedKey associated
        - update is applied for already existing objects

        Args:
        save operation is only supported by REST mode.

        Returns:
          bool: True if succesful operation applied.
        """
        if isinstance(self, VOMambu):
            raise Exception(
                f"This object '{self.__class__.__name__}' is a VO, not support update/save operations"
            )

        if self._mode == Mode.ORM:
            raise Exception("ORM mode does not support update/save operations")

        if self._violations_readonly_rule:
            raise Exception("This instance no its validate, violations readonly rule")

        if self.encoded_key:
            self._instance_mambu.update()
        else:
            self._instance_mambu.create()

    @classmethod
    def _parse_filter_criteria_date(cls, date_field: str, date_operator: Enum, _fields):

        if not date_field or not isinstance(date_field, str):
            raise Exception("date_field, should str")

        for f in _fields:
            if f.name == date_field:
                _field = f
                break

        if _field.type not in ("date", "datetime"):
            raise Exception(
                f"the field '{date_field}' not is type date or datetime in the class '{cls.__name__}'"
            )

        mambu_criteria = {
            "field": cls._parser_field_criteria(_field),
            "operator": date_operator.value,
        }

        return [mambu_criteria]

    @classmethod
    def _search_by_operator_date(
        cls, date_field, extra_criterias, orderby, date_operator
    ) -> list[MambuModel]:
        criterias = cls._parse_filter_criteria_date(
            date_field, date_operator, fields(cls)
        )
        if extra_criterias:
            criterias = criterias + cls._parse_filter_criteria(
                extra_criterias, fields(cls)
            )
        sorting_criteria = cls._parse_sort_criteria(orderby, fields(cls))
        instances_mambu = cls._model_rest.search(
            filterCriteria=criterias,
            sortingCriteria=sorting_criteria,
            detailsLevel=Details.FULL.value,
        )
        objects = []
        for instance_mambu in instances_mambu:
            _object = cls(instance_mambu, Mode.REST)  # type: ignore
            objects.append(_object)
        return objects

    @classmethod
    def search_today(
        cls,
        date_field: str = "creation_date",
        extra_criterias: list[tuple] = None,
        orderby: str = None,
    ) -> list[MambuModel]:
        """search retrieve today's data from mambu online,

        Args:
          date_field (str): field name for use how criteria on today, this field must be date type
          criterias (list(tuples)): list of tuples for apply in search
            - Use criterias criterias with next in next formats
                ('field_name', 'operation', value)
                or
                ('field_name', 'operation', value, value_second) in case between

            - Operations availables for searchs:
                    '=': field equal to value
                    '!=': field different than value
                    '>': field more than value
                    '<': field less than value
                    '<=': field less than value, only apply for dates
                    'between': field between value and second_values, for this operation the format is
                               ('field_name', 'operation', value, second_value)
                    'start_with': field start with value, this operations only apply for strins and is case sensitive
                    'in': field in list value
          orderby (str): string with name field and type order 'name' or 'name desc', by default the order is 'asc'
        search operation is only supported by REST mode and only Entities.

        Returns:
          list: Objects list mambu entities.
        """
        if issubclass(cls._model_rest, MambuEntitySearchable):
            return cls._search_by_operator_date(
                date_field, extra_criterias, orderby, DateOperators.today
            )
        else:
            raise Exception(
                f"This object '{cls.__name__}' is a entity with out support search operations"
            )

    @classmethod
    def search_this_week(
        cls,
        date_field: str = "creation_date",
        extra_criterias: list[tuple] = None,
        orderby: str = None,
    ) -> list[MambuModel]:
        """search retrieve this week's data from mambu online,

        Args:
          date_field (str): field name for use how criteria on this week, this field must be date type
          criterias (list(tuples)): list of tuples for apply in search
            - Use criterias criterias with next in next formats
                ('field_name', 'operation', value)
                or
                ('field_name', 'operation', value, value_second) in case between

            - Operations availables for searchs:
                    '=': field equal to value
                    '!=': field different than value
                    '>': field more than value
                    '<': field less than value
                    '<=': field less than value, only apply for dates
                    'between': field between value and second_values, for this operation the format is
                               ('field_name', 'operation', value, second_value)
                    'start_with': field start with value, this operations only apply for strins and is case sensitive
                    'in': field in list value
          orderby (str): string with name field and type order 'name' or 'name desc', by default the order is 'asc'
        search operation is only supported by REST mode and only Entities.

        Returns:
          list: Objects list mambu entities.
        """
        if issubclass(cls._model_rest, MambuEntitySearchable):
            return cls._search_by_operator_date(
                date_field, extra_criterias, orderby, DateOperators.week
            )
        else:
            raise Exception(
                f"This object '{cls.__name__}' is a entity with out support search operations"
            )

    @classmethod
    def search_this_month(
        cls,
        date_field: str = "creation_date",
        extra_criterias: list[tuple] = None,
        orderby: str = None,
    ) -> list[MambuModel]:
        """search retrieve this month's data from mambu online,

        Args:
          date_field (str): field name for use how criteria on this month, this field must be date type
          criterias (list(tuples)): list of tuples for apply in search
            - Use criterias criterias with next in next formats
                ('field_name', 'operation', value)
                or
                ('field_name', 'operation', value, value_second) in case between

            - Operations availables for searchs:
                    '=': field equal to value
                    '!=': field different than value
                    '>': field more than value
                    '<': field less than value
                    '<=': field less than value, only apply for dates
                    'between': field between value and second_values, for this operation the format is
                               ('field_name', 'operation', value, second_value)
                    'start_with': field start with value, this operations only apply for strins and is case sensitive
                    'in': field in list value
          orderby (str): string with name field and type order 'name' or 'name desc', by default the order is 'asc'
        search operation is only supported by REST mode and only Entities.

        Returns:
          list: Objects list mambu entities.
        """
        if issubclass(cls._model_rest, MambuEntitySearchable):
            return cls._search_by_operator_date(
                date_field, extra_criterias, orderby, DateOperators.month
            )
        else:
            raise Exception(
                f"This object '{cls.__name__}' is a entity with out support search operations"
            )

    @classmethod
    def search_this_year(
        cls,
        date_field: str = "creation_date",
        extra_criterias: list[tuple] = None,
        orderby: str = None,
    ) -> list[MambuModel]:
        """search retrieve this year's data from mambu online,

        Args:
          date_field (str): field name for use how criteria on this year, this field must be date type
          criterias (list(tuples)): list of tuples for apply in search
            - Use criterias criterias with next in next formats
                ('field_name', 'operation', value)
                or
                ('field_name', 'operation', value, value_second) in case between

            - Operations availables for searchs:
                    '=': field equal to value
                    '!=': field different than value
                    '>': field more than value
                    '<': field less than value
                    '<=': field less than value, only apply for dates
                    'between': field between value and second_values, for this operation the format is
                               ('field_name', 'operation', value, second_value)
                    'start_with': field start with value, this operations only apply for strins and is case sensitive
                    'in': field in list value
          orderby (str): string with name field and type order 'name' or 'name desc', by default the order is 'asc'
        search operation is only supported by REST mode and only Entities.

        Returns:
          list: Objects list mambu entities.
        """
        if issubclass(cls._model_rest, MambuEntitySearchable):
            return cls._search_by_operator_date(
                date_field, extra_criterias, orderby, DateOperators.year
            )
        else:
            raise Exception(
                f"This object '{cls.__name__}' is a entity with out support search operations"
            )

    @reloaded_attrs(attrs=["comments"])
    def add_comment(self, comment, mode=Mode.REST):
        if isinstance(self._instance_mambu, MambuEntityCommentable):

            if self._mode == Mode.REST:
                self._instance_mambu.comment(comment)
            else:
                raise Exception("ORM mode does not support write operations.")
        else:
            raise Exception(
                f"This object '{self.__class__.__name__}' is a entity with out support comments"
            )

    def attach_document(self, filename: str, title: str = "", notes: str = ""):
        if isinstance(self._instance_mambu, MambuEntityAttachable):

            if self._mode == Mode.REST:
                self._instance_mambu.attach_document(filename, title, notes)
            else:
                raise Exception("ORM mode does not support write operations.")
        else:
            raise Exception(
                f"This object '{self.__class__.__name__}' is a entity with out support documents"
            )


@dataclass(init=False)
class BaseModel:

    id: str = field(
        metadata={"mambu_source": "id", "read_only": True, "is_required": False}
    )

    encoded_key: str = field(
        metadata={"mambu_source": "encodedKey", "read_only": True, "is_required": False}
    )

    creation_date: datetime = field(
        metadata={
            "mambu_source": "creationDate",
            "read_only": True,
            "is_required": False,
        }
    )
    last_modified_date: datetime = field(
        metadata={
            "mambu_source": "lastModifiedDate",
            "read_only": True,
            "is_required": False,
        }
    )


@dataclass(init=False)
class BaseVO:
    encoded_key: str = field(
        metadata={"mambu_source": "encodedKey", "read_only": True, "is_required": False}
    )


@dataclass
class EntityMambu(MambuModel, BaseModel):
    def __init__(self, instance_mambu, fields_model, mode=Mode.REST, **kwargs):
        super().__init__(instance_mambu, fields_model, mode, **kwargs)


@dataclass
class VOMambu(MambuModel, BaseVO):
    def __init__(self, instance_mambu, fields_model, mode=Mode.REST, **kwargs):
        if mode == Mode.ORM:
            raise Exception("ORM mode does not support for VOs")
        super().__init__(instance_mambu, fields_model, mode, **kwargs)
