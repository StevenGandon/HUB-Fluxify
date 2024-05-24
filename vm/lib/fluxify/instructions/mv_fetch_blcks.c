/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_fetch_blcks
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_mv_fetch_blcks(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;
    unsigned int dest_addr = 0;

    for (unsigned int i = 0; i < 4; i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
        dest_addr |= (unsigned int)vm->fetch_char(vm, pc + 4 + i);
    }

    long int src_block = 0;

    for (int i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == dest_addr) {
            src_block = vm->blocks[i]->value;
            break;
        }
    }

    if (fetch == 0) {
        vm->fetch_src = src_block;
    } else {
        vm->fetch_dest = src_block;
    }

    vm->program_counter += 8;
    printf("MV_FETCH_BLCK 0: %ld, 1: %ld, addr: %u, fetch: %u\n", vm->fetch_src, vm->fetch_dest, dest_addr, fetch);
}
