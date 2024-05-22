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
    int dest_addr = inst->operands[0];
    int src_addr = inst->operands[1];

    if (vm->blocks[dest_addr] == NULL || vm->blocks[src_addr] == NULL) {
        fprintf(stderr, "Invalid block address in mv_fetch_blcks operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *dest_block = vm->blocks[dest_addr];
    block_t *src_block = vm->blocks[src_addr];

    dest_block->value = src_block->value;
}
