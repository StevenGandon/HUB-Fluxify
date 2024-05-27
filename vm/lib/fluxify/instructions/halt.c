/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** free_area
*/

#include "fluxify.h"
#include <stdlib.h>
#include <stdio.h>

void fun_halt(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    unsigned int status = 0;
    size_t pc = vm->program_counter;

    status = (unsigned int)vm->fetch_char(vm, pc);

    vm->is_running = 0;
    vm->fetch_src = status;

    vm->program_counter += 1;
}
