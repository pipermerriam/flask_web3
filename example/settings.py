# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('changeme',
                                'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    FLASKWEB3_CHAIN_NAME = 'devchain'
    FLASKWEB3_PROJECTDIR = '.'
    FLASKWEB3_CHAIN_DIR = os.path.abspath(
        os.path.join(Config.APP_DIR, 'chains'))
