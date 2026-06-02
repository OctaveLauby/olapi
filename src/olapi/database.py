from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from olapi.settings import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
session_maker = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
