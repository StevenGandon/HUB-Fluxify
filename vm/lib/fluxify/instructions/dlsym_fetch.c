/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** dlsym_fetch
*/

#include "floff.h"
#include "fluxify.h"
#include <dlfcn.h>
#include <stdio.h>

void fun_dlsym_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    void *lib_handle = (void *)vm->fetch_src;
    char *symbol_name = (char *)vm->fetch_dest;

    void *symbol = dlsym(lib_handle, symbol_name);
    if (!symbol) {
        vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
        return;
    }

    if (fetch == 0) {
        vm->fetch_src = (long int)symbol;
    } else {
        vm->fetch_dest = (long int)symbol;
    }

    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
