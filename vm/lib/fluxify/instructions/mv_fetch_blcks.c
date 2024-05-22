/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_fetch_blcks
*/

#include "fluxify.h"
#include <stdio.h>

void fun_mv_fetch_blcks(vm_state_t *vm)
{
    if (vm->program_counter + 2 * sizeof(int) > vm->memory_size) {
        fprintf(stderr, "Error: Not enough memory to move fetch blocks\n");
        vm->is_running = 0;
        return;
    }

    int source = vm->memory[vm->program_counter + 1];
    int destination = vm->memory[vm->program_counter + 2];
    int block_size = vm->memory[vm->program_counter + 3];

    memcpy((void*)destination, (void*)source, block_size * sizeof(int));
    printf("Moved %d blocks from address %d to address %d\n", block_size, source, destination);
}
