from setup.adapters import podemos_mambu as pm


class ProductFake(object):
    def __init__(self, name):
        self.name = name


class CustomFieldsFake(object):
    """Class Fake CustomFields"""

    def __init__(self, id, value=None, name=None):
        self.id = id
        self.value = value
        self.name = name


class FieldValidationsFake(object):
    """Class Fake FieldValidation"""

    def __init__(self, id, regla_id, campo, requerido):
        self.id = id
        self.regla_id = regla_id
        self.campo = campo
        self.requerido = requerido


class RolesFake(object):
    """Class Fake Roles"""

    def __init__(self, id=1):
        self.id = id


class MambuGroupMemberFake(object):
    """Class Fake MambuGroupMember"""

    def __init__(self, role):
        roles_name = RolesFake(id=1)
        setattr(roles_name, "roleName", role)
        self.roles = [roles_name]


class MambuDocumentFake(object):
    """Class Fake MambuDocument"""

    def __init__(self, document_id, document_type):
        setattr(self, "documentId", document_id)
        setattr(self, "documentType", document_type)


class MambuAddressFake(object):
    """Class Fake MambuAddress"""

    def __init__(self, city, region, line1, line2):
        self.city = city
        self.region = region
        self.line1 = line1
        self.line2 = line2


class ValidationRuleDataFake(object):
    """Class Fake ValidationRuleData"""

    def __init__(self, id, llave, valor, tipo_dato):
        self.id = id
        self.llave = llave
        self.valor = valor
        self.tipo_dato = tipo_dato


def get_group(**kwargs):
    group = pm.Groups("123")
    mock_group = group.get("123")

    for value in kwargs.items():
        setattr(mock_group, value[0], value[1])

    return mock_group


def get_loan(**kwargs):
    loan = pm.Loans("12345")
    mock_loan = loan.get("12345")

    for value in kwargs.items():
        setattr(mock_loan, value[0], value[1])

    return mock_loan


def get_client(**kwargs):
    client = pm.Clients("OYH804")
    mock_client = client.get("OYH804")

    for value in kwargs.items():
        setattr(mock_client, value[0], value[1])

    return mock_client
