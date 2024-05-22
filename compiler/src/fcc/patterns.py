
INSTRUCTIONS = {
    "add": 0x01,
    "sub": 0x02,
    "reserve_area": 0x43,
    "free_area": 0x44,
    "mv_fetch_blcks": 0x45,
    "mv_blcks_fetch": 0x46,
    "mv_contant_fetch": 0x47
}

class CodeStackGeneration(object):
    def __init__(self) -> None:
        self.code = []
        self.labels = []
        self.symbols = []

        self.symbols_keys = {}

    def add_label(self, arg):
        pos = len(self.labels)
        arg.position = sum(map(len, self.code))
        self.labels.append(arg)
        return (pos)

    def add_symbol(self, arg):
        if (arg.item in self.symbols_keys):
            return self.symbols_keys[arg.item]

        pos = len(self.symbols)
        self.symbols_keys[arg.item] = pos

        self.symbols.append(arg)
        return (pos)

    def add_code(self, arg):
        self.code.append(arg)

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

class PatternFetchBlcks(Pattern):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x45" + self.fetch_num.to_bytes(4, "big") + self.addr.to_bytes(4, "big"))

class PatternStoreFetch(Pattern):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x46" + self.fetch_num.to_bytes(4, "big") + self.addr.to_bytes(4, "big")

class PatternFetchConst(Pattern):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x47" + self.fetch_num.to_bytes(4, "big") + self.addr.to_bytes(4, "big")
