from locust import task

from stress_tests.users_test import MobileUser, WebUser


class UserSepomexMobile(MobileUser):
    @task
    def get_estados(self):
        with self.rest("GET", "/sepomex/estados", json={}) as response:
            assert response.js["data"]


class UserSepomexWeb(WebUser):
    @task
    def get_municipios(self):
        qry_params = "?estado=Tlaxcala"
        with self.rest("GET", f"/sepomex/municipios{qry_params}", json={}) as response:
            assert response.js["data"]
