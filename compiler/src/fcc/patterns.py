from .label_table import *
from .constant_table import *

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
    def __init__(self, builder_arch = "64") -> None:
        self.code = []
        self.labels = []
        self.symbols = []

        self.symbols_keys = {}

        self.builder_arch = builder_arch

    def builder(self, name, __globals = None):
        if (not __globals):
            __globals = globals()
        return __globals.get(name + self.builder_arch, Pattern)

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
    def to_code(self, *args, **kwargs):
        return ('\x00')

class Pattern64(Pattern):
    _size = 8

class PatternAdd64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x01" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternSubstract64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x02" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternMul64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x03" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternDiv64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x04" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternMod64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x05" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternEqual64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x09" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternAnd64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x0a" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternOr64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x0b" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternBinAnd64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x06" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternBinOr64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x07" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternBinXor64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x08" + self.fetch_num.to_bytes(self.__class__._size, "big"))

class PatternAlloc64(Pattern64):
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

class PatternFree64(Pattern64):
    def __init__(self, addr) -> None:
        super().__init__()

        self.addr = addr

        # if (addr - PatternAlloc64._area_stack_start in PatternAlloc64._area_stack_res):
        #     PatternAlloc64._area_stack_res.pop(PatternAlloc64._area_stack_res.index(addr - PatternAlloc64._area_stack_start))

    def to_code(self) -> bytes:
        return (b"\x44" + self.addr.to_bytes(self.__class__._size, "big"))

class PatternWeakFree64(Pattern64):
    def __init__(self, addr) -> None:
        super().__init__()

        self.addr = addr

    def to_code(self) -> bytes:
        return (b"\x44" + self.addr.to_bytes(self.__class__._size, "big"))

class PatternFetchBlcks64(Pattern64):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return (b"\x45" + self.fetch_num.to_bytes(self.__class__._size, "big") + self.addr.to_bytes(self.__class__._size, "big"))

class PatternStoreFetch64(Pattern64):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x46" + self.fetch_num.to_bytes(self.__class__._size, "big") + self.addr.to_bytes(self.__class__._size, "big")

class PatternFetchConst64(Pattern64):
    def __init__(self, addr: int, fetch_num: int) -> None:
        super().__init__()

        self.addr = addr
        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x47" + self.fetch_num.to_bytes(self.__class__._size, "big") + self.addr.to_bytes(self.__class__._size, "big")

class PatternPcFetch64(Pattern64):
    def __init__(self, fetch_num: int) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x49" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternFetchPc64(Pattern64):
    def __init__(self, fetch_num: int) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self) -> bytes:
        return b"\x50" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternGetLabel64(Pattern64):
    def __init__(self, fetch_num: int) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return  b"\x51" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternReadBlckInFetch064(Pattern64):
    def __init__(self, fetch_num=0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x54" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternSwapFetch64(Pattern64):
    def __init__(self) -> None:
        super().__init__()

    def to_code(self):
        return b"\x52"

class PatternDeclareVar64(Pattern64):
    def __init__(self) -> None:
        super().__init__()

    def to_code(self):
        return b"\x55"

class PatternAssignVar64(Pattern64):
    def __init__(self) -> None:
        super().__init__()

    def to_code(self):
        return b"\x56"

class PatternResetFetch64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x57"  + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternFetchVariable64(Pattern64):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x59"  + self.fetch_num.to_bytes(self.__class__._size, "big")


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

        # if (addr - PatternAlloc32._area_stack_start in PatternAlloc32._area_stack_res):
        #     PatternAlloc32._area_stack_res.pop(PatternAlloc32._area_stack_res.index(addr - PatternAlloc32._area_stack_start))

    def to_code(self) -> bytes:
        return (b"\x44" + self.addr.to_bytes(self.__class__._size, "big"))

class PatternWeakFree32(Pattern32):
    def __init__(self, addr) -> None:
        super().__init__()

        self.addr = addr

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

class PatternGetLabel32(Pattern32):
    def __init__(self, fetch_num: int) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return  b"\x51" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternReadBlckInFetch032(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x54" + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternSwapFetch32(Pattern32):
    def __init__(self) -> None:
        super().__init__()

    def to_code(self):
        return b"\x52"

class PatternDeclareVar32(Pattern32):
    def __init__(self) -> None:
        super().__init__()

    def to_code(self):
        return b"\x55"

class PatternAssignVar32(Pattern32):
    def __init__(self) -> None:
        super().__init__()

    def to_code(self):
        return b"\x56"

class PatternResetFetch32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x57"  + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternResetFetch32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x57"  + self.fetch_num.to_bytes(self.__class__._size, "big")

class PatternFetchVariable32(Pattern32):
    def __init__(self, fetch_num = 0) -> None:
        super().__init__()

        self.fetch_num = fetch_num

    def to_code(self):
        return b"\x59"  + self.fetch_num.to_bytes(self.__class__._size, "big")
