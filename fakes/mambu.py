from factory import Factory, Faker, fuzzy

from setup.adapters.mambu_models import *


class ModelFake:
    @classmethod
    def add(cls, obj):
        cls._objects_mambu.append(obj)

    @classmethod
    def get(cls, id, mode="REST"):
        _object = next(
            (obj for obj in cls._objects_mambu if obj.id == id or obj.encoded_key == id),
            None,
        )
        if not _object:
            raise Exception
        return _object

    @classmethod
    def search(
        cls,
        criterias,
        mode="REST",
        sorting_criteria=None,
        offset=None,
        limit=None,
        pagination_details="OFF",
        details_level="BASIC",
    ):
        return cls._objects_mambu

    @classmethod
    def search_by_curp(
        cls,
        mode="REST",
    ):
        return cls._objects_mambu

    @classmethod
    def search_by_tribu(
        cls,
        centre_id,
        limit,
        offset,
        mode="REST",
    ):
        return cls._objects_mambu


class VOFake:
    @classmethod
    def add(cls, obj):
        cls._objects_mambu.append(obj)


class AddressesFake(Factory, VOFake):
    class Meta:
        model = Addresses
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)
    city = fuzzy.FuzzyText(length=100)
    region = fuzzy.FuzzyText(length=100)
    line_1 = fuzzy.FuzzyText(length=100)
    line_2 = fuzzy.FuzzyText(length=100)

    _objects_mambu = []


class DocumentsFake(Factory, VOFake):
    class Meta:
        model = Documents
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)
    file_name = fuzzy.FuzzyText(length=100)

    _objects_mambu = []


class IDDocumentsFake(Factory, VOFake):
    class Meta:
        model = IDDocuments
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)
    client_key = fuzzy.FuzzyText(length=100)
    document_id = fuzzy.FuzzyText(length=30)
    document_type = fuzzy.FuzzyText(length=30)

    _objects_mambu = []


class DisbursementsDetailsFake(Factory, VOFake):
    class Meta:
        model = DisbursementsDetails
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)

    _objects_mambu = []


class InstallmentsFake(Factory, VOFake):
    class Meta:
        model = Installments
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)

    _objects_mambu = []


class GroupRolesFake(Factory, VOFake):
    class Meta:
        model = GroupRoles
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)
    group_role_name_key = fuzzy.FuzzyText(length=100)
    role_name = fuzzy.FuzzyText(length=100)
    role_name_id = fuzzy.FuzzyText(length=100)
    _objects_mambu = []


class GroupMembersFake(Factory, VOFake):
    class Meta:
        model = GroupMembers
        exclude = ("_objects_mambu",)

    encoded_key = fuzzy.FuzzyText(length=8)
    client_key = fuzzy.FuzzyText(length=100)
    roles = []

    _objects_mambu = []


class UserRolesFake(Factory, VOFake):
    class Meta:
        model = UserRoles
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=8)
    encoded_key = fuzzy.FuzzyText(length=8)

    _objects_mambu = []


class CentresFake(Factory, ModelFake):
    class Meta:
        model = Centres
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    @classmethod
    def get(cls, id, mode="REST"):
        try:
            _object = super().get(id, mode)
        except Exception:
            _object = next(
                (obj for obj in cls._objects_mambu if obj.name == id),
                None,
            )
        if not _object:
            raise Exception
        return _object

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class ProductsFake(Factory, ModelFake):
    class Meta:
        model = Products
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class GroupsFake(Factory, ModelFake):
    class Meta:
        model = Groups
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")
    assigned_centre = CentresFake(id="123", name="NIDO")
    group_members = []

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class LoansFake(Factory, ModelFake):
    class Meta:
        model = Loans
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")
    account_holder = GroupsFake(id="123")
    product_type = ProductsFake(id="123")

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True

    def update_state(action="APPROVE", notes="Approved via API"):
        return True


class ClientsFake(Factory, ModelFake):
    class Meta:
        model = Clients
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    last_name = Faker("name")
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class BranchesFake(Factory, ModelFake):
    class Meta:
        model = Branches
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class TasksFake(Factory, ModelFake):
    class Meta:
        model = Tasks
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class TransactionsFake(Factory, ModelFake):
    class Meta:
        model = Transactions
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class UsersFake(Factory, ModelFake):
    class Meta:
        model = Users
        exclude = ("_objects_mambu",)

    id = fuzzy.FuzzyText(length=5)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []

    @classmethod
    def get(cls, id, mode="REST"):
        try:
            _object = super().get(id, mode)
        except Exception:
            _object = next(
                (obj for obj in cls._objects_mambu if obj.username == id),
                None,
            )
        if not _object:
            raise Exception
        return _object

    def write(data: dict) -> bool:
        for k, v in data.items():
            setattr(self, k, v)
        return True

    def save():
        return True


class CommentsFake(Factory, ModelFake):
    class Meta:
        model = Comments
        exclude = ("_objects_mambu",)

    owner_key = fuzzy.FuzzyText(length=8)
    owner_type = fuzzy.FuzzyText(length=8)
    text = fuzzy.FuzzyText(length=20)
    user_key = fuzzy.FuzzyText(length=8)
    encoded_key = fuzzy.FuzzyText(length=8)
    creation_date = Faker("date_this_year")
    last_modified_date = Faker("date_this_year")

    _objects_mambu = []
