/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** free_area
*/

#include "fluxify.h"
#include <stdlib.h>
#include <stdio.h>

void fun_free_area(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    unsigned int address = 0;
    size_t pc = vm->program_counter;

    for (unsigned int i = 0; i < 4; i++) {
        address |= (unsigned int)vm->fetch_char(vm, pc + 1 + i);
    }

    if ((size_t)address >= vm->memory_size || vm->blocks[address] == NULL) {
        fprintf(stderr, "Invalid memory address in free area operation\n");
        vm->is_running = 0;
        return;
    }

    block_t *area_to_free = vm->blocks[address];
    if (area_to_free == NULL || area_to_free->size == 0) {
        fprintf(stderr, "Memory area already freed or invalid address\n");
        vm->is_running = 0;
        return;
    }

    size_t size = area_to_free->size;
    for (size_t i = 0; i < size; ++i) {
        if ((size_t)(address + i) >= vm->memory_size || vm->blocks[address + i] == NULL) {
            fprintf(stderr, "Memory corruption or invalid block in free area operation\n");
            vm->is_running = 0;
            return;
        }
        free(vm->blocks[address + i]);
        vm->blocks[address + i] = NULL;
    }

    vm->program_counter += 5;
    printf("Freed area starting at address: %u\n", address);
}
