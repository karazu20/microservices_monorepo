from locust.user.wait_time import between
from locust_plugins.users import RestUser


class MobileUser(RestUser):
    wait_time = between(0.5, 5)
    weight = 3
    abstract = True


class WebUser(RestUser):
    wait_time = between(0.5, 5)
    weight = 1
    abstract = True
