
INSTRUCTIONS = {
    "add": 0x01,
    "sub": 0x02,
    "reserve_area": 0x43,
    "free_area": 0x44,
    "mv_fetch_blcks": 0x45,
    "mv_blcks_fetch": 0x46,
    "mv_contant_fetch": 0x47,
    "mv_fetch_pc": 0x49,
    "mv_pc_fetch": 0x50
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

class Pattern64(object):
    _size = 8

class Pattern32(Pattern64):
    _size = 4

class PatternAdd32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x01" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternSubstract32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x02" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternMul32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x03" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternDiv32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x04" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternMod32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x05" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternEqual32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x09" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternAnd32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x0a" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternOr32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x0b" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternBinAnd32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x06" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternBinOr32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x07" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternBinXor32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x08" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternAlloc32(Pattern32):
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
        return (b"\x43" + self.ptr.to_bytes(self.__class__._size, "big"))

class PatternFree32(Pattern32):
    def __init__(self, addr) -> None:
        super().__init__()

        self.addr = addr

        PatternAlloc32._area_stack_res.pop(PatternAlloc32._area_stack_res.index(addr - PatternAlloc32._area_stack_start))

    def to_code(self) -> bytes:
        return (b"\x44" + self.addr.to_bytes(self.__class__._size, "big"))

class PatternFetchBlcks32(Pattern32):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x45" + self.fetch_num.to_bytes(self.__class__._size, "big") + self.addr.to_bytes(self.__class__._size, "big"))

class PatternStoreFetch32(Pattern32):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x46" + self.fetch_num.to_bytes(self.__class__._size, "big") + self.addr.to_bytes(self.__class__._size, "big")

class PatternFetchConst32(Pattern32):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x47" + self.fetch_num.to_bytes(self.__class__._size, "big") + self.addr.to_bytes(self.__class__._size, "big")

class PatternPcFetch32(Pattern32):
    def __init__(self, fetch_num: int) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x49" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternFetchPc32(Pattern32):
    def __init__(self, fetch_num: int) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x50" + self.fetch_num.to_bytes(self.__class__._size, "big")
