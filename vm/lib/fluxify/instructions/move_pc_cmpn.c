/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** move_pc_cmpc
*/

#include "fluxify.h"
#include <stdio.h>

void fun_move_pc_cmpn(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;

    if (vm->fetch_src == 0) {
        vm->program_counter = (size_t)vm->fetch_dest;
    }
}
