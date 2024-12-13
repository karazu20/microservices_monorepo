from typing import Callable, Dict, Type  # isort:skip

from typing import Dict, List

from setup import domain  # type: ignore
from setup.adapters import podemos_mambu
from src.mambu.domain import queries
from src.mambu.utils.util import (
    get_criteria_data,
    get_json_client,
    get_json_group,
    get_json_loan,
)

ARRAY_SEARCH_KEY = {
    "client": {
        "client_id": ("id", "startwith"),
        "first_name": ("first_name", "startwith"),
        "middle_name": ("middle_name", "startwith"),
        "last_name": ("last_name", "startwith"),
        "rfc": ("rfc", "startwith"),
    },
    "group": {
        "group_id": ("id", "startwith"),
        "group_name": ("group_name", "startwith"),
    },
    "loan": {
        "loan_id": ("id", "startwith"),
        "status": ("account_state", "="),
        "sub_status_web": ("sub_status_web", "startwith"),
        "date_init": ("creation_date", "between"),
        "date_end": ("creation_date", "between"),
    },
}


def get_groups(
    query: queries.GetGroup,
    mambu: podemos_mambu.PodemosMambu,
) -> List[Dict]:
    group_json = []

    criteria_data = get_criteria_data(
        array_search_key=ARRAY_SEARCH_KEY["group"], criteria=query
    )

    groups = mambu.groups.search(criterias=criteria_data, limit=query.limit, offset=query.offset)  # type: ignore
    for value in groups:
        group_json.append(get_json_group(group=value))

    return group_json


def get_clients(
    query: queries.GetClient,
    mambu: podemos_mambu.PodemosMambu,
) -> List[Dict]:
    client_json = []

    criteria_data = get_criteria_data(
        array_search_key=ARRAY_SEARCH_KEY["client"], criteria=query
    )

    clients = mambu.clients.search(criterias=criteria_data, limit=query.limit, offset=query.offset)  # type: ignore
    for value in clients:
        client_json.append(get_json_client(client=value))  # type: ignore

    return client_json


def get_loans(
    query: queries.GetLoan,
    mambu: podemos_mambu.PodemosMambu,
) -> List[Dict]:
    loan_json = []

    criteria_data = get_criteria_data(
        array_search_key=ARRAY_SEARCH_KEY["loan"], criteria=query
    )

    if query.tribu:
        loans = mambu.loans.search_by_tribu(
            centre_id=query.tribu, limit=query.limit, offset=query.offset  # type: ignore
        )
    else:
        loans = mambu.loans.search(criterias=criteria_data, limit=query.limit, offset=query.offset)  # type: ignore
    if query.data_response:
        data_response = query.data_response.split(",")
        for value in loans:
            list_loans = {}
            for value_data_response in data_response:
                list_loans[value_data_response] = getattr(value, value_data_response)
            loan_json.append(list_loans)
    else:
        for value in loans:
            loan_json.append(get_json_loan(loan=value))

    return loan_json


def get_client(
    query: queries.GetClientId,
    mambu: podemos_mambu.PodemosMambu,
) -> Dict:
    client = mambu.clients.get(id=query.id)
    client_json = get_json_client(client=client)  # type: ignore

    return client_json


def get_loan(
    query: queries.GetLoanId,
    mambu: podemos_mambu.PodemosMambu,
) -> Dict:
    loan = mambu.loans.get(id=query.id)
    loan_json = get_json_loan(loan=loan)  # type: ignore

    return loan_json


def get_group(
    query: queries.GetGroupId,
    mambu: podemos_mambu.PodemosMambu,
) -> Dict:
    group = mambu.groups.get(id=query.id)
    group_json = get_json_group(group=group)

    return group_json


QUERY_HANDLERS = {
    queries.GetGroup: get_groups,
    queries.GetClient: get_clients,
    queries.GetLoan: get_loans,
    queries.GetClientId: get_client,
    queries.GetLoanId: get_loan,
    queries.GetGroupId: get_group,
}  # type: Dict[Type[domain.Query], Callable]


COMMAND_HANDLERS = {}  # type: ignore


EVENT_HANDLERS = {}  # type: ignore
