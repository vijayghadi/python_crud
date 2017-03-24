"""Application configuration."""

import logging
import os
import sys
import newrelic.agent
from sqlalchemy.pool import NullPool
from sqlalchemy.pool import StaticPool


# Service information
SERVICE_NAME = 'ows-app-name'
SERVICE_VERSION = '1.0.0'

# Production environment
PROD_ENVIRONMENT = 'prod'
DEV_ENVIRONMENT = 'dev'
QA_ENVIRONMENT = 'qa'
TEST_ENVIRONMENT = 'test'
ENVIRONMENT = os.environ.get('Environment', DEV_ENVIRONMENT)

if ENVIRONMENT == PROD_ENVIRONMENT:
    newrelic.agent.initialize('newrelic.ini')

# Errors and loggers
SENTRY = os.environ.get('SENTRY_DSN') or None
LOGGER_DSN = os.environ.get('LOGGER_DSN')
LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'ows1'

# Database credentials
'''DB_CREDENTIALS = {
    'database': os.environ.get('AR_MYSQL_DATABASE'),
    'host': os.environ.get('AR_MYSQL_HOST'),
    'password': os.environ.get('AR_MYSQL_PASSWORD'),
    'port': os.environ.get('AR_MYSQL_PORT'),
    'user': os.environ.get('AR_MYSQL_USER')
}'''

DB_CREDENTIALS = {
    'database': 'py_crud',
    'host': 'localhost',
    'password': '12345',
    'port': '3306',
    'user': 'root'
}

# Database config
if ENVIRONMENT == TEST_ENVIRONMENT:
    DB_URL = 'sqlite://'
    POOL_CLASS = StaticPool
else:
    DB_URL = (
        'mysql+pymysql://{user}:{password}@{host}/{db}?charset=utf8'.format(
            user=DB_CREDENTIALS.get('user'),
            password=DB_CREDENTIALS.get('password'),
            host=DB_CREDENTIALS.get('host'),
            db=DB_CREDENTIALS.get('database')))
    POOL_CLASS = NullPool
    '''logging.basicConfig(filename='myapp', level=logging.INFO)
    logging.info('DB URL:',DB_URL)'''


# Generic handlers
HEALTH_CHECK = '/hello/'
