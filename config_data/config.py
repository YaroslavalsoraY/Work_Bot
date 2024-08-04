from dataclasses import dataclass
from environs import Env
from typing import Optional


@dataclass
class Work_Bot:
    token: str


@dataclass
class Config:
    tg_bot: Work_Bot


def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=Work_Bot(token=env('API_TOKEN')))
