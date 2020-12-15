# -- Imports --------------------------------------------------------------------------

from typing import (
    Union, Iterable, Tuple, List
)
from random import randrange
from pathlib import Path
from .morph import analyze
from .responder import (
    RandomResponder, PatternResponder, TemplateResponder, MarkovResponder,
    KeywordResponder, SpecialResponder, UserRandomResponder,
)
from .dictionary import Dictionary
from ..moca_core import ENCODING

# -------------------------------------------------------------------------- Imports --

# -- MocaBot --------------------------------------------------------------------------


class MocaBot(object):
    """
    人工無脳コアクラス。

    プロパティ:
    name -- 人工無脳コアの名前
    responder_name -- 現在の応答クラスの名前
    """

    def __init__(self, name: str, data_dir: Union[Path, str]):
        self._dictionary = Dictionary(name, data_dir)

        self._responders = {
            'random': RandomResponder('random', self._dictionary),
            'pattern': PatternResponder('pattern', self._dictionary),
            'template': TemplateResponder('template', self._dictionary),
            'markov': MarkovResponder('markov', self._dictionary),
            'special': SpecialResponder('special', self._dictionary),
            'keyword': KeywordResponder('keyword', self._dictionary),
            'user_random': UserRandomResponder('user_random', self._dictionary)
        }

        self._name = name
        self._responder = self._responders['random']

    def dialogue(self, message: str, study: bool = False, config: dict = {}, responder: str = '') -> Tuple[str, str]:
        """
        ユーザーからの入力を受け取り、Responderに処理させた結果を返す。
        呼び出されるたびにランダムでResponderを切り替える。
        studyパラメータまたはauto_study設定がオンになっている場合のみ学習する。
        設定パラメータ
            user_random_level: user_randomをレスポンダーとして使用する確率
            auto_study: studyパラメータ関係なく学習する。
            word_block_list: 返事に含ませないキーワードリスト。
        """
        parts = analyze(message)
        if responder == '':
            self._responder = self._responders['special']
            response = self._responder.response(message, parts)
            if response is None:
                self._responder = self._responders['keyword']
                response = self._responder.response(message, parts)
            if (response is None) and (config.get('user_random_level', 0) > randrange(0, 100)):
                self._responder = self._responders['user_random']
                response = self._responder.response(message, parts)
            if response is None:
                limit = 3
                while True:
                    chance = randrange(0, 100)
                    if limit <= 0:
                        self._responder = self._responders['random']
                    elif 0 <= chance <= 2:
                        self._responder = self._responders['random']
                    elif 3 <= chance <= 30:
                        self._responder = self._responders['template']
                    elif 31 <= chance <= 60:
                        self._responder = self._responders['pattern']
                    else:
                        self._responder = self._responders['markov']
                    response = self._responder.response(message, parts)
                    if response:
                        break
                    else:
                        limit -= 1
        else:
            self._responder = self._responders[responder]
            response = self._responder.response(message, parts)
        if study or config.get('auto_study', False):
            self._dictionary.study(message, parts)
        for word in config.get('word_block_list', []):
            if word in response:
                return self.dialogue(message, study)
        return self._responder.name, response

    def save(self):
        """Dictionaryへの保存を行う。"""
        self._dictionary.save()

    def study(self, message: Union[str, Iterable[str]]):
        """メッセージを学習する。"""
        if isinstance(message, str):
            self._dictionary.study(message, analyze(message))
        else:
            for item in message:
                self._dictionary.study(item, analyze(item))

    def study_from_file(
            self,
            filename: Union[Path, str],
            print_log: bool = False
    ) -> List[str]:
        res = []
        with open(str(filename), mode='r', encoding=ENCODING) as file:
            count = 0
            for line in file:
                for message in line.split():
                    if len(message) < 3:
                        pass
                    elif message.startswith('#'):
                        pass
                    elif message.startswith('@'):
                        pass
                    elif message.startswith('http'):
                        pass
                    elif message.isdigit():
                        pass
                    else:
                        parts = analyze(message)
                        self._dictionary.study(message, parts)
                        count += 1
                        if print_log:
                            print(message)
                        res.append(message)
        self.save()
        if print_log:
            print(f'{count}件のテキストを学習しました。')
        return res

    @property
    def name(self) -> str:
        """人工無脳インスタンスの名前"""
        return self._name

    @property
    def responder_name(self) -> str:
        """保持しているResponderの名前"""
        return self._responder.name

# -------------------------------------------------------------------------- MocaBot --
