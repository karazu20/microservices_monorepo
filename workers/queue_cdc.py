import redis
from rq import Connection, Worker

from setup import config


def main():
    # Provide queue names to listen to as arguments to this script,
    # similar to rq worker
    with Connection(redis.Redis(**config.get_redis_host_and_port())):
        w = Worker("cdc_queue", name="cdc_worker")
        w.work()


if __name__ == "__main__":
    main()
