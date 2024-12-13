import pytest
from flask import g

from setup import sessions
from setup.adapters import podemos_mambu as pm


def fake_loan(entid, detailsLevel, get_entities):
    from mambupy.api.mambuloan import MambuLoan

    loan = MambuLoan()
    loan.id = "123"
    loan.encodedKey = "ABCD"
    return loan


def test_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    Loans = pm.Loans()

    mock_loan = Loans.get(123)

    mock_loan.write({"loan_amount": 80000.0, "account_state": "APPROVED"})

    mock_loan._instance_mambu.patch.assert_called_with(fields=["loanAmount"])

    mock_loan._mode = pm.Mode.ORM
    with pytest.raises(Exception) as e:
        assert mock_loan.write({"hello": "world"})
    assert "ORM mode does not support write operations" == str(e.value)


def test_loans_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans.write")
    Loans = pm.Loans()
    mock_loan = Loans.get(123)

    mock_loan.write({"amount": 80000.0, "status": "APPROVED"})

    mock_loan.write.assert_called_with({"amount": 80000.0, "status": "APPROVED"})


def test_groups_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans.write")
    Groups = pm.Groups()
    mock_group = Groups.get("LAS BIENPORTADAS")

    mock_group.write({"group_name": "LAS FASCINEROSAS"})

    mock_client.write.assert_called_with({"group_name": "LAS FASCINEROSAS"})


def test_clients_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Loans.write")
    Clients = pm.Clients()
    mock_client = Clients.get("ABC123")

    mock_client.write({"firstName": "FULANITA"})

    mock_client.write.assert_called_with({"firstName": "FULANITA"})


