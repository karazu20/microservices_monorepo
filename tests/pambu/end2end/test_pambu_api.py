from datetime import date

import pytest

from src.pambu import config


@pytest.fixture(scope="module")
def roles_usuario(pambu_session):
    rol_user = "rol_podemos"

    for i in range(1, 3):
        pambu_session.execute(
            "INSERT INTO rol (nombre, nombre_corto, active, created, updated) VALUES (:nombre, :nombre_corto, :active, :created, :updated)",
            dict(
                nombre=f"{rol_user}_{i}",
                nombre_corto=f"rol_{i}",
                active=True,
                created=date.today(),
                updated=date.today(),
            ),
        )
        pambu_session.commit()


@pytest.mark.usefixtures("postgres_db")
def test_create_user(client, mambu, roles_usuario):

    user = mambu.users.build(id="batman", username="batman", email="baticueva@testo.mx ")
    mambu.users.add(user)
    data = {"username": "batman", "email": "baticueva@testo.mx", "id_rol": "2"}
    url = config.get_api_url()
    response = client.post(f"{url}/pambu/new_user", json=data)
    assert response.status_code == 201

    data = {}
    response = client.get(f"{url}/pambu/new_user", json=data)
    assert response.status_code == 405


def test_get_release(client):

    url = config.get_api_url()
    response = client.post(f"{url}/pambu/app_last_version")
    assert response.status_code == 405

    response = client.get(f"{url}/pambu/app_last_version")
    assert response.status_code == 200
