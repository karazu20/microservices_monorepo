from dataclasses import field
from datetime import datetime
from typing import Optional

import marshmallow.validate
from marshmallow import validates_schema
from marshmallow_dataclass import dataclass

from setup.domain import Query


@dataclass
class GetGroup(Query):
    group_id: Optional[str] = field(metadata={"required": False})
    group_name: Optional[str] = field(metadata={"required": False})
    limit: Optional[int] = field(metadata={"required": False}, default=10)
    offset: Optional[int] = field(metadata={"required": False}, default=0)


@dataclass
class GetClient(Query):
    client_id: Optional[str] = field(metadata={"required": False})
    first_name: Optional[str] = field(metadata={"required": False})
    middle_name: Optional[str] = field(metadata={"required": False})
    last_name: Optional[str] = field(metadata={"required": False})
    rfc: Optional[str] = field(metadata={"required": False})
    limit: Optional[int] = field(metadata={"required": False}, default=10)
    offset: Optional[int] = field(metadata={"required": False}, default=0)


@dataclass
class GetLoan(Query):
    loan_id: Optional[str] = field(metadata={"required": False})
    status: Optional[str] = field(metadata={"required": False})
    sub_status_web: Optional[str] = field(metadata={"required": False})
    limit: Optional[int] = field(metadata={"required": False}, default=10)
    offset: Optional[int] = field(metadata={"required": False}, default=0)
    data_response: Optional[str] = field(metadata={"required": False}, default=None)
    tribu: Optional[str] = field(metadata={"required": False}, default=None)
    date_init: Optional[str] = field(metadata={"required": False}, default=None)
    date_end: Optional[str] = field(metadata={"required": False}, default=None)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data["date_init"] and not data["date_end"]:
            raise marshmallow.ValidationError("date_end es requerida")
        if not data["date_init"] and data["date_end"]:
            raise marshmallow.ValidationError("date_init es requerida")

        if data["date_init"] and data["date_end"]:
            try:
                datetime.strptime(data["date_init"], "%Y-%m-%d")
            except ValueError:
                raise marshmallow.ValidationError(
                    "date_init formato incorrecto de fecha, el correcto es Y-m-d (%s)"
                    % datetime.now().strftime("%Y-%m-%d")
                )

            try:
                datetime.strptime(data["date_end"], "%Y-%m-%d")
            except ValueError:
                raise marshmallow.ValidationError(
                    "date_end formato incorrecto de fecha, el correcto es Y-m-d (%s)"
                    % datetime.now().strftime("%Y-%m-%d")
                )


@dataclass
class GetClientId(Query):
    id: Optional[str] = field(metadata={"required": True})


@dataclass
class GetLoanId(Query):
    id: Optional[str] = field(metadata={"required": True})


@dataclass
class GetGroupId(Query):
    id: Optional[str] = field(metadata={"required": True})
