"""
-- EPITECH PROJECT, 2024
-- Hub project
-- File description:
-- flo file format
"""

from os import access, F_OK, R_OK, W_OK

from ..common.str_mem import str_mem

from .exceptions import (
    FloFFFileInvalidArchitecture,
    FloFFFileNotFound,
    FloFFFilePermissionDenied,
    FloFFFileInvalidMagic,
    FloFFFileCompilerNameTooBig,
    FloFFFileNumberOfTablesTooBig,
    FloFFFileStartingLabelAddressTooBig,
    FloFFFileTableContentTooBig
)

from .locals import (
    TABLE_LABEL,
    TABLE_PROGRAM,
    TABLE_CONSTANT,

    ARCH_X86_64,
    ARCH_X64_32,

    DEFAULT_MAGIC,
    BYTE_ORDER
)

#   _________________
#  |   Header 64b    |
#  |_________________|
#  |  Size  |  Name  |
#  |________|________|
#  |   04     Magic  |
#  |-----------------|
#  |   02    FVersion|
#  |-----------------|
#  |   02      Arch  |
#  |-----------------|
#  |   01    SizeText|
#  |------vvv--------|
#  |   --    Compiler|
#  |-----------------|
#  |   40     CHash  |
#  |-----------------|
#  |   08    NbTable |
#  |-----------------|
#  |   08  StartLabel|
#  |_________________|
#  |      Body       |
#  |_________________|
#  |  Size  |  Name  |
#  |________|________|
#  |   01   TableType|
#  |-----------------|
#  |   08   TableSize|
#  |------vvv--------|
#  |   --   TableByte|
#  |-----------------|
#  |       ...       |
#  |_________________|


class Floff64Table(object):
    def __init__(self, table_type: int, table_bytes: int) -> None:
        self.type: int = table_type
        self.bytes: bytes = table_bytes

    def __str__(self) -> str:
        return f"{Floff64Table.type_to_string(self.type)}:\n{str_mem(self.bytes)}"

    def __repr__(self) -> str:
        return (self.__str__())

    @staticmethod
    def type_to_string(table_type: int) -> str:
        if (table_type == TABLE_LABEL):
            return ("labels")
        if (table_type == TABLE_PROGRAM):
            return ("program")
        if (table_type == TABLE_CONSTANT):
            return ("constant")
        return ("unknown")

class Floff64(object):
    def __init__(self) -> None:
        self.magic: bytes = DEFAULT_MAGIC
        self.version: tuple = (1, 0)
        self.arch: int = ARCH_X86_64
        self.compiler: str = "fcc"
        self.code_hash: str = ('0' * 40)
        self.start_label: int = 0x00

        self.tables: list = []

        self.raw_bytes: bytes = b''

    def __str__(self) -> str:
        return f"{self.code_hash}:\n" + \
            f"  magic: {''.join(map(lambda x: hex(x).split('x')[1].zfill(2), self.magic))}\n" + \
            f"  version: {'.'.join(map(str, self.version))}\n" + \
            f"  architecture: {Floff64.arch_to_string(self.arch)}\n" + \
            f"  compiler: {self.compiler}\n" + \
            f"  start label: 0x{self.start_label}\n" + \
            '\n  '.join(map(str, self.tables))

    def __repr__(self) -> str:
        return (self.__str__())

    @staticmethod
    def from_file(file_path: str, check_magic: bool = True, check_architecture: bool = True) -> object:
        new_format: Floff64
        number_tables: int

        if (not access(file_path, F_OK)):
            raise (FloFFFileNotFound(file_path))
        if (not access(file_path, R_OK)):
            raise (FloFFFilePermissionDenied(file_path))

        with open(file_path, 'rb') as fp:
            read = fp.read
            from_bytes = lambda x: int.from_bytes(x, BYTE_ORDER)
            new_format = Floff64()

            new_format.magic = read(4)
            if (new_format.magic != DEFAULT_MAGIC):
                raise (FloFFFileInvalidMagic(file_path))

            new_format.version = tuple(read(2))
            new_format.arch = from_bytes(read(1))
            if (new_format.arch != ARCH_X86_64):
                raise (FloFFFileInvalidArchitecture(file_path))

            new_format.compiler = read(read(1)[0]).decode()
            new_format.code_hash = read(40).decode()
            number_tables = from_bytes(read(8))
            new_format.start_label = from_bytes(read(8))

            new_format.tables = [None] * number_tables
            for i in range(number_tables):
                new_format.tables[i] = Floff64Table(
                    from_bytes(read(1)),
                    read(from_bytes(read(8)))
                )

        return (new_format)

    @staticmethod
    def arch_to_string(arch: int) -> str:
        if (arch == ARCH_X86_64):
            return ("x86_64")
        if (arch == ARCH_X64_32):
            return ("x64_32")
        return ("unknown")

    @staticmethod
    def integer_to_bytes(interger: int, size: int, byteorder: str = "big") -> bytes:
        value: str = (bytes.fromhex(hex(interger).split('x')[1].zfill(size * 2)))
        return (value if byteorder == "big" else value[::-1])

    def create_table(self, table_type: int, table_content: bytes = None):
        self.tables.append(Floff64Table(table_type, table_content))

    def add_table(self, table: Floff64Table):
        self.tables.append(table)

    def write(self) -> None:
        temp: bytearray = bytearray()
        extend_array = temp.extend
        integer_to_bytes = lambda x: self.integer_to_bytes(x, 8, BYTE_ORDER)

        extend_array(self.magic)
        extend_array(self.version)
        extend_array((self.arch,))

        if (len(self.compiler) > 0xff):
            raise (FloFFFileCompilerNameTooBig(self.code_hash))
        extend_array((len(self.compiler.encode()), ))

        extend_array(self.compiler.encode())
        extend_array(self.code_hash.encode())

        if (len(self.tables) > 0xffffffffffffffff):
            raise (FloFFFileNumberOfTablesTooBig(self.code_hash))
        extend_array(integer_to_bytes(len(self.tables)))

        if (self.start_label > 0xffffffffffffffff):
            raise (FloFFFileStartingLabelAddressTooBig(self.code_hash))
        extend_array(integer_to_bytes(self.start_label))

        for table in self.tables:
            extend_array((table.type,))

            if (len(table.bytes) > 0xffffffffffffffff):
                raise (FloFFFileTableContentTooBig(self.code_hash))
            extend_array(integer_to_bytes(len(table.bytes)))

            extend_array(table.bytes)
        self.raw_bytes = bytes(temp)

    def flush(self, file_path: str) -> None:
        if (not access('/'.join(file_path.split('/')[:-1]), W_OK)):
            raise (FloFFFilePermissionDenied(file_path))

        with open(file_path, 'wb') as fp:
            fp.write(self.raw_bytes)
            fp.flush()

        self.raw_bytes = b''
