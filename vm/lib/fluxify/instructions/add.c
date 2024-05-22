/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** add
*/

#include "fluxify.h"
#include <stdio.h>

#include "fluxify.h"
#include <stdio.h>

void fun_add(vm_state_t *vm, instruction_t *inst)
{
    int dest_addr = inst->operands[0];
    int src_addr1 = inst->operands[1];
    int src_addr2 = inst->operands[2];

    if (vm->blocks[dest_addr] == NULL || vm->blocks[src_addr1] == NULL || vm->blocks[src_addr2] == NULL) {
        fprintf(stderr, "Invalid block address in add operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *dest_block = vm->blocks[dest_addr];
    block_t *src_block1 = vm->blocks[src_addr1];
    block_t *src_block2 = vm->blocks[src_addr2];

    dest_block->value = src_block1->value + src_block2->value;
}
