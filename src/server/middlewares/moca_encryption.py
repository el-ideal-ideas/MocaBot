# -- Imports --------------------------------------------------------------------------

from sanic.request import Request
from spf import SanicPlugin
try:
    from orjson import loads
except (ImportError, ModuleNotFoundError):
    try:
        from ujson import loads
    except (ImportError, ModuleNotFoundError):
        from json import loads
from ... import moca_modules as mzk
from ... import core

# -------------------------------------------------------------------------- Imports --

# -- Init --------------------------------------------------------------------------

if not isinstance(core.SERVER_CONFIG['key']['pyjs_secret'], str) \
        or len(core.SERVER_CONFIG['key']['pyjs_secret']) != 16:
    mzk.print_error('pyjs_secret config must be a string of 16 characters.')
    mzk.sys_exit(1)

# -------------------------------------------------------------------------- Init --

# -- Middleware --------------------------------------------------------------------------


class EncryptionPlugin(SanicPlugin):
    def __init__(self, *args, **kwargs):
        super(EncryptionPlugin, self).__init__(*args, **kwargs)


encryption_plugin: EncryptionPlugin = EncryptionPlugin()

PYJS_SECRET = core.SERVER_CONFIG['key']['pyjs_secret'].encode()


@encryption_plugin.middleware(priority=1, attach_to='request', relative='pre')
async def moca_decryption(request: Request):
    if request.headers.get('Moca-Encryption', None) is not None:
        body = mzk.pyjs_decrypt(request.body, PYJS_SECRET)
        request.body = body

# -------------------------------------------------------------------------- Middleware --
