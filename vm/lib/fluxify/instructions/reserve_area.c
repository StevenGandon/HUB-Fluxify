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
    unsigned int address = 0;
    size_t pc = vm->program_counter;
    long int size = sizeof(long int);

    // Fetch address from instruction
    for (unsigned int i = 0; i < 4; i++) {
        address |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    if (size <= 0) {
        fprintf(stderr, "Invalid size in reserve area operation\n");
        vm->is_running = 0;
        return;
    }

    if ((size_t)address + (size_t)size > vm->memory_size) {
        size_t new_memory_size = (size_t)address + (size_t)size;
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

    int count = 0;

    for (; vm->blocks[count] != NULL; ++count);

    block_t **new_blocks = realloc(vm->blocks, (long unsigned int)(count + 2) * sizeof(block_t *));
    if (new_blocks == NULL) {
        fprintf(stderr, "Memory reallocation failed in reserve area operation\n");
        vm->is_running = 0;
        return;
    }
    vm->blocks = new_blocks;

    vm->blocks[count] = malloc(sizeof(block_t));
    if (vm->blocks[count] == NULL) {
        fprintf(stderr, "Memory allocation failed for new block\n");
        vm->is_running = 0;
        return;
    }
    vm->blocks[count]->address = address;
    vm->blocks[count]->value = 0;
    vm->blocks[count + 1] = NULL;

    vm->program_counter += 4;
    printf("Reserved area: %u, size: %zu\n", address, (size_t)size);
}
