# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Any, Optional
)
from plyvel import DB, Error
from pathlib import Path
from ..moca_utils import moca_dumps as dumps, moca_loads as loads
from ..moca_cache import MocaSimpleCache

# -------------------------------------------------------------------------- Imports --

# -- Moca Level DB --------------------------------------------------------------------------


class MocaLevelDB:
    """
    Level DB.

    Attributes
    ----------
    self._db: LevelDB
        the level db.
    self._cache: Optional[MocaSimpleCache]
        the cache object.
    """

    def __init__(
            self,
            db: Union[Path, str],
            cache_size: int = 0
    ):
        """
        :param db: the filename of level database.
        :param cache_size: if this value is bigger than 0, MocaLevelDB will cache response use MocaSimpleCache.
        """
        self._db: DB = DB(str(db), create_if_missing=True)
        self._cache: Optional[MocaSimpleCache]
        if cache_size > 0:
            self._cache = MocaSimpleCache(pool_size=cache_size, page_size=cache_size // 5)
        else:
            self._cache = None

    @property
    def db(self) -> DB:
        return self._db

    def put(self, key: Union[bytes, str], value: Any) -> bool:
        """Add a data to core database."""
        __key = key if isinstance(key, bytes) else key.encode()
        if self._cache is not None:
            self._cache.set(str(__key), value)
        try:
            self._db.put(__key, dumps(value))
            return True
        except (Error, ValueError, TypeError):
            return False

    def get(self, key: Union[bytes, str], default: Any = None) -> Any:
        """Get a data from core database."""
        __key = key if isinstance(key, bytes) else key.encode()
        if self._cache is not None:
            cache = self._cache.get(str(__key))
            if cache is not None:
                return cache
        try:
            return loads(self._db.get(__key))
        except (Error, ValueError, TypeError):
            return default

    def delete(self, key: Union[bytes, str]) -> bool:
        """Delete data from core database."""
        __key = key if isinstance(key, bytes) else key.encode()
        if self._cache is not None:
            self._cache.remove_cache(str(__key))
        try:
            self._db.delete(__key)
            return True
        except Error:
            return False

    def close(self) -> None:
        """close the connection."""
        self._db.close()

# -------------------------------------------------------------------------- Moca Level DB --
