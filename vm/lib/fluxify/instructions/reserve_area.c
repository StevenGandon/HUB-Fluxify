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

    block_t *new_area = (block_t *)malloc(sizeof(block_t));
    if (new_area == NULL) {
        fprintf(stderr, "Memory allocation failed in reserve area operation\n");
        vm->is_running = 0;
        return;
    }
    new_area->address = address;
    new_area->value = 0;
    new_area->size = (size_t)size;

    int count = 0;

    for (; vm->blocks[count] != NULL; count++);

    vm->blocks[count + 1] = new_area;
    vm->blocks[count + 2] = NULL;

    vm->program_counter += 4;
    printf("Reserved area at address: %u, size: %zu\n", address, (size_t)size);
}
