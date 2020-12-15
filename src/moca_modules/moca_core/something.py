# -- Imports --------------------------------------------------------------------------

from typing import (
    List
)
from random import choice, random
from time import sleep

# -------------------------------------------------------------------------- Imports --

# -- Something --------------------------------------------------------------------------


def mochimochi(flag: int):
    """もっちもっちにゃんにゃん！"""
    data = ('もっち', 'にゃん')
    goal = 'もっちもっちにゃんにゃん'
    tmp: List[str] = []
    while True:
        print('.', end='')
        if len(tmp) < 4:
            if flag == 0:
                tmp.append(choice(data))
            elif flag == 1:
                tmp.append(data[0 if random() < 0.5 else 1])
            else:
                print('にゃん！？')
        else:
            if ''.join(tmp) == goal:
                print('にゃん！')
                break
            else:
                tmp.clear()
        sleep(0.1)


def heart(msg: str) -> None:
    print(
        '\n'.join(
            [''.join(
                [(msg[(x - y) % len(msg)]
                  if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0
                  else ' ' if msg.isascii() else '　'
                  ) for x in range(-30, 30)]
            ) for y in range(15, -15, -1)]
        )
    )

# -------------------------------------------------------------------------- Something --
