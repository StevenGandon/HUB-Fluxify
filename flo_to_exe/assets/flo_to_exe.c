#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "flo_to_exe.h"
#include "fluxify.h"
#include "floff.h"

int main(int argc, char **argv)
{
    vm_state_t vm;
    void *mem = fmemopen(FILE_COMPILED, *SIZE, "r");

    vm.arch = ARCH_X86_64;
    vm.filename = "unknown_compiled_program";
    fclose(mem);
    return (0);
}
