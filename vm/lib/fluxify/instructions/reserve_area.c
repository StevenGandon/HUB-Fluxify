/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** reserve_area
*/

#include "fluxify.h"
#include <stdio.h>

void fun_reserve_area(vm_state_t *vm)
{
    int size = vm->memory[vm->program_counter + 1];
    int *new_area = (int *)malloc((size_t)size * sizeof(int));

    if (new_area == NULL) {
        fprintf(stderr, "Error: Unable to allocate memory\n");
        vm->is_running = 0;
        return;
    }
    vm->memory_addresses[vm->program_counter + 2] = (intptr_t)new_area;
    vm->program_counter += 3;
}
