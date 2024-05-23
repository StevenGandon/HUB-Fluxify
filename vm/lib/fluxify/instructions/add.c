/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** add
*/

#include "fluxify.h"
#include <stdio.h>

void fun_add(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int dest_addr = 0;
    unsigned int src_addr1 = 0;
    unsigned int src_addr2 = 0;

    for (unsigned int i = 0; i < 4; i++) {
        dest_addr |= (unsigned int)vm->fetch_char(vm, pc + 1 + i);
        src_addr1 |= (unsigned int)vm->fetch_char(vm, pc + 5 + i);
        src_addr2 |= (unsigned int)vm->fetch_char(vm, pc + 9 + i);
    }

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
