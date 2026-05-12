from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

from app.db.base import Base
from app.core.config import DATABASE_URL

# importa tutti i modelli (IMPORTANTE per autogenerate)
from app.models.user import User
from app.models.workspace import Workspace
from app.models.membership import Membership
from app.models.project import Project
from app.models.skill import Skill
from app.models.task import Task
from app.models.project_skill import project_skills
from app.models.workspace_invitation import WorkspaceInvitation 


# Alembic config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata
target_metadata = Base.metadata


# 🔹 OFFLINE MODE
def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# 🔹 ONLINE MODE
def run_migrations_online() -> None:
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
