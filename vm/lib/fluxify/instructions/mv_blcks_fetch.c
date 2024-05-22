/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_blcks_fetch
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_mv_blcks_fetch(vm_state_t *vm)
{
    intptr_t source = vm->memory_addresses[vm->program_counter + 1];
    int destination_register = vm->memory[vm->program_counter + 2];
    int block_size = vm->memory[vm->program_counter + 3];

    if (destination_register < (int)vm->num_registers) {
        memcpy(&vm->registers[destination_register], (void *)source, (size_t)block_size * sizeof(int));
        vm->program_counter += 4;
    } else {
        fprintf(stderr, "Error mv_blcks_fetch: Invalid register\n");
        vm->is_running = 0;
    }
}
