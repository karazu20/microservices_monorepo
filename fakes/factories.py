from factory import Factory, Faker, Sequence

from src.sepomex.domain.models import Colonia, Estado, Municipio
from src.validations.domain.models import Rule


class ColoniaFactory(Factory):
    class Meta:
        model = Colonia

    id = Sequence(lambda n: 1000 + n)
    nombre = Faker("name")
    ciudad = Faker("city")
    asentamiento = Faker("city")
    codigo_postal = "15987"


class MunicipioFactory(Factory):
    class Meta:
        model = Municipio

    id = Sequence(lambda n: 1000 + n)
    nombre = Faker("city")


class EstadoFactory(Factory):
    class Meta:
        model = Estado

    id = Sequence(lambda n: 1000 + n)
    nombre = Faker("city")


class RuleFactory(Factory):
    class Meta:
        model = Rule

    regla = "group_risk"