def test_loans_get(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.MambuModel.get")
    loan = pm.Loans.get("LOAN123")
    assert loan is not None
    pm.MambuModel.get.assert_called_with("LOAN123")


def test_clients_get(mocker):
    mock_model_rest = mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    client = pm.Clients.get("ABC123")
    assert client is not None
    mock_model_rest.get.assert_called_with(
        entid="ABC123", detailsLevel="FULL", get_entities=False
    )


def test_groups_search(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    group = pm.Groups.search("GRP123")
    assert group is not None
    pm.MambuModel.search.assert_called_with("GRP123")


def test_loans_search(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.search")

    loan = pm.Loans.search([("loan_amount", "=", 70000)])

    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "loanAmount",
                "operator": "EQUALS",
                "value": 70000,
            }
        ],
        sortingCriteria=None,
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_clients_search(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest.search")
    client = pm.Clients.search([("first_name", "=", "Simpsons")], orderby="state desc")

    assert client is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "firstName",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": "Simpsons",
            }
        ],
        sortingCriteria={
            "field": "state",
            "order": "DESC",
        },
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_groups_search(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest.search")
    group = pm.Groups.search(
        [
            (
                "loan_cycle",
                "=",
                2,
            )
        ],
        orderby="group_name",
    )
    assert group is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "loanCycle",
                "operator": "EQUALS",
                "value": 2,
            }
        ],
        sortingCriteria={
            "field": "groupName",
            "order": "ASC",
        },
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_centres_search(mocker):
    mock_get_all = mocker.patch(
        "setup.adapters.podemos_mambu.Centres._model_rest.get_all"
    )
    centre = pm.Centres.search(
        [
            (
                "assigned_branch_key",
                "=",
                "8a818e147d52a9a3017d52febb191ad0",
            )
        ]
    )
    assert centre is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_branches_search(mocker):
    def fakes_branches(
        offset,
        limit,
        paginationDetails,
        detailsLevel,
    ):
        from mambupy.api.mambubranch import MambuBranch

        list_branches = []
        for i in range(10):
            b = MambuBranch()
            b.id = f"123{i}"
            if i % 2 == 1:
                b.name = f"AZD-{i}"
            list_branches.append(b)
        return list_branches

    mock_get_all = mocker.patch(
        "setup.adapters.podemos_mambu.Branches._model_rest.get_all",
        side_effect=fakes_branches,
    )

    branches = pm.Branches.search(
        [
            (
                "name",
                "=",
                "AZD-7",
            )
        ]
    )
    assert branches is not None
    assert len(branches) > 0
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_products_search(mocker):
    mock_get_all = mocker.patch(
        "setup.adapters.podemos_mambu.Products._model_rest.get_all"
    )

    product = pm.Products.search(
        [
            (
                "allow_custom_repayment_allocation",
                "=",
                False,
            )
        ]
    )
    assert product is not None

    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    product = pm.Products.search(
        [
            (
                "creation_date",
                "=",
                "2020/04/01",
            )
        ]
    )

    assert product is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    product = pm.Products.search(
        [
            (
                "creation_date",
                "=",
                "2020/04/01",
            )
        ]
    )

    mock_get_all.side_effect = TypeError(
        "get_all() got an unexpected keyword argument 'detailsLevel'"
    )

    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_tasks_search(mocker):
    mock_get_all = mocker.patch("setup.adapters.podemos_mambu.Tasks._model_rest.get_all")
    task = pm.Tasks.search(
        [
            (
                "status",
                "=",
                "T1",
            )
        ]
    )
    assert task is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_transactions_search(mocker):
    mock_search = mocker.patch(
        "setup.adapters.podemos_mambu.Transactions._model_rest.search"
    )

    transaction = pm.Transactions.search(
        [
            (
                "value_date",
                "=",
                "16/02/2021",
            )
        ],
    )
    assert transaction is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "valueDate",
                "operator": "ON",
                "value": "16/02/2021",
            }
        ],
        sortingCriteria=None,
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_users_search(mocker):
    mock_get_all = mocker.patch("setup.adapters.podemos_mambu.Users._model_rest.get_all")
    user = pm.Users.search(
        [
            (
                "last_name",
                "startwith",
                "Luis",
            )
        ],
    )
    assert user is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    user = pm.Users.search(
        [
            (
                "creation_date",
                "<",
                "2022/04/02",
            )
        ],
    )
    assert user is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    user = pm.Users.search(
        [
            (
                "creation_date",
                "between",
                "2021/04/02",
                "2022/04/02",
            )
        ],
    )
    assert user is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    user = pm.Users.search(
        [
            (
                "first_name",
                "=",
                "Luis",
            )
        ],
    )
    assert user is not None
    mock_get_all.assert_called_with(
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_loans_write_set_state(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    Loans = pm.Loans()
    mock_loan = Loans.get(123)
    mock_loan.account_state = "PENDING_APPROVAL"

    mock_loan.write(data={"account_state": "APPROVE", "notes": "Approved via API"})
    mock_loan._instance_mambu.set_state.assert_called_with(
        action="APPROVE", notes="Approved via API"
    )
    mock_loan._instance_mambu.patch.assert_called_with(fields=[])

    mock_loan._instance_mambu.set_state.reset_mock()
    mock_loan.write(data={"account_state": "APPROVE"})
    mock_loan._instance_mambu.set_state.assert_called_with(
        action="APPROVE", notes="Updated via API"
    )


def test_save(mocker):
    update_mock = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.update")
    create_mock = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.create")
    mock_loan = pm.Loans()
    mock_loan.loan_name = "Credito 1"
    mock_loan._instance_mambu.encodedKey = None
    mock_loan.save()
    assert update_mock.call_count == 0
    create_mock.assert_called_with()

    mocker.patch(
        "setup.adapters.podemos_mambu.Loans._model_rest.get",
        side_effect=fake_loan,
    )

    mock_loan = pm.Loans.get(123)
    mock_loan.loan_name = "Credito 1"

    update_mock.reset_mock()
    create_mock.reset_mock()

    mock_loan.save()
    assert create_mock.call_count == 0
    update_mock.assert_called_with()

    assert mock_loan.loan_name == mock_loan._instance_mambu.loanName
    mock_loan._mode = pm.Mode.ORM
    with pytest.raises(Exception) as e:
        assert mock_loan.save()
    assert "ORM mode does not support update/save operations" == str(e.value)


def test_loans_save(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.MambuModel.save")
    Loans = pm.Loans()
    mock_loan = Loans.get(123)
    mock_loan.loan_name = "CREDITO 1"

    mock_loan.save()

    pm.MambuModel.save.assert_called_with()


def test_groups_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.MambuModel.save")
    Groups = pm.Groups()
    mock_group = Groups.get("G1")
    mock_group.group_name = "LAS BIENPORTADAS"

    mock_group.save()

    pm.MambuModel.save.assert_called_with()


def test_clients_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.MambuModel.save")
    Clients = pm.Clients()
    mock_client = Clients.get("ABC123")
    mock_client.first_name = "PEDRO"
    mock_client.save()
    pm.MambuModel.save.assert_called_with()


def test_centres_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Centres._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.MambuModel.save")
    mock_centre = pm.Centres.get("ABC123")
    mock_centre.name = "ABC123"
    mock_centre.save()
    pm.MambuModel.save.assert_called_with()


def test_branches_write(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Branches._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.MambuModel.save")
    mock_branch = pm.Branches.get("ABC123")
    mock_branch.name = "ABC123"
    mock_branch.save()
    pm.MambuModel.save.assert_called_with()


def test_loans_to_dict():
    loan = pm.Loans()
    loan.loan_name = "Credito 1"
    loan.account_state = "Open"
    d = loan.to_dict()
    assert isinstance(d, dict)
    assert "id" in d
    assert "account_state" in d
    assert loan.loan_name == d.get("loan_name")


def test_loan_update_readonly(mocker):

    mocker.patch(
        "setup.adapters.podemos_mambu.Loans._model_rest.get",
        side_effect=fake_loan,
    )

    loan = pm.Loans.get("123")

    with pytest.raises(Exception) as e:
        loan.id = "ASD1"
    assert "The attribute 'id' of 'Loans" in str(e.value)

    loan = pm.Loans.get("123")

    loan.loan_name = "Credito 1"
    assert not loan._violations_readonly_rule
    assert loan._instance_mambu.loanName == "Credito 1"


def test_loan_not_exist_fields(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    loan = pm.Loans.get("ABC123")

    with pytest.raises(Exception) as e:
        loan.hola = "hola"
    assert "The attribute 'hola' not exist in 'Loans'" in str(e.value)


def test_full_name(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")

    mock_client = pm.Clients.get("ABC123")

    mock_client.first_name = "FULANITA"
    mock_client.middle_name = "DE TAL"
    mock_client.last_name = "FLORES"

    assert mock_client.full_name == "FULANITA DE TAL FLORES"


def test_full_name_without_middle_name(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mock_client = pm.Clients.get("ABC123")

    mock_client.first_name = "FULANITA"
    mock_client.middle_name = None
    mock_client.last_name = "FLORES"

    assert mock_client.full_name == "FULANITA FLORES"


def test_vo_not_support_methods(mocker):
    with pytest.raises(Exception) as e:
        pm.Addresses.get("123")
    assert "This object 'Addresses' is a VO, not support get operation" == str(e.value)
    with pytest.raises(Exception) as e:
        pm.Addresses.search(
            [
                (
                    "city",
                    "=",
                    "CDMX",
                )
            ]
        )
    assert "This object 'Addresses' is a VO, not support search operations" == str(
        e.value
    )


def test_search_faileds():
    with pytest.raises(Exception) as e:
        user = pm.Users.search(None)
    assert "criterias search, only supports a list with at least one criterias" == str(
        e.value
    )
    with pytest.raises(Exception) as e:
        user = pm.Users.search(
            [
                (
                    "field_x",
                    "=",
                    "Luis",
                )
            ],
        )
    assert "Criteria not valid, the field 'field_x' not exist in entity Users" == str(
        e.value
    )

    with pytest.raises(Exception) as e:
        group = pm.Groups.search(
            [
                (
                    "group_name",
                    "=",
                )
            ],
        )
    assert (
        "Criteria not valid ('group_name', '='), please use an valid format ('field', 'operation', 'value') or ('field', 'operation', 'value', 'second_value')"
        == str(e.value)
    )

    with pytest.raises(Exception) as e:
        loan = pm.Loans.search(
            [
                (
                    "loan_amount",
                    "between",
                    7000,
                )
            ],
        )
    assert (
        "Criteria not valid, the operation 'between' required 4 items ('field', 'between', 'value', 'second_value')"
        == str(e.value)
    )

    with pytest.raises(Exception) as e:
        centre = pm.Centres.search(
            [
                (
                    "state",
                    "in",
                    "hola",
                )
            ],
        )
    assert "Criteria not valid, the operation 'in' required a list values" == str(e.value)

    with pytest.raises(Exception) as e:
        centre = pm.Centres.search(
            [
                (
                    "state",
                    "=",
                    "hola",
                )
            ],
            orderby="name inverso",
        )
    assert "arg sortby not valid, invalid order 'inverso'" == str(e.value)


def test_groups_add_comment(mocker):
    mock_comment = mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest.comment")
    mock_group = pm.Groups()
    mock_group.comments = []

    mock_group.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_group._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_group.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_clients_add_comment(mocker):
    mock_comment = mocker.patch(
        "setup.adapters.podemos_mambu.Clients._model_rest.comment"
    )
    mock_client = pm.Clients()
    mock_client.comments = []

    mock_client.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_client._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_client.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_loans_add_comment(mocker):
    mock_comment = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.comment")
    mock_loan = pm.Loans()
    mock_loan.comments = []

    mock_loan.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_loan._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_loan.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_branches_add_comment(mocker):
    mock_comment = mocker.patch(
        "setup.adapters.podemos_mambu.Branches._model_rest.comment"
    )
    mock_branch = pm.Branches()
    mock_branch.comments = []

    mock_branch.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_branch._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_branch.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_centres_add_comment(mocker):
    mock_comment = mocker.patch(
        "setup.adapters.podemos_mambu.Centres._model_rest.comment"
    )

    mock_centre = pm.Centres()
    mock_centre.comments = []

    mock_centre.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_centre._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_centre.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_users_add_comment(mocker):
    mock_comment = mocker.patch("setup.adapters.podemos_mambu.Users._model_rest.comment")
    mock_user = pm.Users()
    mock_user.comments = []

    mock_user.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_user._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_user.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_products_add_comment(mocker):
    mock_comment = mocker.patch(
        "setup.adapters.podemos_mambu.Products._model_rest.comment"
    )
    mock_product = pm.Products()
    mock_product.comments = []

    mock_product.add_comment("If I would, would you?")

    mock_comment.assert_called_with("If I would, would you?")

    mock_product._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_product.add_comment("something")
    assert "ORM mode does not support write operations" in str(e.value)


def test_search_today(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.search")
    loan = pm.Loans.search_today(
        "creation_date",
        [
            (
                "account_state",
                "=",
                "ACTIVE",
            )
        ],
    )
    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "creationDate",
                "operator": "TODAY",
            },
            {
                "field": "accountState",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": "ACTIVE",
            },
        ],
        sortingCriteria=None,
        detailsLevel="FULL",
    )


def test_search_this_week(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.search")
    loan = pm.Loans.search_this_week(
        "last_modified_date",
        [
            (
                "account_state",
                "=",
                "ACTIVE",
            )
        ],
        "approved_date desc",
    )
    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "lastModifiedDate",
                "operator": "THIS_WEEK",
            },
            {
                "field": "accountState",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": "ACTIVE",
            },
        ],
        sortingCriteria={
            "field": "approvedDate",
            "order": "DESC",
        },
        detailsLevel="FULL",
    )


def test_search_this_month(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.search")
    loan = pm.Loans.search_this_month(
        "last_modified_date",
        [
            (
                "account_state",
                "=",
                "ACTIVE",
            )
        ],
        "approved_date",
    )
    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "lastModifiedDate",
                "operator": "THIS_MONTH",
            },
            {
                "field": "accountState",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": "ACTIVE",
            },
        ],
        sortingCriteria={
            "field": "approvedDate",
            "order": "ASC",
        },
        detailsLevel="FULL",
    )


def test_search_this_year(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.search")
    loan = pm.Loans.search_this_year(
        "creation_date",
        [
            (
                "account_state",
                "=",
                "ACTIVE",
            )
        ],
    )
    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "creationDate",
                "operator": "THIS_YEAR",
            },
            {
                "field": "accountState",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": "ACTIVE",
            },
        ],
        sortingCriteria=None,
        detailsLevel="FULL",
    )


