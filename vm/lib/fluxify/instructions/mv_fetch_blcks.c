/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_fetch_blcks
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_mv_fetch_blcks(vm_state_t *vm)
{
    intptr_t source = vm->memory_addresses[vm->program_counter + 1];
    intptr_t destination = vm->memory_addresses[vm->program_counter + 2];
    int block_size = vm->memory[vm->program_counter + 3];

    memcpy((void *)destination, (void *)source, (size_t)block_size * sizeof(int));
    vm->program_counter += 4;
}
