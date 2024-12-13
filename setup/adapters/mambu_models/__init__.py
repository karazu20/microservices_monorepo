from setup.adapters.mambu_models.addresses import Addresses
from setup.adapters.mambu_models.branches import Branches
from setup.adapters.mambu_models.centres import Centres
from setup.adapters.mambu_models.clients import Clients
from setup.adapters.mambu_models.comments import Comments
from setup.adapters.mambu_models.disbursements import DisbursementsDetails
from setup.adapters.mambu_models.documents import Documents
from setup.adapters.mambu_models.group_members import GroupMembers
from setup.adapters.mambu_models.group_roles import GroupRoles
from setup.adapters.mambu_models.groups import Groups
from setup.adapters.mambu_models.id_documents import IDDocuments
from setup.adapters.mambu_models.installments import Installments
from setup.adapters.mambu_models.loans import Loans
from setup.adapters.mambu_models.model import Details, MambuModel, Mode
from setup.adapters.mambu_models.products import Products
from setup.adapters.mambu_models.tasks import Tasks
from setup.adapters.mambu_models.transactions import Transactions
from setup.adapters.mambu_models.user_roles import UserRoles
from setup.adapters.mambu_models.users import Users

__all__ = [
    "MambuModel",
    "Mode",
    "Details",
    "Branches",
    "Centres",
    "Loans",
    "Products",
    "Tasks",
    "Transactions",
    "Clients",
    "Groups",
    "Users",
    "Addresses",
    "Comments",
    "DisbursementsDetails",
    "Documents",
    "GroupMembers",
    "GroupRoles",
    "IDDocuments",
    "UserRoles",
    "Installments",
]
