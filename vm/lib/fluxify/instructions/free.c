/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** free
*/

#include "fluxify.h"
#include <stdio.h>
#include <stdlib.h>

void fun_free_area(vm_state_t *vm, instruction_t *inst)
{
    int address = inst->operands[0];

    if ((size_t)address >= vm->memory_size || vm->blocks[address] == 0) {
        fprintf(stderr, "Invalid memory address in free area operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *area_to_free = (block_t *)vm->blocks[address];
    if (area_to_free == NULL) {
        fprintf(stderr, "Memory area already freed or invalid address\n");
        vm->is_running = 0;
        return;
    }

    free(area_to_free);
    vm->blocks[address] = 0;
}
