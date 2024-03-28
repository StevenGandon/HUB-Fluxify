from typing import Any
from ..String.show_mem import show_mem
from .buffer import Buffer

MEMORY: Buffer = Buffer(0)
OFFSET: int = 0
PTR_INSTANCES: set = set()

class Ptr(object):
    __prev_addr: int = 0
    __prev_size: int = 0

    def __init__(self, addr: int = None, offset: int = 0) -> None:
        self.addr: int = addr
        self.offset: int = offset
        self.allocated: bool = False

    def __str__(self) -> str:
        if (self.addr is None):
            return "NULL"
        return '\t'.join(str(item) for item in MEMORY[self.addr:self.addr + self.offset])

    def __repr__(self) -> str:
        return (self.__str__())

    def read(self, node: int = 0) -> Any:
        if (self.addr + node >= OFFSET):
            raise (MemoryError("Out of memory"))
        return (MEMORY[self.addr + node])

    def write(self, value: int, node: int = 0) -> None:
        if (self.addr + node >= OFFSET):
            raise (MemoryError("Out of memory"))
        MEMORY[self.addr + node] = value

    def __getitem__(self, key: int) -> int:
        return self.read(key)
    
    def __setitem__(self, key: int, value: int) -> None:
        return self.write(value, key)

    def alloc(self, blks: int, error: bool = False) -> None:
        self.addr: int = self.__prev_addr + self.__prev_size
        self.offset: int = blks

        if (OFFSET < self.addr + blks):
            if (error):
                raise (MemoryError("Out of memory"))
            else:
                self.addr = None
                return

        Ptr.__prev_addr = self.addr
        Ptr.__prev_size = blks
        self.allocated = True
        PTR_INSTANCES.add(self)

    def free(self) -> None:
        offset: int = self.offset
        addr: int = self.addr

        if (addr is None):
            return

        if (not self.allocated):
            raise (MemoryError("Not allocated"))

        for i in range(offset):
            MEMORY[addr + i] = 0x00
        for i in range(addr + offset, self.__prev_addr + self.__prev_size):
            MEMORY[i - offset] = MEMORY[i]
            MEMORY[i] = 0x00

        Ptr.__prev_addr -= offset

        for item in PTR_INSTANCES:
            if item.addr > self.addr:
                item.addr -= offset

        self.allocated: bool = False
        self.offset = 0
        PTR_INSTANCES.remove(self)

    def __add__(self, __obj: int) -> object:
        return Ptr(self.addr + __obj, self.offset - 1)

def preallocate_blocks(size: int) -> None:
    global MEMORY, OFFSET

    MEMORY = Buffer(size)
    OFFSET = size

def extend_blocks(size: int) -> None:
    global MEMORY, OFFSET

    MEMORY += Buffer(size)
    OFFSET += size

def get_raw_mem() -> tuple:
    return MEMORY.copy()

def balloc(size: int) -> Ptr:
    ptr: Ptr = Ptr()
    ptr.alloc(size)
    return (ptr)

def bfree(ptr: Ptr) -> None:
    if (ptr.allocated):
        ptr.free()

# preallocate_blocks(20)
# ptr = Ptr()
# ptr.alloc(5)
# for i in range(5):
#     (ptr + i).write(i)
# ptr2 = Ptr()
# ptr2.alloc(5)
# ptr3 = Ptr()
# ptr3.alloc(10)
# for i in range(5):
#     (ptr2 + i).write(i)
# ptr.free()
# for i in range(10):
#     (ptr3 + i).write(i * 10)
# for i in range(5):
#     (ptr2 + i).write(i * 2)
# show_mem(get_raw_mem())
# exit(0)
