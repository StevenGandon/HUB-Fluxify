/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** add
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>

void fun_reset_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    if (fetch == 0) {
        vm->fetch_src = 0;
    } else {
        vm->fetch_dest = 0;
    }

    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
