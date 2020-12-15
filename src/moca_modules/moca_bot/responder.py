# -- Imports --------------------------------------------------------------------------

from typing import (
    List, Tuple, Optional
)
from abc import ABCMeta, abstractmethod
from random import choice
from re import search
from .dictionary import Dictionary
from .morph import is_keyword

# -------------------------------------------------------------------------- Imports --

# -- Responder --------------------------------------------------------------------------


class Responder(metaclass=ABCMeta):
    """
    AIの応答を制御する思考エンジンの基底クラス。

    メソッド:
    response(str) -- ユーザーの入力strを受け取り、思考結果を返す

    プロパティ:
    name -- Responderオブジェクトの名前
    """

    def __init__(self, name: str, dictionary: Dictionary):
        """文字列nameを受け取り、自身のnameに設定する。
        辞書dictionaryを受け取り、自身のdictionaryに保持する。"""
        self._name = name
        self._dictionary = dictionary

    @abstractmethod
    def response(self, *args) -> Optional[str]:
        """文字列を受け取り、思考した結果を返す"""
        pass

    @property
    def name(self) -> str:
        """思考エンジンの名前"""
        return self._name


# -------------------------------------------------------------------------- Responder --

# -- Random Responder --------------------------------------------------------------------------

class RandomResponder(Responder):
    """
    AIの応答を制御する思考エンジンクラス。
    登録された文字列からランダムなものを返す。
    """

    def response(self, *args) -> Optional[str]:
        """ユーザーからの入力は受け取るが、使用せずにランダムな応答を返す。"""
        count = 0
        while True:
            response = choice(self._dictionary.random)
            if response != '[el]#moca_null#':
                return response
            else:
                count += 1
                if count > 32:
                    return '[el]#moca_not_enough_data#'

# -------------------------------------------------------------------------- Random Responder --

# -- Pattern Responder --------------------------------------------------------------------------


class PatternResponder(Responder):
    """
    登録されたパターンに反応し、関連する応答を返す。
    """

    def response(self, message: str, _) -> Optional[str]:
        """ユーザーの入力に合致するパターンがあれば、関連するフレーズを返す。"""
        try:
            for pattern in self._dictionary.pattern:
                matcher = search(pattern['pattern'], message)
                if matcher:
                    chosen_response = choice(pattern['phrases'])
                    return chosen_response.replace('%match%', matcher[0])
            return None
        except Exception:
            return None

# -------------------------------------------------------------------------- Pattern Responder --

# -- Template Responder --------------------------------------------------------------------------


class TemplateResponder(Responder):
    def response(self, _, parts: List[Tuple[str, str]]) -> Optional[str]:
        """形態素解析結果partsに基づいてテンプレートを選択・生成して返す。"""
        try:
            keywords = [word for word, part in parts if is_keyword(part)]
            count = len(keywords)
            if count > 0:
                if count in self._dictionary.template:
                    template = choice(self._dictionary.template[count])
                    for keyword in keywords:
                        template = template.replace('%noun%', keyword, 1)
                    return template
            return None
        except Exception:
            return None

# -------------------------------------------------------------------------- Template Responder --

# -- Markov Responder --------------------------------------------------------------------------


class MarkovResponder(Responder):
    def response(self, _, parts: List[Tuple[str, str]]) -> Optional[str]:
        """
        形態素のリストpartsからキーワードを選択し、それに基づく文章を生成して返す。
        キーワードに該当するものがなかった場合はランダム辞書から返す。
        """
        try:
            keyword = next((w for w, p in parts if is_keyword(p)), '')
            response = self._dictionary.markov.generate(keyword)
            return response
        except Exception:
            return None

# -------------------------------------------------------------------------- Markov Responder --

# -- Special Responder --------------------------------------------------------------------------


class SpecialResponder(Responder):
    def response(self, message: str, _) -> Optional[str]:
        """固定返事があれば返答する。"""
        try:
            return self._dictionary.special.get(message, None)
        except Exception:
            return None

# -------------------------------------------------------------------------- Special Responder --

# -- Keyword Responder --------------------------------------------------------------------------


class KeywordResponder(Responder):
    def response(self, message: str, _) -> Optional[str]:
        """キーワードを含んでいれば返答する。"""
        try:
            for key in self._dictionary.keyword:
                if key in message:
                    return self._dictionary.keyword.get(key, None)
            return None
        except Exception:
            return None

# -------------------------------------------------------------------------- Keyword Responder --

# -- User Random Responder --------------------------------------------------------------------------


class UserRandomResponder(Responder):
    def response(self, *args) -> Optional[str]:
        """ユーザー定義のランダム返答をする"""
        try:
            return choice(self._dictionary.user_random)
        except Exception:
            return None


# -------------------------------------------------------------------------- User Random Responder --
