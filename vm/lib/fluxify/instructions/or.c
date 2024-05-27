/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** add
*/

#include "fluxify.h"
#include <stdio.h>

void fun_or(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < 4; i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    long int result = vm->fetch_src | vm->fetch_dest;

    printf("OR 0: %ld, 1: %ld\n", vm->fetch_src, vm->fetch_dest);

    if (fetch == 0) {
        vm->fetch_src = result;
    } else {
        vm->fetch_dest = result;
    }
    vm->program_counter += 4;
}
