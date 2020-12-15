# -- Imports --------------------------------------------------------------------------

from typing import (
    List, Optional, Union, Tuple
)
from random import choice
from collections import defaultdict
from copy import copy
from pathlib import Path
try:
    from cloudpickle import dump, load
except (ImportError, ModuleNotFoundError):
    from pickle import dump, load

# -------------------------------------------------------------------------- Imports --

# -- Markov --------------------------------------------------------------------------


class Markov(object):
    """マルコフ連鎖による文章の学習・生成を行う。

    クラス定数:
    END_MARK -- 文章の終わりを表す記号
    CHAIN_MAX -- 連鎖を行う最大値
    """
    END_MARK = '%END%'
    CHAIN_MAX = 30

    def __init__(self):
        """インスタンス変数の初期化。
        self._dic -- マルコフ辞書。 __dic['prefix1']['prefix2'] == ['suffixes']
        self._starts -- 文章が始まる単語の数。 __starts['prefix'] == count
        """
        self._dic = defaultdict(lambda: defaultdict(lambda: []))
        self._starts = defaultdict(lambda: 0)

    def add_sentence(self, parts: List[Tuple[str, str]]) -> None:
        """形態素解析結果partsを分解し、学習を行う。"""
        # 実装を簡単にするため、3単語以上で構成された文章のみ学習する
        if len(parts) > 3:
            # 呼び出し元の値を変更しないように`copy`する
            parts_copy = copy(parts)
            # prefix1, prefix2 には文章の先頭の2単語が入る
            prefix1, prefix2 = parts_copy.pop(0)[0], parts_copy.pop(0)[0]
            # 文章の開始点を記録する
            # 文章生成時に「どの単語から文章を作るか」の参考にするため
            self._add_start(prefix1)
            # `prefix`と`suffix`をスライドさせながら`__add_suffix`で学習させる
            # すべての単語を登録したら、最後にEND_MARKを追加する
            for suffix, _ in parts_copy:
                self._add_suffix(prefix1, prefix2, suffix)
                prefix1, prefix2 = prefix2, suffix
            self._add_suffix(prefix1, prefix2, self.END_MARK)

    def generate(self, keyword: str) -> Optional[str]:
        """keywordをprefix1とし、そこから始まる文章を生成して返す。"""
        # 辞書が空である場合はNoneを返す
        if not self._dic:
            return None
        else:
            # keywordがprefix1として登録されていない場合、__startsからランダムに選択する
            prefix1 = keyword if self._dic[keyword] else choice(list(self._starts.keys()))
            # prefix1をもとにprefix2をランダムに選択する
            prefix2 = choice(list(self._dic[prefix1].keys()))
            # 文章の始めの単語2つをwordsに設定する
            words = [prefix1, prefix2]
            # 最大CHAIN_MAX回のループを回し、単語を選択してwordsを拡張していく
            # ランダムに選択したsuffixがENDMARKであれば終了し、単語であればwordsに追加する
            # その後prefix1, prefix2をスライドさせて始めに戻る
            for _ in range(self.CHAIN_MAX):
                suffix = choice(self._dic[prefix1][prefix2])
                if suffix == self.END_MARK:
                    break
                words.append(suffix)
                prefix1, prefix2 = prefix2, suffix
            return ''.join(words)

    def load(self, filename: Union[Path, str]) -> None:
        """ファイルfilenameから辞書データを読み込む。"""
        with open(str(filename), 'rb') as file:
            self._dic, self._starts = load(file)

    def save(self, filename: Union[Path, str]) -> None:
        """ファイルfilenameへ辞書データを書き込む。"""
        with open(str(filename), 'wb') as file:
            dump((self._dic, self._starts), file)

    def _add_suffix(self, prefix1, prefix2, suffix):
        self._dic[prefix1][prefix2].append(suffix)

    def _add_start(self, prefix1):
        self._starts[prefix1] += 1

# -------------------------------------------------------------------------- Markov --
