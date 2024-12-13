from __future__ import annotations  # type: ignore

import abc
from typing import Any

from setup.adapters.mambu_models import (
    Addresses,
    Branches,
    Centres,
    Clients,
    Comments,
    DisbursementsDetails,
    Documents,
    GroupMembers,
    GroupRoles,
    Groups,
    IDDocuments,
    Installments,
    Loans,
    Products,
    Tasks,
    Transactions,
    UserRoles,
    Users,
)

from setup.adapters.mambu_models import Mode, Details, MambuModel  # isort:skip


class AbstractMambu(abc.ABC):
    loans: Any = NotImplemented
    groups: Any = NotImplemented
    clients: Any = NotImplemented
    centres: Any = NotImplemented
    branches: Any = NotImplemented
    products: Any = NotImplemented
    tasks: Any = NotImplemented
    transactions: Any = NotImplemented
    users: Any = NotImplemented

    addresses: Any = NotImplemented
    documents: Any = NotImplemented
    id_documents: Any = NotImplemented
    disbursements_details: Any = NotImplemented
    group_members: Any = NotImplemented
    group_roles: Any = NotImplemented
    user_roles: Any = NotImplemented
    comments: Any = NotImplemented
    installments: Any = NotImplemented


class PodemosMambu(AbstractMambu):

    loans = Loans
    groups = Groups
    clients = Clients
    centres = Centres
    branches = Branches
    products = Products
    tasks = Tasks
    transactions = Transactions
    users = Users

    addresses = Addresses
    documents = Documents
    id_documents = IDDocuments
    disbursements_details = DisbursementsDetails
    group_members = GroupMembers
    group_roles = GroupRoles
    user_roles = UserRoles
    comments = Comments
    installments = Installments
