from os.path import isfile
from src.floff import *

class Linker(object):
    def __init__(self, files: list, arch: int = ARCH_X86_64) -> None:
        self.arch = arch
        self.files = files if all(isfile(file) for file in files) else []

    def link(self) -> FloffAuto:
        result = Floff64() if (self.arch == ARCH_X86_64) else Floff32()

        for i, file in enumerate(self.files):
            floff_file: Floff64 = FloffAuto(file)

            if (i == 0):
                for item in floff_file.tables:
                    result.add_table(item)

        result.code_hash = "0000000000000000000000000000000000000000"
