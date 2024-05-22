/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_blcks_fetch
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_mv_blcks_fetch(vm_state_t *vm, instruction_t *inst)
{
    int mem_addr = inst->operands[0];
    int src_addr = inst->operands[1];

    if ((size_t)mem_addr >= vm->memory_size || (size_t)src_addr >= vm->memory_size) {
        fprintf(stderr, "Invalid memory address in move blocks fetch operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *src_block = (block_t *)vm->blocks[src_addr];

    if (vm->blocks[mem_addr] == NULL || src_block == NULL) {
        fprintf(stderr, "Invalid block address in move blocks fetch operation\n");
        vm->is_running = 0;
        return;
    }

    vm->blocks[mem_addr]->value = src_block->value;
}
