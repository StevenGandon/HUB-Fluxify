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
    intptr_t address = vm->memory_addresses[vm->program_counter + 1];

    free((void *)address);
    vm->program_counter += 2;
}
