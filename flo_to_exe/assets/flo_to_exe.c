#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "flo_to_exe.h"
#include "fluxify.h"
#include "floff.h"

int launch_vm(vm_state_t *vm, FILE *program, short arch)
{
    void *result;

    if (arch == ARCH_X64_32) {
        result = create_floff32();
        if (result)
            read_floff32_fp(result, program);
    } else {
        result = create_floff64();
        if (result)
            read_floff64_fp(result, program);
    }

    if (result == NULL) {
        fprintf(stderr, "Invalid .flo file: %s\n", vm->filename);
        return (1);
    }

    printf("Architecture: %hu\n", (unsigned short)vm->arch);
    printf("Architecture file: %hu\n", (unsigned short)((floff32_t *)result)->architecture);

    if (((floff32_t *)result)->architecture != vm->arch) {
        printf("Incompatible architecture, architecture passed as argument is not the same as the file architecture.\n");
        return (1);
    }

    if (vm->arch == ARCH_X86_64) {
        floff64_t *flo_data = (floff64_t *)result;

        load_constants64(flo_data, vm);
        load_instructions64(flo_data, vm);
        load_labels64(flo_data, vm);
        printf("Loaded 64-bit .flo file successfully.\n");
        return execute_program(vm);
    } else if (vm->arch == ARCH_X64_32) {
        floff32_t *flo_data = (floff32_t *)result;

        load_constants32(flo_data, vm);
        load_instructions32(flo_data, vm);
        load_labels32(flo_data, vm);
        printf("Loaded 32-bit .flo file successfully.\n");
        return execute_program(vm);
    }
    return (1);
}

int main(int argc, char **argv)
{
    vm_state_t vm;
    int ret = 0;
    unsigned char *buffer = malloc(*SIZE);

    if (!buffer)
        return 84;
    memcpy(buffer, FILE_COMPILED, *SIZE);

    FILE *mem = fopen(FILE_COMPILED, "wb+");
    if (!mem) {
        fprintf(stderr, "Error opening file.\n");
        free(buffer);
        return 84;
    }

    vm.filename = "unknown_compiled_program";

    fwrite(buffer, (vm.arch == ARCH_X86_64 ? 8 : 4), *SIZE, mem);
    fflush(mem);
    rewind(mem);

    fseek(mem, 6, SEEK_SET);

    *(((unsigned char *)&vm.arch) + 1) = (unsigned char)getc(mem);
    *(((unsigned char *)&vm.arch)) = (unsigned char)getc(mem);

    rewind(mem);

    ret = launch_vm(&vm, mem, vm.arch);

    fclose(mem);
    return (ret);
}
