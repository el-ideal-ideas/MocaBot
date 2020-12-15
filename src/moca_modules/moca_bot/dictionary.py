# -- Imports --------------------------------------------------------------------------

from typing import (
    List, Tuple, Union
)
from collections import defaultdict
from pathlib import Path
from functools import partial
from .markov import Markov
from .morph import is_keyword
from ..moca_core import ENCODING
try:
    from ujson import dump, load
except (ImportError, ModuleNotFoundError):
    from json import dump as __dump, load

    # This is done in order to ensure that the JSON response is
    # kept consistent across both ujson and inbuilt json usage.
    dump = partial(__dump, separators=(",", ":"))

# -------------------------------------------------------------------------- Imports --

# -- Dictionary --------------------------------------------------------------------------


class Dictionary(object):
    """思考エンジンの辞書クラス。

    プロパティ:
    _data_dir -- データ保存用ディレクトリ
    _name -- 辞書の名前
    _random -- ランダム辞書
    _pattern -- パターン辞書
    _template -- テンプレート辞書
    _markov -- マルコフ辞書
    _special -- 固定返事
    _keyword -- キーワード辞書
    _user_random -- ユーザー定義ランダム辞書
    """

    def __init__(self, name: str, data_dir: Union[str, Path]):
        """ファイルから辞書の読み込みを行う。"""
        self._name = name
        self._data_dir = Path(data_dir)
        self._random = None
        self._pattern = None
        self._template = None
        self._markov = None
        self._special = None
        self._keyword = None
        self._user_random = None
        self.reload()
        
    def reload(self) -> None:
        self._random = self._load_random()
        self._pattern = self._load_pattern()
        self._template = self._load_template()
        self._markov = self._load_markov()
        self._special = self._load_special()
        self._keyword = self._load_keyword()
        self._user_random = self._load_user_random()

    def study(self, message: str, parts: List[Tuple[str, str]]) -> None:
        """ランダム辞書、パターン辞書、テンプレート辞書、マルコフ辞書の学習データをメモリに保存する。"""
        self.study_random(message)
        self.study_pattern(message, parts)
        self.study_template(parts)
        self.study_markov(parts)

    def study_markov(self, parts: List[Tuple[str, str]]) -> None:
        """形態素のリストpartsを受け取り、マルコフ辞書に学習させる。"""
        self._markov.add_sentence(parts)

    def study_template(self, parts: List[Tuple[str, str]]) -> None:
        """
        形態素のリストpartsを受け取り、
        名詞のみ'%noun%'に変更した文字列templateをself._templateに追加する。
        名詞が存在しなかった場合、または同じtemplateが存在する場合は何もしない。
        """
        template = ''
        count = 0
        for word, part in parts:
            if is_keyword(part):
                word = '%noun%'
                count += 1
            template += word

        if count > 0 and template not in self._template[count]:
            self._template[count].append(template)

    def study_random(self, message: str) -> None:
        """
        ユーザーの発言をランダム辞書に保存する。
        すでに同じ発言があった場合は何もしない。
        """
        if message not in self._random:
            self._random.append(message)

    def study_pattern(self, message: str, parts: List[Tuple[str, str]]) -> None:
        """ユーザーの発言を形態素partsに基づいてパターン辞書に保存する。"""
        for word, part in parts:
            if is_keyword(part):  # 品詞が名詞でなければ学習しない
                # 単語の重複チェック
                # 同じ単語で登録されていれば、パターンを追加する
                # 無ければ新しいパターンを作成する
                duplicated = self._find_duplicated_pattern(word)
                if duplicated and message not in duplicated['phrases']:
                    duplicated['phrases'].append(message)
                else:
                    self._pattern.append({'pattern': word, 'phrases': [message]})

    def add_special(self, keyword: str, text: str) -> None:
        """固定返事を追加する。"""
        self._special[keyword] = text

    def add_keyword(self, keyword: str, text: str) -> None:
        """キーワード返事を追加する。"""
        self._keyword[keyword] = text
        
    def add_user_random(self, text: str) -> None:
        """ユーザー定義ランダム返事を追加する。"""
        self._user_random.append(text)

    def save(self) -> None:
        """メモリ上の辞書をファイルに保存する。"""
        self._save_random()
        self._save_pattern()
        self._save_template()
        self._markov.save(self._data_dir.joinpath('markov.data'))
        self._save_special()
        self._save_keyword()
        self._save_user_random()

    def _save_template(self):
        """テンプレート辞書を保存する。"""
        filename = str(self._data_dir.joinpath('template.txt'))
        with open(filename, mode='w', encoding=ENCODING) as file:
            for count, templates in self._template.items():
                for template in templates:
                    file.write('{}\t{}\n'.format(count, template))

    def _save_pattern(self):
        """パターン辞書を保存する。"""
        filename = str(self._data_dir.joinpath('pattern.txt'))
        with open(filename, mode='w', encoding=ENCODING) as file:
            for pattern in self._pattern:
                file.write(Dictionary.pattern2line(pattern))
                file.write('\n')

    def _save_random(self):
        """ランダム辞書を保存する。"""
        filename = str(self._data_dir.joinpath('random.txt'))
        with open(filename, mode='w', encoding=ENCODING) as file:
            file.write('\n'.join(self.random))

    def _save_special(self):
        """固定返事を保存する。"""
        filename = str(self._data_dir.joinpath('special.json'))
        with open(filename, mode='w', encoding=ENCODING) as file:
            dump(self._special,
                 file,
                 ensure_ascii=False,
                 indent=4,
                 sort_keys=False)

    def _save_keyword(self):
        """キーワードを保存する。"""
        filename = str(self._data_dir.joinpath('keyword.json'))
        with open(filename, mode='w', encoding=ENCODING) as file:
            dump(self._keyword,
                 file,
                 ensure_ascii=False,
                 indent=4,
                 sort_keys=False)

    def _save_user_random(self):
        """ユーザー定義ランダム辞書を保存する。"""
        filename = str(self._data_dir.joinpath('user_random.json'))
        with open(filename, mode='w', encoding=ENCODING) as file:
            dump(self._user_random,
                 file,
                 ensure_ascii=False,
                 indent=4,
                 sort_keys=False)

    def _find_duplicated_pattern(self, word: str):
        """パターン辞書に名詞wordがあればパターンハッシュを、無ければNoneを返す。"""
        return next((pattern for pattern in self._pattern if pattern['pattern'] == word), None)

    def _load_random(self):
        """
        ランダム辞書を読み込み、リストを返す。
        空である場合、[el]#moca_null#を追加する。
        """
        filename = str(self._data_dir.joinpath('random.txt'))
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                lines = file.read().splitlines()
                return [message for message in lines if message != ''] if len(lines) > 0 else ['[el]#moca_null#']
        except FileNotFoundError:
            return ['[el]#moca_null#']

    def _load_pattern(self):
        """パターン辞書を読み込み、パターンハッシュのリストを返す。"""
        filename = str(self._data_dir.joinpath('pattern.txt'))
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                return [Dictionary.line2pattern(line) for line in file.read().splitlines() if line != '']
        except FileNotFoundError:
            return []

    def _load_template(self):
        """テンプレート辞書を読み込み、ハッシュを返す。"""
        filename = str(self._data_dir.joinpath('template.txt'))
        templates = defaultdict(lambda: [])
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                for line in file.read().splitlines():
                    count, template = line.split('\t')
                    if count and template:
                        count = int(count)
                        templates[count].append(template)
                return templates
        except FileNotFoundError:
            return templates

    def _load_special(self):
        """固定返事を読み込んで辞書を返す。"""
        filename = str(self._data_dir.joinpath('special.json'))
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                return load(file)
        except FileNotFoundError:
            return {}

    def _load_keyword(self):
        """キーワードを読み込んで辞書を返す。"""
        filename = str(self._data_dir.joinpath('keyword.json'))
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                return load(file)
        except FileNotFoundError:
            return {}

    def _load_user_random(self):
        """ユーザー定義ランダム辞書を読み込んでリストを返す。"""
        filename = str(self._data_dir.joinpath('user_random.json'))
        try:
            with open(filename, mode='r', encoding=ENCODING) as file:
                return load(file)
        except FileNotFoundError:
            return []

    def _load_markov(self):
        """Markovオブジェクトを生成し、filenameから読み込みを行う。"""
        markov = Markov()
        filename = self._data_dir.joinpath('markov.data')
        if filename.is_file():
            markov.load(filename)
        return markov

    @staticmethod
    def pattern2line(pattern: dict):
        """
        パターンのハッシュを文字列に変換する。
        >>> pattern = {'pattern': 'Pattern', 'phrases': ['phrases', 'list']}
        >>> Dictionary.pattern2line(pattern)
        'Pattern\\tphrases|list'
        """
        return '{}\t{}'.format(pattern['pattern'], '|'.join(pattern['phrases']))

    @staticmethod
    def line2pattern(line: str):
        """
        文字列lineを\tで分割し、{'pattern': [0], 'phrases': [1]}の形式で返す。
        [1]はさらに`|`で分割し、文字列のリストとする。
        >>> line = 'Pattern\\tphrases|list'
        >>> Dictionary.line2pattern(line)
        {'pattern': 'Pattern', 'phrases': ['phrases', 'list']}
        """
        pattern, phrases = line.split('\t')
        if pattern and phrases:
            return {'pattern': pattern, 'phrases': phrases.split('|')}

    @property
    def random(self):
        """ランダム辞書"""
        return self._random

    @property
    def pattern(self):
        """パターン辞書"""
        return self._pattern

    @property
    def template(self):
        """テンプレート辞書"""
        return self._template

    @property
    def markov(self):
        """マルコフ辞書"""
        return self._markov

    @property
    def special(self):
        """固定返事"""
        return self._special

    @property
    def keyword(self):
        """キーワード"""
        return self._keyword

    @property
    def user_random(self):
        """ユーザー定義ランダム"""
        return self._user_random

# -------------------------------------------------------------------------- Dictionary --
