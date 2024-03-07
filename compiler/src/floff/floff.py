from .floff64 import *
from .floff32 import Floff32

class FloffAuto(Floff64):
    def __new__(cls, *args, **kwargs) -> None:
        raise TypeError(f"FloffAuto can not be directly instantiated, its only use is for the fromfile static method.")

    @staticmethod
    def from_file(file_path: str, check_magic: bool = True, check_architecture: bool = True) -> object:
        new_format: FloffAuto
        arch: int

        if (not access(file_path, F_OK)):
            raise (FloFFFileNotFound(file_path))
        if (not access(file_path, R_OK)):
            raise (FloFFFilePermissionDenied(file_path))

        with open(file_path, 'rb') as fp:
            read = fp.read
            from_bytes = lambda x: int.from_bytes(x, BYTE_ORDER)

            fp.seek(6)

            arch = from_bytes(read(2))

        if (arch == ARCH_X86_64):
            new_format = Floff64.from_file(file_path, check_magic, check_architecture)
        elif (arch == ARCH_X64_32):
            new_format = Floff32.from_file(file_path, check_magic, check_architecture)
        else:
            raise (FloFFFileInvalidArchitecture(file_path))

        return (new_format)
