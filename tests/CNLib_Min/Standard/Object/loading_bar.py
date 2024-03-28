from typing import Iterable, Any, TextIO, Callable
from sys import stdout
from time import sleep

STYLE_DEFAULT: Callable = lambda index, max_index, loading: "Loading: [%d/%d] - %s\r" % (index, max_index, loading)
STYLE_TEST: Callable = lambda index, max_index, loading: f"{loading} - {index}/{max_index} [{'.' * index}{' ' * (max_index - index)}]\r"

class LoadingBar(object):
    def __init__(self, iterable: Iterable = None, fp: TextIO = stdout, style: Callable = STYLE_DEFAULT) -> None:
        if (iterable is None):
            iterable = list()

        self.items: list = list(iterable)
        self.max_index: int = len(self.items)
        self.index: int = 0
        self.fp: TextIO = fp
        self.style: str = style
        self.correct: str = 0

    def add(self, __obj: Any) -> None:
        self.max_index += 1
        self.items.append(__obj)

    def show(self) -> None:
        if (not self.fp or not self.fp.writable or self.fp.closed):
            return
        style: str = self.style(self.index, self.max_index, self.items[self.index - 1])

        self.fp.write(' ' * self.correct + '\r' + style)
        self.fp.flush()

        self.correct = len(style)

    def __iter__(self) -> object:
        self.index: int = 0

        return self

    def __next__(self) -> Any:
        if self.index >= self.max_index:
            raise StopIteration

        value: Any = self.items[self.index]
        self.index += 1
        self.show()

        return (self.index, value)

#L = LoadingBar([5, 0, 1, 4849, 489, 8, 7, 9, 6, 7, 4, 8, 8, 6], style=STYLE_TEST)
#L.add(4)
#stdout.write(code_invisible_cursor())
#for i, item in L:
#    sleep(0.5)
#stdout.write(code_visible_cursor())
#exit(0)