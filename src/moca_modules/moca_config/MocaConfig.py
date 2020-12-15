# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Optional, Any, List, Tuple, Dict, Callable
)
from pathlib import Path
try:
    from ujson import dumps
except (ImportError, ModuleNotFoundError):
    from json import dumps
from ..moca_file import MocaSynchronizedJSONDictFile
from ..moca_el_command import el_command_parser
from ..moca_core import MOCA_NULL

# -------------------------------------------------------------------------- Imports --

# -- MocaConfig --------------------------------------------------------------------------


class MocaConfig:
    """
    -- english --------------------------------------------------------------------------
    This is the config module developed by el.ideal-ideas for Moca System.
    This config module is json based.
    All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
    MocaConfig class will reload the json file in 1(default value) seconds If it was changed.
    If the json file was changed. the new config value will overwrite the old config value that in memory.
    If the config file contains "__private__": True, the config file will be a private file.
    If the config key is starts with "_" , the config will be a private config.
    If you want to access the private config, you should input the access token or the root password.
    -- 日本語 --------------------------------------------------------------------------
    これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
    この設定モジュールはJSON形式を採用しています。
    JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
    MocaConfigクラスはデフォルト設定では1秒ごとJSONファイルをリロードします(変更があった場合)。
    JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
    設定ファイルが"__private__": True,を含む場合、その設定ファイルはプライベートな設定ファイルになります。
    "_"から始まる設定内容も同様にプライベートになります。
    プライベートな設定情報にアクセスする場合、アクセストークンまたはrootパスワードが必要になります。
    -- 中文 --------------------------------------------------------------------------
    这是el.ideal-ideas为茉客系统开发的设定模块。
    这个设定模块采用了JSON格式。
    JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
    MocaConfig类会每1（初期值）秒重新读取一次JSON文件（如果有变更）。
    如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。
    如果设定文件包含"__private__": True,该设定文件则为隐私文件。
    如果设定key由"_"开始，该设定则为隐私设定。
    访问隐私设定的时候，需要输入access-token或者root密码。

    Attributes
    ----------
    self._config_file: MocaSynchronizedJSONDictFile
        a instance of MocaSynchronizedJSONDictFile, MocaConfig use this instance to storage configs.
    """

    _ROOT_PASS: Optional[str] = None

    def __init__(
            self,
            filename: Union[str, Path],
            ensure_ascii: bool = False,
            reload_interval: float = 1.0,
            access_token: Optional[str] = None,
            manual_reload: bool = False,
            **kwargs,
    ):
        """
        :param filename: the path of config file.
        :param ensure_ascii: If ensure_ascii is false,
                             then the strings written to file can contain non-ASCII characters.
        :param reload_interval: the interval to check reload.
        :param access_token: when you access to the private config, you need to provide access token.
        :param manual_reload: don't create the reload timer thread. You need run reload method manually.
        """
        self._config_file: MocaSynchronizedJSONDictFile = MocaSynchronizedJSONDictFile(
            filename, reload_interval, ensure_ascii, True, manual_reload=manual_reload
        )
        if access_token is None and self._config_file.get('__access_token__', None) is None:
            self._config_file.set('__access_token__', None)
        else:
            self._config_file.set('__access_token__', access_token)
        self._config_file.set('__private__', False)
        #############################
        if kwargs.get('mochi', False):
            self._config_file.set('__mochi__', 'もっちもっちにゃんにゃん！')
        #############################

    @classmethod
    def set_root_pass(cls, password: str) -> bool:
        """
        Root password only can set once.
        :param password: the root password.
        :return: status, [success] or [failed]
        """
        if cls._ROOT_PASS is None:
            cls._ROOT_PASS = password
            return True
        else:
            return False

    @classmethod
    def change_root_pass(cls, new_password: str, old_password: str) -> bool:
        """
        Change the root password.
        :param new_password: the new root password.
        :param old_password: the old root password.
        :return: status, [success] or [failed]
        """
        if cls._ROOT_PASS == old_password:
            cls._ROOT_PASS = new_password
            return True
        else:
            return False

    @property
    def path(self) -> Path:
        """Return the path of config file."""
        return self._config_file.filename

    @property
    def reload_interval(self) -> float:
        """Return the value of reload_interval"""
        return self._config_file.check_interval

    def is_private(self) -> bool:
        """If this config file is private, return True."""
        return bool(self._config_file.get('__private__', default=False))

    def reload_config(self) -> None:
        """Reload json config file manually."""
        self._config_file.reload_file()

    def get_config_size(self) -> int:
        """Return config cache size"""
        return len(self._config_file.dict)

    def _is_allowed(self, key: str, access_token: str = '', root_pass: str = '') -> bool:
        """Check the permission."""
        if key.startswith('_') or self._config_file.get('__private__', default=False):
            return root_pass == self._ROOT_PASS or self._config_file.check('__access_token__', access_token)
        else:
            return True

    def reload_file(self) -> None:
        self._config_file.reload_file()

    def get_config(
            self,
            key: str,
            res_type: Any = any,
            default: Any = None,
            auto_convert: bool = False,
            allow_el_command: bool = False,
            save_unknown_config: bool = False,
            access_token: str = '',
            root_pass: str = ''
    ) -> Any:
        """
        return the config value.
        :param key: the config name.
        :param res_type: the response type you want to get. if the value is <any>, don't check the response type.
        :param default: if can't found the config value, return default value.
        :param auto_convert: if the response type is incorrect, try convert the value.
        :param allow_el_command: try parser el command.
        :param save_unknown_config: save the config value with default value when can't found the config value.
        :param access_token: the access token of this config file.
        :param root_pass: the root password.
        :return: config value. if can't found the config value, return default value.
                 if the response type is incorrect and can't convert the value, return default value.
                 if can't access to the config, return default value.
        """
        # check permission
        if not self._is_allowed(key, access_token, root_pass):
            res = default
        else:
            # try get config
            config = self._config_file.get(key, MOCA_NULL)
            # check config
            if config == MOCA_NULL:
                if save_unknown_config:
                    self._config_file.set(key, default)
                res = default
            elif res_type != any and not isinstance(config, res_type):  # type error.
                if not auto_convert:
                    res = default
                elif res_type is str:
                    res = str(config)
                elif res_type is int:
                    try:
                        res = int(config)
                    except (TypeError, ValueError):
                        res = default
                elif res_type is float:
                    try:
                        res = float(config)
                    except (TypeError, ValueError):
                        res = default
                elif res_type is bool:
                    try:
                        res = bool(config)
                    except (TypeError, ValueError):
                        res = default
                elif res_type is tuple:
                    try:
                        res = tuple(config)
                    except (TypeError, ValueError):
                        res = default
                elif res_type is list:
                    try:
                        res = list(config)
                    except (TypeError, ValueError):
                        res = default
                elif res_type is dict:
                    try:
                        res = dict(config)
                    except (TypeError, ValueError):
                        res = default
                elif res_type is set:
                    try:
                        res = set(config)
                    except (TypeError, ValueError):
                        res = default
                else:
                    res = default
            else:
                res = config
        # return response
        if allow_el_command and isinstance(res, str):
            status, data = el_command_parser(res)
            if status:
                return data
            else:
                return res
        else:
            return res

    def set_config(
            self,
            key: str,
            config_value: Any,
            allow_el_command: bool = False,
            access_token: str = '',
            root_pass: str = ''
    ) -> bool:
        """
        set a config value.
        if the key already exists, overwrite it.
        :param key: the config name.
        :param config_value: the config value.
        :param allow_el_command: use el command.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: success or failed.
        """
        if self._is_allowed(key, access_token, root_pass):
            # check data
            try:
                _ = dumps(config_value)
                value = config_value
            except (TypeError, ValueError):
                value = str(config_value)
            # try parse el command.
            if allow_el_command:
                status, data = el_command_parser(value)
                if status:
                    new_value = data
                else:
                    new_value = value
            else:
                new_value = value
            # set new value.
            self._config_file.set(key, new_value)
            return True
        else:
            return False

    def get_all_config(self, access_token: str = '', root_pass: str = '') -> Optional[dict]:
        """
        Return all config.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: if can't access to the config file, return None
        """
        if self.is_private():
            if self._is_allowed('__private__', access_token, root_pass):
                return self._config_file.dict
            else:
                return None
        else:
            if self._is_allowed('__private__', access_token, root_pass):
                return self._config_file.dict
            else:
                return {key: value for key, value in self._config_file.dict.items() if not key.startswith('_')}

    def remove_config(
            self,
            key: str,
            access_token: str = '',
            root_pass: str = ''
    ) -> Optional[bool]:
        """
        Remove a config.
        :param key: the config key.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed].
        """
        if self._is_allowed(key, root_pass, access_token):
            self._config_file.remove(key)
            return True
        else:
            return None

    def set_config_private(self) -> None:
        """
        Set the config private. private config can't be accessed without access token.
        """
        self._config_file.set('__private__', True)

    def set_config_public(
            self,
            access_token: str = '',
            root_pass: str = ''
    ) -> bool:
        """Set the config public."""
        if self._is_allowed('__private__', access_token, root_pass):
            self._config_file.set('__private__', True)
            return True
        else:
            return False

    def set_access_token(
            self,
            new_token: str,
            old_token: str = '',
            root_pass: str = '',
    ) -> bool:
        """
        Set a access token for config file.
        :param new_token: the new access token of config file.
        :param old_token: the old access token of config file.
        :param root_pass: the root password.
        :return status, [success] or [failed].
        """
        if self._config_file.get('__access_token__', None) is None \
                or self._is_allowed('__access_token__', old_token, root_pass):
            self._config_file.set('__access_token__', new_token)
            return True
        else:
            return False

    def add_handler(
            self,
            name: str,
            keys: Union[List[str], str],
            handler: Callable,
            args: Tuple = (),
            kwargs: Dict = {}
    ) -> None:
        """
        Add a handler to do something when the config value was changed.
        :param name: the name of this handler. if same name is already exists, overwrite it.
        :param keys: the keys of the config.
        :param handler: the handler function.  arguments(the_updated_key, old_value, new_value, *args, **kwargs)
        :param args: arguments to the handler.
        :param kwargs: keyword arguments to the handler.
        :return: None
        """
        self._config_file.add_handler(name, keys, handler, args, kwargs)

    def remove_handler(self, name: str) -> None:
        """Remove the registered handler"""
        self._config_file.remove_handler(name)

    def get_handler(self, name: str) -> Optional[Callable]:
        """Get the registered handler"""
        return self._config_file.get_handler(name)

# -------------------------------------------------------------------------- MocaConfig --
