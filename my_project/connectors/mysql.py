"""MySQL Connector.

Manages interactions with MySQL.

"""

from contextlib import contextmanager
# import functools

# from oto import response
# from pynamodb.exceptions import PynamoDBException
from sqlalchemy import create_engine
# from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from my_project import config
# from my_project.connectors import sentry


# please don't use the following private variables directly;
# use db_session
_db_engine = create_engine(
    config.DB_URL, poolclass=config.POOL_CLASS, encoding='utf-8')
_db_session = sessionmaker(bind=_db_engine)

BaseModel = declarative_base()


@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations.

    Taken from http://docs.sqlalchemy.org/en/latest/orm/session_basics.html.
    This handles rollback and closing of session, so there is no need
    to do that throughout the code.
    Usage:
        with db_session() as session:
            session.execute(query)
    """
    session = _db_session()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
