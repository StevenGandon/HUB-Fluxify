def gen_code(binary, fp):
    __l = 0

    with open(binary, "rb") as f:
        __l = len(f.read())

    fp.write('#include "flo_to_exe.h"\n')
    fp.write("char FILE_COMPILED[] = {\n  ")

    with open(binary, "rb") as f:
        for i in range(__l):
            fp.write(hex(int.from_bytes(f.read(1), "big")))

            if i != __l - 1:
                fp.write(', ' if i % 11 != 10 else ',')

            if (i % 11 == 10):
                fp.write('\n  ')

    fp.write("\n};\n")
    fp.write("int SIZE[] = {" + str(__l) + "};\n")
    return (0)