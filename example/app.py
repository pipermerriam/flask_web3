# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
from gevent.pywsgi import WSGIServer

from example import public
from example.extensions import flaskweb3
from example.settings import DevConfig


class GeventFriendlyFlask(Flask):
    def run(self, host=None, port=None, debug=None, **options):
        if host is None:
            host = '127.0.0.1'
        if port is None:
            port = 5000

        if debug is not None:
            self.debug = bool(debug)

        ws = WSGIServer((host, port), DebuggedApplication(self))

        @run_with_reloader
        def _run():
            ws.serve_forever()

        _run()


def create_app(config_object=DevConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = GeventFriendlyFlask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    flaskweb3.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    return None


