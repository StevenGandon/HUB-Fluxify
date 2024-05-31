/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_constant_fetch
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>

void fun_mv_constant_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;
    unsigned int dest_addr = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
        dest_addr |= (unsigned int)vm->fetch_char(vm, pc + (vm->arch == ARCH_X86_64 ? 8 : 4) + i);
    }

    long int dest_block = dest_addr >= vm->constant_size ? 0 : vm->constants[dest_addr];

    if (fetch == 0) {
        vm->fetch_src = dest_block;
    } else {
        vm->fetch_dest = dest_block;
    }

    vm->program_counter += vm->arch == ARCH_X86_64 ? 16 : 8;

    printf("MV_CONST_FETCH 0: %ld, 1: %ld, addr: %u, fetch: %u\n", vm->fetch_src, vm->fetch_dest, dest_addr, fetch);
}
