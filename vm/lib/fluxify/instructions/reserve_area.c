/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** reserve_area
*/

#include "fluxify.h"
#include <stdlib.h>
#include <stdio.h>

void fun_reserve_area(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int address = 0;
    unsigned int size = 0;

    for (unsigned int i = 0; i < 4; i++) {
        address |= (unsigned int)vm->fetch_char(vm, pc + 1 + i) << (i * 8);
        size |= (unsigned int)vm->fetch_char(vm, pc + 5 + i) << (i * 8);
    }

    if (size <= 0) {
        fprintf(stderr, "Invalid size in reserve area operation\n");
        vm->is_running = 0;
        return;
    }

    size_t new_memory_size = (size_t)address + (size_t)size;
    if (new_memory_size > vm->memory_size) {
        block_t **new_blocks = realloc(vm->blocks, new_memory_size * sizeof(block_t *));
        if (new_blocks == NULL) {
            fprintf(stderr, "Memory reallocation failed in reserve area operation\n");
            vm->is_running = 0;
            return;
        }
        vm->blocks = new_blocks;
        for (size_t i = vm->memory_size; i < new_memory_size; ++i) {
            vm->blocks[i] = NULL;
        }
        vm->memory_size = new_memory_size;
    }

    block_t *new_area = (block_t *)malloc((size_t)size * sizeof(block_t));
    if (new_area == NULL) {
        fprintf(stderr, "Memory allocation failed in reserve area operation\n");
        vm->is_running = 0;
        return;
    }

    for (unsigned int i = 0; i < size; ++i) {
        new_area[i].address = (size_t)address + i;
        new_area[i].value = 0;
        vm->blocks[address + i] = &new_area[i];
    }
}
