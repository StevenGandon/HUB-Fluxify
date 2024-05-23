/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_constant_fetch
*/

#include "fluxify.h"
#include <stdio.h>

void fun_mv_constant_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;
    unsigned int dest_addr = 0;

    for (unsigned int i = 0; i < 4; i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
        dest_addr |= (unsigned int)vm->fetch_char(vm, pc + 4 + i);
    }

    long int dest_block = dest_addr >= vm->constant_size ? 0 : vm->constants[dest_addr];

    if (fetch == 0) {
        vm->fetch_src = dest_block;
    } else {
        vm->fetch_dest = dest_block;
    }

    printf("Fetched dest: %ld, Fetched constant: %ld\n", vm->fetch_dest, vm->fetch_src);
}
