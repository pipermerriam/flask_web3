# -*- coding: utf-8 -*-
"""Create an application instance."""

from example.app import create_app
from example.settings import DevConfig


CONFIG = DevConfig

app = create_app(CONFIG)

if __name__ == '__main__':
    app.run(debug=True)
