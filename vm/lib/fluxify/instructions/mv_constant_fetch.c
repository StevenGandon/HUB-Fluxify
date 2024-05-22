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
    int dest_addr = inst->operands[0];
    int constant = inst->operands[1];

    if (vm->blocks[dest_addr] == NULL) {
        fprintf(stderr, "Invalid block address in mv_constant_fetch operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *dest_block = vm->blocks[dest_addr];

    dest_block->value = constant;
}
