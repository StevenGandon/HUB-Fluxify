
INSTRUCTIONS = {
    "add": 0x01,
    "ret": 0x40,
    "call": 0x41,
    "fetch": 0x42,
    "reserve_area": 0x43,
    "free_area": 0x44
}

class CodeStackGeneration(object):
    def __init__(self) -> None:
        self.code = []
        self.labels = []
        self.symbols = []

    def add_label(self, *args):
        self.labels.extend(args)

    def add_symbol(self, *args):
        self.symbols.extend(args)

    def add_code(self, *args):
        self.code.extend(args)

class Pattern(object):
    pass

class PatternAlloc(Pattern):
    _area_stack_start = 0x0A
    _area_stack_res = []

    def __init__(self) -> None:
        super().__init__()

        self.ptr = self.__class__._area_stack_start + self._find_empty_addr()

        self.__class__._area_stack_res.append(self.ptr - self.__class__._area_stack_start)

    def _find_empty_addr(self) -> None:
        i = 0

        while i in self.__class__._area_stack_res:
            i += 1
        return (i)

    def to_code(self) -> bytes:
        return (b"\x43" + self.ptr.to_bytes(4, "big"))

class PatternFree(Pattern):
    def __init__(self, addr) -> None:
        super().__init__()

        self.addr = addr

        PatternAlloc._area_stack_res.pop(PatternAlloc._area_stack_res.index(addr - PatternAlloc._area_stack_start))

    def to_code(self) -> bytes:
        return (b"\x44" + self.addr.to_bytes(4, "big"))

class PatternFetch(Pattern):
    def __init__(self, offset: int, addr: int) -> None:
        super().__init__()

        self.offset = offset
        self.addr = addr

    def to_code(self) -> bytes:
        return (b"\x42" + self.offset.to_bytes(4, "big") + self.addr.to_bytes(4, "big"))
