"""Application."""
# import project as project

from raven.contrib import flask

from my_project import api
from my_project import config
from my_project import handlers  # noqa


if config.SENTRY:
    api.app.config['SENTRY_DSN'] = config.SENTRY
    flask.Sentry(api.app)

app = api.app
