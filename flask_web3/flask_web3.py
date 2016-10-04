from flask import current_app
from geth import DevGethProcess
from populus.utils.filesystem import get_blockchains_dir
from web3 import IPCProvider
from web3 import Web3

__all__ = ('FlaskWeb3')
__version__ = '0.1.0'

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class FlaskWeb3(object):
    def __init__(self, app=None, chain_name=None, config_prefix='FLASKWEB3'):
        self.chain_name = chain_name
        self.config_prefix = config_prefix
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.chain_name = app.config.get(
            '{0}_CHAIN_NAME'.format(self.config_prefix), 'temp'
        )
        self.base_dir = app.config.get(
            '{0}_BASEDIR'.format(self.config_prefix), '.'
        )

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions[self.config_prefix.lower()] = self

    def start_geth(self):
        if current_app.config.get('FLASKWEB3_CHAIN_NAME') == 'local':
            geth_proc = DevGethProcess(
                chain_name=current_app.config.get('FLASKWEB3_CHAIN_NAME'),
                base_dir=get_blockchains_dir(
                    current_app.config.get('FLASKWEB3_PROJECTDIR')))
            geth_proc.start()
            return geth_proc

    @property
    def _geth(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, '_geth'):
                ctx._geth = self.start_geth()
            return ctx._geth

    @property
    def web3(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, '_geth'):
                ctx._geth = self.start_geth()
            if not hasattr(ctx, 'web3'):
                ctx.web3 = Web3(IPCProvider(ctx._geth.ipc_path))
            return ctx.web3
