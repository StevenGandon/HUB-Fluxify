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
    int constant = vm->memory[vm->program_counter + 1];
    intptr_t destination = vm->memory_addresses[vm->program_counter + 2];

    *((int *)destination) = constant;
    vm->program_counter += 3;
}
