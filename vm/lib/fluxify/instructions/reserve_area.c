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
    int address = inst->operands[0];
    int size = inst->operands[1];

    if ((size_t)address >= vm->memory_size) {
        fprintf(stderr, "Invalid memory address in reserve area operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *new_area = (block_t *)malloc((size_t)size * sizeof(block_t));
    if (new_area == NULL) {
        fprintf(stderr, "Memory allocation failed in reserve area operation\n");
        vm->is_running = 0;
        return;
    }

    for (size_t i = 0; i < (size_t)size; ++i) {
        new_area[i].adress = (size_t)address + i;
        new_area[i].value = 0;
    }

    vm->blocks[address] = new_area;
}
