from dataclasses import dataclass
from data import cfg

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseConfig:
    db_host: str
    db_access: str
    db_access_key: str

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:
    return Config(
        tg_bot=TgBot(
            token=cfg.BOT_TOKEN,
            admin_ids=list(map(int, cfg.list_admin))),
        db=DatabaseConfig(
            db_host=cfg.USER_STORAGE_URL,
            db_access=cfg.AWS_ACCESS_KEY_ID,
            db_access_key=cfg.AWS_SECRET_ACCESS_KEY)
        )

