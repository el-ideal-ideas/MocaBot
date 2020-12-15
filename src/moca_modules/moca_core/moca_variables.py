# -- Imports --------------------------------------------------------------------------

from typing import (
    Optional, List, Dict, Union
)
from multiprocessing import cpu_count, current_process
from socket import gethostname, gethostbyname
from uuid import uuid4
from pytz import timezone
from pytz.tzfile import DstTzInfo
from os import environ
from pathlib import Path
from sys import platform
from platform import system
from subprocess import check_output
from tzlocal import get_localzone
from ..moca_data.config import __DEBUG_MODE__

# -------------------------------------------------------------------------- Imports --

# -- Private Functions --------------------------------------------------------------------------


def __get_str_from_file(filename: Union[str, Path], encoding: str) -> str:
    """Return the contents of the file as string."""
    try:
        with open(str(filename), mode='r', encoding=encoding) as f:
            return f.read()
    except (FileNotFoundError, PermissionError):
        return '[el]#moca_error#'


# -------------------------------------------------------------------------- Private Functions --

# -- Private Info --------------------------------------------------------------------------

__redhat_release: str = __get_str_from_file('/etc/redhat-release', 'utf-8')

# -------------------------------------------------------------------------- Private Info --

# -- Variables --------------------------------------------------------------------------

ENCODING: str = 'utf-8'

VERSION: str = __get_str_from_file(Path(__file__).parent.joinpath('.version'), ENCODING)

# special value
MOCA_NULL = uuid4().hex
MOCA_FALSE = uuid4().hex
MOCA_TRUE = uuid4().hex

# OS
OS: str = system()  # Windows, Darwin, Linux
IS_WIN: bool = True if platform == 'win32' or platform == 'cygwin' else False
IS_MAC: bool = OS == 'Darwin'
IS_LINUX: bool = OS == 'Linux'
IS_UNIX_LIKE: bool = not IS_WIN
IS_RHEL: bool = __redhat_release.startswith('Red Hat Enterprise Linux release')
IS_RHEL8: bool = __redhat_release.startswith('Red Hat Enterprise Linux release 8')
IS_CENTOS: bool = __redhat_release.startswith('CentOS Linux release')
IS_CENTOS8: bool = __redhat_release.startswith('CentOS Linux release 8')
IS_RHEL_LIKE: bool = Path('/etc/redhat-release').is_file()
KERNEL: str = check_output('uname -a', shell=True).decode(ENCODING) if IS_UNIX_LIKE else 'UNKNOWN'

# new line
NEW_LINE: str = '\r\n' if IS_WIN else '\n'

# path
SELF_PATH: Path = Path(__file__).parent.parent
SYSTEM_DATA_PATH: Path = SELF_PATH.joinpath('moca_data')
SCRIPT_DIR_PATH: Path = SELF_PATH.joinpath('moca_scripts')
TMP_DIR: Path = Path('C:\\WINDOWS\\Temp').joinpath('moca_modules') \
    if IS_WIN else Path('/var/tmp').joinpath('moca_modules')
TMP_DIR.mkdir(parents=True, exist_ok=True)

# files
CHINESE_WORD_BLACKLIST: Dict[str, Path] = {
    '反动':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('反动.txt'),
    '政治':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('政治.txt'),
    '敏感词1':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('敏感词1.txt'),
    '敏感词2':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('敏感词2.txt'),
    '暴恐':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('暴恐.txt'),
    '民生':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('民生.txt'),
    '涉枪涉爆违法信息关键词':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('涉枪涉爆违法信息关键词.txt'),
    '色情':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('chinese').joinpath('色情.txt'),
}

JAPANESE_WORD_BLACKLIST: Dict[str, Path] = {
    'Offensive':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('japanese').joinpath('Offensive.txt'),
    'Sexual':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('japanese').joinpath('Sexual.txt'),
    'Sexual_with_bopo':
        SYSTEM_DATA_PATH.joinpath('word_blacklist').joinpath('japanese').joinpath('Sexual_with_bopo.txt'),
}

# system property
CPU_COUNT: int = cpu_count()
HOST_NAME: str = gethostname()
HOST: str = gethostbyname(HOST_NAME)
PROCESS_ID: Optional[int] = current_process().pid
PROCESS_NAME: str = current_process().name

# a random string.
RANDOM_KEY = uuid4().hex + uuid4().hex + uuid4().hex + uuid4().hex

# timezone
TIME_ZONE: str = environ.get('MOCA_TIME_ZONE', environ.get('TIME_ZONE', get_localzone().zone))
tz: DstTzInfo = timezone(TIME_ZONE)

