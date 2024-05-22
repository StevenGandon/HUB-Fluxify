/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** sub
*/

#include "fluxify.h"
#include <stdio.h>

void fun_sub(vm_state_t *vm)
{
    int reg1 = vm->memory[vm->program_counter + 1];
    int reg2 = vm->memory[vm->program_counter + 2];
    int result_reg = vm->memory[vm->program_counter + 3];

    if (reg1 < (int)vm->num_registers && reg2 < (int)vm->num_registers && result_reg < (int)vm->num_registers) {
        vm->registers[result_reg] = vm->registers[reg1] - vm->registers[reg2];
    } else {
        fprintf(stderr, "Error sub: Invalid register\n");
        vm->is_running = 0;
    }
    vm->program_counter += 4;
}
