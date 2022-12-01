import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

current_file = os.path.dirname(__file__)
engine = create_engine(f"sqlite:///{current_file}/luckydraw")
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
    print("We are connected to the DB successfully...")
