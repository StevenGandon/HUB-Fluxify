from os.path import isfile
from src.floff import *

class Linker(object):
    def __init__(self, files: list, arch: int = ARCH_X86_64, name="a.flo") -> None:
        self.arch = arch
        self.files = files if all(isfile(file) for file in files) else []

        self.code = Floff64() if (self.arch == ARCH_X86_64) else Floff32()

        self.name = name

        self.size_t = 4 if self.arch == ARCH_X64_32 else 8

    def link(self) -> FloffAuto:
        code = self.code

        code_size = 0
        constant_size = 0
        alloc_size = 0x0A
        constants = {}

        for i, file in enumerate(self.files):
            redirect_const_table = {}
            temp_const_size = 0
            floff_file: Floff64 = FloffAuto.from_file(file)

            if (i == 0):
                for item in floff_file.tables:
                    code.add_table(item)
                    if (item.type == TABLE_PROGRAM):
                        index = 0
                        while ((index := item.bytes.find(b"\x43", index + 1)) != -1):
                            alloc_size += 1

                        print(alloc_size)

                        code_size += len(item.bytes)
                    if (item.type == TABLE_CONSTANT):
                        temp = 0
                        while temp < len(item.bytes):
                            temp += 1

                            size = int.from_bytes(item.bytes[temp:temp + self.size_t], "big")

                            temp += self.size_t

                            value = item.bytes[temp:temp + size]

                            temp += size

                            constants[value] = constant_size

                            constant_size += 1

                continue

            for item in floff_file.tables:
                if (item.type == TABLE_PROGRAM):
                    new_bytes = bytearray()

                    new_bytes.extend(item.bytes)

                    index = 0
                    while ((index := new_bytes.find(b"\x43", index + 1)) != -1):
                        new_bytes = new_bytes[:index + 1] + alloc_size.to_bytes(self.size_t, "big") + new_bytes[index + 1 + self.size_t:]
                        alloc_size += 1

                    print(alloc_size)

                    code_size += len(item.bytes)

                    item.bytes = bytes(new_bytes)

                if (item.type == TABLE_CONSTANT):
                    temp = 0
                    new_bytes = bytearray()

                    while temp < len(item.bytes):
                        vl_type = item.bytes[temp]

                        temp += 1

                        size = int.from_bytes(item.bytes[temp:temp + self.size_t], "big")

                        temp += self.size_t

                        value = item.bytes[temp:temp + size]

                        temp += size

                        print(value, constants)

                        if (value in constants):
                            redirect_const_table[temp_const_size] = constants[value]
                            temp_const_size += 1
                            continue

                        temp_const_size += 1

                        redirect_const_table[temp_const_size] = constant_size

                        constants[value] = constant_size

                        constant_size += 1

                        new_bytes.extend(vl_type.to_bytes(1, "big"))
                        new_bytes.extend(size.to_bytes(self.size_t, "big"))
                        new_bytes.extend(value)

                    item.bytes = bytes(new_bytes)

                if (item.type == TABLE_LABEL):
                    temp = 0
                    new_bytes = bytearray()

                    while (temp < len(item.bytes)):
                        size = item.bytes[temp]

                        temp += 1

                        name = item.bytes[temp:temp + size]

                        temp += size

                        position = int.from_bytes(item.bytes[temp:temp + self.size_t]) + code_size

                        temp += self.size_t

                        if (name != b"_start"):
                            new_bytes.extend(size.to_bytes(1, "big"))
                            new_bytes.extend(name)
                            new_bytes.extend(position.to_bytes(self.size_t, "big"))

                    item.bytes = bytes(new_bytes)

                code.add_table(item)


        code.code_hash = "0000000000000000000000000000000000000000"
        print(code)
        code.write()
        code.flush(self.name)
