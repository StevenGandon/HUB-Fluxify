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
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int mem_addr = 0;
    unsigned int src_addr = 0;

    for (unsigned int i = 0; i < 4; i++) {
        mem_addr |= (unsigned int)vm->fetch_char(vm, pc + 1 + i) << (i * 8);
        src_addr |= (unsigned int)vm->fetch_char(vm, pc + 5 + i) << (i * 8);
    }

    if (mem_addr >= vm->memory_size || src_addr >= vm->memory_size || vm->blocks[mem_addr] == NULL || vm->blocks[src_addr] == NULL) {
        fprintf(stderr, "Invalid block address in move blocks fetch operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *src_block = vm->blocks[src_addr];
    block_t *mem_block = vm->blocks[mem_addr];

    mem_block->value = src_block->value;

    vm->fetch_dest = mem_block->value;
    vm->fetch_src = src_block->value;

    printf("Fetched dest: %ld, Fetched src: %ld\n", vm->fetch_dest, vm->fetch_src);
}
