#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Integration tests for flask_web3."""

import flask
from web3 import Web3

from flask.ext.web3.flask_web3 import FlaskWeb3
import pytest


@pytest.fixture
def app():
    return flask.Flask(__name__)

@pytest.fixture
def flaskweb3(app):
    flaskweb3 = FlaskWeb3()
    app.config['FLASKWEB3_CHAIN_NAME'] = 'local'
    app.config['FLASKWEB3_PROJECTDIR'] = '.'
    app.config['FLASKWEB3_CHAINDIR'] = 'chains'
    flaskweb3.init_app(app)
    return flaskweb3

def test_constructor(flaskweb3):
    assert flaskweb3.chain_name is not None
    assert flaskweb3.base_dir is not None


def test_init_app(app):
    flaskweb3 = FlaskWeb3()
    assert flaskweb3.chain_name is None
    flaskweb3.init_app(app)
    assert flaskweb3.chain_name is not None
    if hasattr(app, 'extensions'):
        assert 'flaskweb3' in app.extensions
        assert app.extensions['flaskweb3'] == flaskweb3


def test_coinbase_exists(app, flaskweb3):
    with app.app_context():
        web3f = flaskweb3.web3
        assert isinstance(web3f, Web3)
        assert web3f.eth.coinbase is not None


def test_geth_runs(app, flaskweb3):
    with app.app_context():
        geth = flaskweb3._geth
        assert geth.is_running