# debug mode
IS_DEBUG: bool = __DEBUG_MODE__ if __DEBUG_MODE__ in (True, False) else True if str(environ.get('MOCA_DEBUG')) in (
    'y', 'Y', 'yes', 'Yes', 'YES', 'true', 'True', 'TRUE', 'T', 't', 'ok', 'Ok', 'OK', '1'
) else False

# The license of MocaSystem.
LICENSE: str = """
MIT License

Copyright 2020.9.13 <el.ideal-ideas: https://www.el-ideal-ideas.com>

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation the rights 
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Logo
EL_S: str = """Ω*
              ■          ■■■■■  
              ■         ■■   ■■ 
              ■        ■■     ■ 
              ■        ■■       
    ■■■■■     ■        ■■■      
   ■■   ■■    ■         ■■■     
  ■■     ■■   ■          ■■■■   
  ■■     ■■   ■            ■■■■ 
  ■■■■■■■■■   ■              ■■■
  ■■          ■               ■■
  ■■          ■               ■■
  ■■     ■    ■        ■■     ■■
   ■■   ■■    ■   ■■■  ■■■   ■■ 
    ■■■■■     ■   ■■■    ■■■■■
"""

# japanese Hiragana list
# あ -- ん [:46]
# ぁ -- っ [46:55]
# が -- ぽ [55:]
HIRAGANA: List[str] = ["あ", "い", "う", "え", "お",
                       "か", "き", "く", "け", "こ",
                       "さ", "し", "す", "せ", "そ",
                       "た", "ち", "つ", "て", "と",
                       "な", "に", "ぬ", "ね", "の",
                       "は", "ひ", "ふ", "へ", "ほ",
                       "ま", "み", "む", "め", "も",
                       "や", "ゆ", "よ",
                       "ら", "り", "る", "れ", "ろ",
                       "わ", "を",
                       "ん",
                       "ぁ", "ぃ", "ぅ", "ぇ", "ぉ",
                       "ゃ", "ゅ", "ょ",
                       "っ",
                       "が", "ぎ", "ぐ", "げ", "ご",
                       "ざ", "じ", "ず", "ぜ", "ぞ",
                       "だ", "ぢ", "づ", "で", "ど",
                       "ば", "び", "ぶ", "べ", "ぼ",
                       "ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]

# japanese Katakana list
# ア -- ン [:46]
# ァ -- ッ [46:55]
# ガ -- ポ [55:]
KATAKANA: List[str] = ["ア", "イ", "ウ", "エ", "オ",
                       "カ", "キ", "ク", "ケ", "コ",
                       "サ", "シ", "ス", "セ", "ソ",
                       "タ", "チ", "ツ", "テ", "ト",
                       "ナ", "ニ", "ヌ", "ネ", "ノ",
                       "ハ", "ヒ", "フ", "ヘ", "ホ",
                       "マ", "ミ", "ム", "メ", "モ",
                       "ヤ", "ユ", "ヨ",
                       "ラ", "リ", "ル", "レ", "ロ",
                       "ワ", "ヲ",
                       "ン",
                       "ァ", "ィ", "ゥ", "ェ", "ォ",
                       "ャ", "ュ", "ョ",
                       "ッ",
                       "ガ", "ギ", "グ", "ゲ", "ゴ",
                       "ザ", "ジ", "ズ", "ゼ", "ゾ",
                       "ダ", "ヂ", "ヅ", "デ", "ド",
                       "バ", "ビ", "ブ", "ベ", "ボ",
                       "パ", "ピ", "プ", "ペ", "ポ"]

# alphabet uppercase letter
ALPHABET_UPPERCASE: List[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G',
                                 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                                 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                                 'V', 'W', 'X', 'Y', 'Z']

# alphabet lowercase letter
ALPHABET_LOWERCASE: List[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                                 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                 'o', 'p', 'q', 'r', 's', 't', 'u',
                                 'v', 'w', 'x', 'y', 'z']

# number list
DIGITS: List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# chinese number list
CHINESE_DIGITS_COMPLEX: List[str] = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
CHINESE_DIGITS_SIMPLE: List[str] = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九']

# japanese number list
JAPANESE_DIGITS_HIRAGANA: List[str] = ['いち', 'に', 'さん', 'し', 'ご', 'ろく', 'しち', 'はち', 'きゅう', 'じゅう']
JAPANESE_DIGITS_KATAKANA: List[str] = ['イチ', 'ニ', 'サン', 'シ', 'ゴ', 'ロク', 'シチ', 'ハチ', 'キュウ', 'ジュウ']

# -------------------------------------------------------------------------- Variables --

# -- Clean UP --------------------------------------------------------------------------

del __redhat_release

# -------------------------------------------------------------------------- Clean Up --
