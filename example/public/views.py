# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from flask import Blueprint, render_template
from example.extensions import flaskweb3

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/node/')
def node():
    """Node info page."""
    web3ipc = flaskweb3.web3
    return render_template('public/node.html', web3ipc=web3ipc)