def test_search_dates_faileds():
    with pytest.raises(Exception) as e:
        user = pm.Users.search_today("cretaion_date")
    assert "This object 'Users' is a entity with out support search operations" == str(
        e.value
    )
    with pytest.raises(Exception) as e:
        user = pm.Users.search_this_week("cretaion_date")
    assert "This object 'Users' is a entity with out support search operations" == str(
        e.value
    )
    with pytest.raises(Exception) as e:
        user = pm.Users.search_this_month("cretaion_date")
    assert "This object 'Users' is a entity with out support search operations" == str(
        e.value
    )
    with pytest.raises(Exception) as e:
        user = pm.Users.search_this_year("cretaion_date")
    assert "This object 'Users' is a entity with out support search operations" == str(
        e.value
    )
    with pytest.raises(Exception) as e:
        user = pm.Loans.search_today(
            1,
        )
    assert "date_field, should str" == str(e.value)
    with pytest.raises(Exception) as e:
        user = pm.Loans.search_today(
            "activation_transaction_key",
        )
    assert (
        "the field 'activation_transaction_key' not is type date or datetime in the class 'Loans'"
        == str(e.value)
    )


def test_clients_search_custom_field(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest.search")
    client = pm.Clients.search(
        [("profesion_clients", "=", "Vendedora")], orderby="state desc"
    )

    assert client is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "_customfields_integrante.Profesion_Clients",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": "Vendedora",
            }
        ],
        sortingCriteria={
            "field": "state",
            "order": "DESC",
        },
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_loans_search_custom_field(mocker):
    mock_search = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.search")
    loan = pm.Loans.search([("renovacion_loan_accounts", "=", 3)])

    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "_autorizacionoperativa_loan.Renovacion_Loan_Accounts",
                "operator": "EQUALS",
                "value": 3,
            }
        ],
        sortingCriteria=None,
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    loan = pm.Loans.search([("creation_date", "between", "2022-11-20", "2022-12-20")])

    assert loan is not None
    mock_search.assert_called_with(
        filterCriteria=[
            {
                "field": "creationDate",
                "operator": "BETWEEN",
                "value": "2022-11-20",
                "secondValue": "2022-12-20",
            }
        ],
        sortingCriteria=None,
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_loans_get_with_user(token_user, mocker):

    g.user = sessions.User("user.fake", "user.fake@fakedomain.com")
    mock_get = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.get")

    loan = pm.Loans.get("LOAN123")
    assert loan is not None
    mock_get.assert_called_with(
        entid="LOAN123",
        detailsLevel="FULL",
        get_entities=False,
        user="user.fake",
        pwd="FakeP455",
    )


def test_loans_approve(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    Loans = pm.Loans()
    mock_loan = Loans.get(123)
    mock_loan.account_state = "PENDING_APPROVAL"

    mock_loan.approve(notes="Approved via API")
    mock_loan._instance_mambu.approve.assert_called_with(notes="Approved via API")

    mock_loan._instance_mambu.approve.reset_mock()
    mock_loan.account_state = "CLOSED"
    with pytest.raises(Exception) as e:
        assert mock_loan.approve(notes="Approved via API")
    assert "with state 'CLOSED', is a state not valid to approve" in str(e.value)

    mock_loan._instance_mambu.approve.reset_mock()
    mock_loan._mode = "ORM"
    mock_loan.account_state = "PENDING_APPROVAL"
    with pytest.raises(Exception) as e:
        assert mock_loan.approve(notes="Approved via API")
    assert "ORM mode does not support write operations" in str(e.value)


def test_loans_disburse(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")

    Loans = pm.Loans()
    mock_loan = Loans.get(123)
    mock_loan.account_state = "APPROVED"

    mock_loan.disburse(notes="disbursed via API")
    mock_loan._instance_mambu.disburse.assert_called_with(
        notes="disbursed via API", firstRepaymentDate=None, disbursementDate=None
    )

    mock_loan._instance_mambu.disburse.reset_mock()
    mock_loan.account_state = "PENDING_APPROVAL"
    with pytest.raises(Exception) as e:
        assert mock_loan.disburse(notes="disbursed via API")
    assert "with state 'PENDING_APPROVAL', is a state not valid to disburse" in str(
        e.value
    )

    mock_loan._instance_mambu.disburse.reset_mock()
    mock_loan._mode = "ORM"
    mock_loan.account_state = "APPROVED"
    with pytest.raises(Exception) as e:
        assert mock_loan.approve(notes="disbursed via API")
    assert "ORM mode does not support write operations" in str(e.value)


def test_loan_transactions(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mock_search_transactions = mocker.patch(
        "setup.adapters.podemos_mambu.Transactions._model_rest.search"
    )

    mock_loan = pm.Loans.get(123)

    mock_loan.transactions
    mock_search_transactions.assert_called_with(
        filterCriteria=[
            {
                "field": "parentAccountKey",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": mock_loan.encoded_key,
            }
        ],
        sortingCriteria=None,
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )

    new_loan = pm.Loans()
    transactions = new_loan.transactions
    assert transactions == []


def test_attach_document(mocker):
    mock_attach_document = mocker.patch(
        "setup.adapters.podemos_mambu.Clients._model_rest.attach_document"
    )
    mock_client = pm.Clients()

    mock_client.attach_document("/tmp/curp.pdf", "curp", "mambu api")

    mock_attach_document.assert_called_with("/tmp/curp.pdf", "curp", "mambu api")

    mock_client._mode = "ORM"
    with pytest.raises(Exception) as e:
        assert mock_client.attach_document("something")
    assert "ORM mode does not support write operations" in str(e.value)

    mock_centre = pm.Centres()
    with pytest.raises(Exception) as e:
        assert mock_centre.attach_document("/tmp/curp.pdf", "curp", "mambu api")
    assert "'Centres' is a entity with out support documents" in str(e.value)


def test_clients_update_risk(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Clients._model_rest")
    mock_client = pm.Clients.get("123")

    from setup.adapters.mambu_models.clients import Risk

    mock_client.update_risk(Risk.low)
    mock_client._instance_mambu.patch.assert_called_with(
        fields=["niveles_riesgo_clientes"]
    )


def test_loan_get_installments(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mock_loan = pm.Loans.get("1234")
    mock_loan.installments
    mock_loan._instance_mambu.get_schedule.assert_called_with()


def test_group_previous_loans(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Groups._model_rest")
    mock_search_loans = mocker.patch(
        "setup.adapters.podemos_mambu.Loans._model_rest.search"
    )

    mock_group = pm.Groups.get("1234")
    mock_group.previous_loans

    mock_search_loans.assert_called_with(
        filterCriteria=[
            {
                "field": "accountHolderKey",
                "operator": "EQUALS_CASE_SENSITIVE",
                "value": mock_group.encoded_key,
            }
        ],
        sortingCriteria=None,
        offset=None,
        limit=None,
        paginationDetails="OFF",
        detailsLevel="FULL",
    )


def test_clients_search_by_curp(mocker):
    mock_get_all = mocker.patch(
        "setup.adapters.podemos_mambu.Clients._model_rest.get_all"
    )
    client = pm.Clients.search_by_curp("VAMV731224MDFNNC10")
    assert client is not None
    mock_get_all.assert_called_with(filters={"idNumber": "VAMV731224MDFNNC10"})


def test_loans_search_by_tribu(mocker):
    mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest")
    mocker.patch("setup.adapters.podemos_mambu.Centres._model_rest")
    mock_get_all = mocker.patch("setup.adapters.podemos_mambu.Loans._model_rest.get_all")
    mock_get = mocker.patch("setup.adapters.podemos_mambu.Loans.get")

    mock_centre = pm.Centres(name="TribuTI")
    mock_loan = pm.Loans(id="1234", assigned_centre=mock_centre)
    mock_get_all.return_value = [mock_loan]
    mock_get.return_value = mock_loan
    loan = pm.Loans.search_by_tribu(centre_id="TribuTI", limit=10, offset=10)

    mock_get_all.assert_called_with(filters={"centreId": "TribuTI"}, limit=10, offset=10)
    assert loan is not None
    assert loan[0].assigned_centre.name == "TribuTI"
