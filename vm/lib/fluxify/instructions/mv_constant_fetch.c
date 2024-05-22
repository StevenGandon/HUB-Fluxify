/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_constant_fetch
*/

#include "fluxify.h"
#include <stdio.h>

void fun_mv_constant_fetch(vm_state_t *vm)
{
    if (vm->program_counter + 2 * sizeof(int) > vm->memory_size) {
        fprintf(stderr, "Error: Not enough memory to move constant fetch\n");
        vm->is_running = 0;
        return;
    }

    int constant = vm->memory[vm->program_counter + 1];
    int destination = vm->memory[vm->program_counter + 2];

    memcpy((void*)destination, &constant, sizeof(int));
    printf("Moved constant %d to address %d\n", constant, destination);
}
