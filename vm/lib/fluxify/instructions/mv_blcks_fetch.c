/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_blcks_fetch
*/

#include "fluxify.h"
#include <stdio.h>

void fun_mv_blcks_fetch(vm_state_t *vm)
{
    if (vm->program_counter + 2 * sizeof(int) > vm->memory_size) {
        fprintf(stderr, "Error: Not enough memory to move blocks to fetch\n");
        vm->is_running = 0;
        return;
    }

    int source = vm->memory[vm->program_counter + 1];
    int destination_register = vm->memory[vm->program_counter + 2];
    int block_size = vm->memory[vm->program_counter + 3];

    if (destination_register < vm->num_registers) {
        memcpy(&vm->registers[destination_register], (void*)source, block_size * sizeof(int));
        printf("Moved %d blocks from address %d to register %d\n", block_size, source, destination_register);
    } else {
        fprintf(stderr, "Error: Invalid register\n");
        vm->is_running = 0;
    }
}