/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** free
*/

#include "fluxify.h"
#include <stdio.h>

void fun_free_area(vm_state_t *vm)
{
    if (vm->program_counter + sizeof(int) > vm->memory_size) {
        fprintf(stderr, "Error: Not enough memory to free area\n");
        vm->is_running = 0;
        return;
    }

    int address = vm->memory[vm->program_counter + 1];

    free((void*)address);
    printf("Freed area at address %d\n", address);
}
