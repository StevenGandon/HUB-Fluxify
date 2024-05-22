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
    if (vm->program_counter + sizeof(int) > vm->memory_size) {
        fprintf(stderr, "Error: Not enough memory to reserve area\n");
        vm->is_running = 0;
        return;
    }

    int size = vm->memory[vm->program_counter + 1];

    vm->memory[vm->program_counter + 2] = (int)malloc(size * sizeof(int));
    printf("Reserved area of size %d at address %d\n", size, vm->memory[vm->program_counter + 2]);
}
