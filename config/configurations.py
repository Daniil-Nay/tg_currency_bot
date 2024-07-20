from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass
class Database:
    redis_host: str
    redis_port: int
    password: str


@dataclass
class TgBot:
    token: str
    creator_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: Database


def load_config() -> Config:
    load_dotenv()
    tg_bot = TgBot(
        token=getenv("BOT_API_KEY"),
        creator_id=int(getenv("CREATOR_ID"))
    )

    db = Database(
        redis_host=getenv("REDIS_HOST"),
        redis_port=int(getenv("REDIS_PORT")),
        password=getenv("PASSWORD", None)
    )
    return Config(tg_bot=tg_bot,
                  db=db
                  )
