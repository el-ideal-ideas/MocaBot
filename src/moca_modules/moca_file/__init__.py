# -- Imports --------------------------------------------------------------------------

from .MocaDirectoryCache import MocaDirectoryCache
from .MocaFileAppendController import MocaFileAppendController
from .MocaFileCacheController import MocaFileCacheController
from .MocaSynchronizedBinaryFile import MocaSynchronizedBinaryFile
from .MocaSynchronizedJSONDictFile import MocaSynchronizedJSONDictFile
from .MocaSynchronizedJSONFile import MocaSynchronizedJSONFile
from .MocaSynchronizedJSONListFile import MocaSynchronizedJSONListFile
from .MocaSynchronizedJSONFile import MocaSynchronizedTextFile
from .MocaWriteFileController import MocaWriteFileController, MocaWriteEncryptedFileController
from .utils import (
    get_str_from_file, get_str_from_file_with_cache, aio_get_str_from_file, aio_get_str_from_file_with_cache,
    get_mime_type, get_mime_type_with_cache, get_timestamp, get_bytes_from_file, get_bytes_from_file_with_cache,
    aio_get_bytes_from_file, aio_get_bytes_from_file_with_cache, write_str_to_file, aio_write_str_to_file,
    write_bytes_to_file, aio_write_bytes_to_file, append_str_to_file, aio_append_str_to_file, load_json_from_file,
    load_json_from_file_with_cache, aio_load_json_from_file, aio_load_json_from_file_with_cache,
    dump_json_to_file, aio_dump_json_to_file, get_last_line, get_str_from_end_of_file
)

# -------------------------------------------------------------------------- Imports --


"""
This module provides some classes for manage files.

Requirements
------------
ujson           
    UltraJSON is an ultra fast JSON encoder and decoder written in pure C with bindings for Python 3.5+.
aiofiles        
    aiofiles is an Apache2 licensed library, written in Python, for handling local disk files in asyncio applications.
async_lru
    Simple lru cache for asyncio
python-magic
    python-magic is a Python interface to the libmagic file type identification library.
    libmagic identifies file types by checking their headers according to a predefined list of file types.
    This module need libmagic.
    CentOS
        dnf install file-devel
    Debian/Ubuntu
        sudo apt-get install libmagic1
    Windows
        pip install python-magic-bin
    macOS
        brew install libmagic 
"""
