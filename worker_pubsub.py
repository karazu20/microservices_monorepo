import json
import logging
import os
import time
from typing import Callable  # type: ignore

from dotenv import load_dotenv

from setup.adapters.bus import RedisBus
from setup.config import ROOT_PATH, Logs

logger = logging.getLogger(__name__)

load_dotenv()


directories_ms = os.listdir(f"{ROOT_PATH}/src")
for dir_ms in directories_ms:
    try:
        __import__(f"src.{dir_ms}.entrypoints.consumers")
    except ModuleNotFoundError:
        continue

env = os.environ.get("ENV", "prod")
Logs.config_logs(None, env)


def main():
    channels = [
        subcription.get("channel") for subcription in RedisBus.get_subscriptions()
    ]

    if channels:
        subscriptions = RedisBus.pubsubs(channels)

        while True:

            event = subscriptions.get_message()
            if event:
                consumer = list(
                    filter(
                        lambda sub, channel=event["channel"].decode("utf-8"): sub[
                            "channel"
                        ]
                        == channel,
                        RedisBus.get_subscriptions(),
                    )
                )
                try:
                    consumer[0]["consumer"](json.loads(event["data"]))
                    logger.info(
                        "Event:%s driven succes for handler %s",
                        event,
                        consumer[0]["consumer"],
                    )
                except Exception as e:
                    logger.error(
                        "Error to consumer event %s on handler %s, Error: %s",
                        event,
                        consumer[0]["consumer"],
                        e,
                    )

            time.sleep(0.001)  # be nice to the system


if __name__ == "__main__":
    main()
