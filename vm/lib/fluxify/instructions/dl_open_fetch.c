/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** div
*/

#include "floff.h"
#include "fluxify.h"
#include <dlfcn.h>
#include <string.h>
#include <stdio.h>

void fun_div(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    char *lib_name = (char *)vm->fetch_src;

    void *handle = dlopen(lib_name, RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "Error: Unable to load library '%s': %s\n", lib_name, dlerror());
        vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
        return;
    }

    if (fetch == 0) {
        vm->fetch_src = (long int)handle;
    } else {
        vm->fetch_dest = (long int)handle;
    }

    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
