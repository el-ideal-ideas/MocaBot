# -- Imports --------------------------------------------------------------------------

from typing import (
    Set, Union, List, Dict
)
from collections import defaultdict
from pathlib import Path
from re import compile
from ..moca_core import ENCODING
from ..moca_utils import to_hankaku

# -------------------------------------------------------------------------- Imports --

# -- MocaSimpleWordFilter --------------------------------------------------------------------------


class MocaSimpleWordFilter:
    """
    A very simple filter implementation.

    Attributes
    ----------
    self._keywords: Set[str]
        A set of keywords that should be filtered.
    """

    def __init__(self):
        self._keywords: Set[str] = set()

    @property
    def keywords(self) -> Set[str]:
        return self._keywords

    def add_word(self, word: str) -> None:
        """Adds a keyword to the blacklist."""
        data = to_hankaku(word.lower().strip())
        if data != '':
            self._keywords.add(data)

    def load_keywords_from_file(self, filename: Union[str, Path], encoding: str = ENCODING) -> None:
        """Load keywords from a file."""
        with open(str(filename), mode='r', encoding=encoding) as file:
            for keyword in file:
                self.add_word(keyword)

    def filter(self, message: str, replace: str = '*') -> str:
        """Replace keywords in blacklist to `replace`"""
        data = to_hankaku(message.lower().strip())
        for keyword in self._keywords:
            if keyword in data:
                data = data.replace(keyword, replace * len(keyword))
        return data


# -------------------------------------------------------------------------- MocaSimpleWordFilter --

# -- MocaBSFilter --------------------------------------------------------------------------


class MocaBSFilter:

    """
    Filter Messages from keywords, Use Back Sorted Mapping to reduce replacement times.

    Attributes
    ----------
    self._keywords: List[str]
        The list of keywords that should be filtered.
    self._keywords_set: Set[str]
        A set of keywords that should be filtered.
    self._back_sorted_dict
        Back Sorted Mapping.
    self._pat_en
        compile(r'^[0-9a-zA-Z]+$')
    """

    def __init__(self):
        self._keywords: List[str] = []
        self._keywords_set: Set[str] = set()
        self._back_sorted_dict = defaultdict(set)
        self._pat_en = compile(r'^[0-9a-zA-Z]+$')  # phrase english or not

    @property
    def keywords(self) -> Set[str]:
        return self._keywords_set

    def add_word(self, keyword: str) -> None:
        """Adds a keyword to the blacklist."""
        data = to_hankaku(keyword.lower().strip())
        if data != '' and data not in self._keywords_set:
            self._keywords.append(data)
            self._keywords_set.add(data)
            index = len(self._keywords) - 1
            for word in data.split():
                if self._pat_en.search(word):
                    self._back_sorted_dict[word].add(index)
                else:
                    for char in word:
                        self._back_sorted_dict[char].add(index)

    def load_keywords_from_file(self, filename: Union[str, Path], encoding: str = ENCODING) -> None:
        """Load keywords from a file."""
        with open(str(filename), mode='r', encoding=encoding) as file:
            for keyword in file:
                self.add_word(keyword)

    def filter(self, message: str, replace: str = '*') -> str:
        """Replace keywords in blacklist to `replace`"""
        data = to_hankaku(message.lower().strip())
        for word in data.split():
            if self._pat_en.search(word):
                for index in self._back_sorted_dict[word]:
                    data = data.replace(self._keywords[index], replace)
            else:
                for char in word:
                    for index in self._back_sorted_dict[char]:
                        data = data.replace(self._keywords[index], replace)
        return data

# -------------------------------------------------------------------------- MocaBSFilter --

# -- MocaDFAFilter --------------------------------------------------------------------------


class MocaDFAFilter:
    """
    Filter Messages from keywords, Use DFA to keep algorithm perform constantly.

    Attributes
    ----------
    self._keyword_chains
        the keyword chains.
    """

    def __init__(self):
        self._keyword_chains = {}
        self._delimit = '\x00'

    @property
    def keyword_chains(self) -> Dict:
        return self._keyword_chains

    def add_word(self, keyword: str) -> None:
        """Add a word."""
        chars = to_hankaku(keyword.lower().strip())
        if chars != '':
            level = self.keyword_chains
            for i in range(len(chars)):
                if chars[i] in level:
                    level = level[chars[i]]
                else:
                    if not isinstance(level, dict):
                        break
                    for j in range(i, len(chars)):
                        level[chars[j]] = {}
                        last_level, last_char = level, chars[j]
                        level = level[chars[j]]
                    last_level[last_char] = {self._delimit: 0}
                    break
            if i == len(chars) - 1:
                level[self._delimit] = 0

    def load_keywords_from_file(self, filename: Union[str, Path], encoding: str = ENCODING) -> None:
        with open(str(filename), mode='r', encoding=encoding) as file:
            for keyword in file:
                self.add_word(keyword)

    def filter(self, message: str, replace: str = '*') -> str:
        """Replace keywords in blacklist to `replace`"""
        data = to_hankaku(message.lower().strip())
        ret = []
        start = 0
        while start < len(data):
            level = self.keyword_chains
            step_ins = 0
            for char in data[start:]:
                if char in level:
                    step_ins += 1
                    if self._delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(replace * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(data[start])
                    break
            else:
                ret.append(data[start])
            start += 1
        return ''.join(ret)

# -------------------------------------------------------------------------- MocaDFAFilter --
