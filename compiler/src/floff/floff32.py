from .floff64 import *

class Floff32Table(Floff64Table):
    pass

class Floff32(Floff64):
    def __init__(self) -> None:
        self.magic: bytes = DEFAULT_MAGIC
        self.version: tuple = (1, 0)
        self.arch: int = ARCH_X64_32
        self.compiler: str = "fcc"
        self.code_hash: str = ('0' * 40)
        self.start_label: int = 0x00

        self.tables: list = []

        self.raw_bytes: bytes = b''

    @staticmethod
    def from_file(file_path: str, check_magic: bool = True, check_architecture: bool = True) -> object:
        new_format: Floff32
        number_tables: int

        if (not access(file_path, F_OK)):
            raise (FloFFFileNotFound(file_path))
        if (not access(file_path, R_OK)):
            raise (FloFFFilePermissionDenied(file_path))

        with open(file_path, 'rb') as fp:
            read = fp.read
            from_bytes = lambda x: int.from_bytes(x, BYTE_ORDER)
            new_format = Floff32()

            new_format.magic = read(4)

            if (check_magic and new_format.magic != DEFAULT_MAGIC):
                raise (FloFFFileInvalidMagic(file_path))

            new_format.version = tuple(read(2))
            new_format.arch = from_bytes(read(2))
            if (check_architecture and new_format.arch != ARCH_X64_32):
                raise (FloFFFileInvalidArchitecture(file_path))

            new_format.compiler = read(read(1)[0]).decode()
            new_format.code_hash = read(40).decode()
            number_tables = from_bytes(read(4))
            new_format.start_label = from_bytes(read(4))

            new_format.tables = [None] * number_tables
            for i in range(number_tables):
                new_format.tables[i] = Floff64Table(
                    from_bytes(read(1)),
                    read(from_bytes(read(4)))
                )

        return (new_format)

    def create_table(self, table_type: int, table_content: bytes = None):
        self.tables.append(Floff32Table(table_type, table_content))

    def write(self) -> None:
        temp: bytearray = bytearray()
        extend_array = temp.extend
        integer_to_bytes = lambda x: self.integer_to_bytes(x, 4, BYTE_ORDER)
        integer_to_bytes_short = lambda x: self.integer_to_bytes(x, 2, BYTE_ORDER)

        extend_array(self.magic)
        extend_array(self.version)
        extend_array(integer_to_bytes_short(self.arch))

        if (len(self.compiler) > 0xff):
            raise (FloFFFileCompilerNameTooBig(self.code_hash))
        extend_array((len(self.compiler.encode()), ))

        extend_array(self.compiler.encode())
        extend_array(self.code_hash.encode())

        if (len(self.tables) > 0xffffffff):
            raise (FloFFFileNumberOfTablesTooBig(self.code_hash))
        extend_array(integer_to_bytes(len(self.tables)))

        if (self.start_label > 0xffffffff):
            raise (FloFFFileStartingLabelAddressTooBig(self.code_hash))
        extend_array(integer_to_bytes(self.start_label))

        for table in self.tables:
            extend_array((table.type,))

            if (len(table.bytes) > 0xffffffff):
                raise (FloFFFileTableContentTooBig(self.code_hash))
            extend_array(integer_to_bytes(len(table.bytes)))

            extend_array(table.bytes)
        self.raw_bytes = bytes(temp)
