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
    unsigned int dest_addr = 0;
    unsigned int constant = 0;

    for (unsigned int i = 0; i < 4; i++) {
        dest_addr |= (unsigned int)vm->fetch_char(vm, pc + 1 + i) << (i * 8);
        constant |= (unsigned int)vm->fetch_char(vm, pc + 5 + i) << (i * 8);
    }

    if (dest_addr >= vm->memory_size || vm->blocks[dest_addr] == NULL) {
        fprintf(stderr, "Invalid block address in mv_constant_fetch operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *dest_block = vm->blocks[dest_addr];
    dest_block->value = constant;
}
