import os

from pydantic import BaseSettings


class Environment(BaseSettings):
    model_path: str
    test_products_path: str


if "COMPOSE_PROJECT_NAME" in os.environ:
    environment = Environment(_env_file="prod.env")
else:
    environment = Environment(_env_file="local.env")
