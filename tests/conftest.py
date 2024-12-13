# pylint: disable=redefined-outer-name

import pytest
from sqlalchemy.orm import close_all_sessions

from setup.data_bases import PodemosDBs, engine_podemos, get_session
from src.cdc.adapters.orm import metadata as metadata_cdc
from src.groups.adapters.orm import metadata as metadata_groups
from src.loans_status.adapters.orm import metadata as metadata_loans_status
from src.nip.adapters.orm import metadata as metadata_nip
from src.pambu.adapters.orm import metadata as metadata_pambu
from src.sepomex.adapters.orm import metadata as metadata_sepomex
from src.storage.adapters.orm import metadata as metadata_storage
from src.validations.adapters.orm import metadata as metadata_validations


@pytest.fixture(scope="session")
def postgres_db():
    engine_utils = engine_podemos(PodemosDBs.utils)
    engine_pambu = engine_podemos(PodemosDBs.pambu)
    engine_validations = engine_podemos(PodemosDBs.validations)
    engine_digitalization = engine_podemos(PodemosDBs.digitalization)
    engine_documents = engine_podemos(PodemosDBs.documents)

    metadata_pambu.create_all(engine_pambu)
    metadata_sepomex.create_all(engine_utils)
    metadata_nip.create_all(engine_digitalization)
    metadata_cdc.create_all(engine_digitalization)
    metadata_groups.create_all(engine_digitalization)
    metadata_loans_status.create_all(engine_validations)
    metadata_validations.create_all(engine_validations)
    metadata_storage.create_all(engine_documents)

    yield

    metadata_pambu.drop_all(engine_pambu)
    metadata_sepomex.drop_all(engine_utils)
    metadata_cdc.drop_all(engine_digitalization)
    metadata_nip.drop_all(engine_digitalization)
    metadata_groups.drop_all(engine_digitalization)
    metadata_loans_status.drop_all(engine_validations)
    metadata_validations.drop_all(engine_validations)
    metadata_storage.drop_all(engine_documents)


@pytest.fixture(scope="session")
def pambu_session(postgres_db):
    yield get_session(PodemosDBs.pambu)()
    close_all_sessions()


@pytest.fixture(scope="session")
def digitalization_session(postgres_db):
    yield get_session(PodemosDBs.digitalization)()
    close_all_sessions()


@pytest.fixture(scope="session")
def validations_session(postgres_db):
    yield get_session(PodemosDBs.validations)()
    close_all_sessions()


@pytest.fixture(scope="session")
def app():
    from src.application import create_application

    return create_application(__name__, "test")


@pytest.fixture(scope="session")
def client(app):
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True, scope="session")
def app_context(app):
    testing_client = app.test_request_context()
    testing_client.push()
    yield app
    testing_client.pop()


@pytest.fixture(scope="function")
def mambu():
    from fakes.adapters import FakePodemosMambu

    yield FakePodemosMambu
    FakePodemosMambu.clear()


@pytest.fixture(scope="session")
def token_user(postgres_db):
    pambu_session = get_session(PodemosDBs.pambu)()
    from datetime import date

    from fakeredis import FakeStrictRedis

    from setup.adapters.cache import RedisCache

    token = "F4k3T0k3n12345"
    RedisCache.cache = FakeStrictRedis()

    user_name = "user.fake"
    email = "user.fake@fakedomain.com"
    RedisCache.set("user:token:" + str(token), str(email))
    RedisCache.set(
        "user:data:" + str(email),
        str(f'{{"username": "{user_name}", "email": "{email}"}}'),
    )

    nombre_ce = "Coordinador de Emprendedoras"
    r = pambu_session.execute(
        "INSERT INTO rol (nombre, nombre_corto, active, created, updated) VALUES (:nombre, :nombre_corto, :active, :created, :updated)",
        dict(
            nombre=nombre_ce,
            nombre_corto="CE",
            active=True,
            created=date.today(),
            updated=date.today(),
        ),
    )
    pambu_session.commit()
    pambu_session.execute(
        "INSERT INTO usuario (username, email, pass_mambu, active, created, updated, id_rol) VALUES (:username, :email, :pass_mambu, :active, :created, :updated, :id_roll)",
        dict(
            username=user_name,
            email=email,
            pass_mambu="KObfmZUOb7fwXu3cUcOl70Smk4nb/+tz/fuVqqpGs6U=",
            active=True,
            created=date.today(),
            updated=date.today(),
            id_roll=1,
        ),
    )
    pambu_session.commit()
    yield token
    RedisCache.cache.flushall()
    pambu_session.execute(
        "DELETE FROM usuario WHERE username = :username",
        dict(username=user_name),
    )
    pambu_session.execute(
        "DELETE FROM rol WHERE nombre = :nombre",
        dict(nombre=nombre_ce),
    )
    pambu_session.commit()
