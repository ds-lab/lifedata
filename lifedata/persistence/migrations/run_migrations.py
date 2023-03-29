from alembic import command
from alembic.config import Config


def get_alembic_config() -> Config:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "lifedata.persistence:migrations")
    return alembic_cfg


def upgrade_to_head():
    alembic_config = get_alembic_config()
    command.upgrade(alembic_config, "head")
