from typing import Any, Iterable
from numbers import Number

def str_mem(mem: Any) -> None:
    text: str = ''
    final: str = ''

    if (isinstance(mem, str)):
        mem: Any = mem.encode()

    if (isinstance(mem, Number)):
        mem = [int(mem)]

    for i, item in enumerate(mem):
        if (i % 16 == 0):
            if (i != 0):
                final += f' |{text}|\n'
            final += (f'{hex(i).replace("0x", "").zfill(8)}  ')
            text = ''

        if (i % 16 != 0 and i % 8 == 0):
            final += (' ')

        final += (hex(item).replace("0x", "").zfill(2) + ' ')

        if (chr(item).isprintable()):
            text += chr(item)
        else:
            text += '.'

    if (i % 16 != 0):
        final += (15 - i % 16) * '   ' + (' ' if i % 16 < 8 else '')
        final += (f' |{text}|\n')
        final += (f'{hex(i + 1).replace("0x", "").zfill(8)}\n')
    else:
        final += '\n'
    return (final)


def show_mem(mem: Any) -> None:
    print(str_mem(mem))
