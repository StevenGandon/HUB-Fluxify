/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** div
*/

#include "fluxify.h"
#include <stdio.h>

void fun_div(vm_state_t *vm)
{
    int reg1 = vm->memory[vm->program_counter + 1];
    int reg2 = vm->memory[vm->program_counter + 2];
    int result_reg = vm->memory[vm->program_counter + 3];

    if (reg1 < (int)vm->num_registers && reg2 < (int)vm->num_registers && result_reg < (int)vm->num_registers) {
        if (vm->registers[reg2] != 0) {
            vm->registers[result_reg] = vm->registers[reg1] / vm->registers[reg2];
        } else {
            fprintf(stderr, "Error: Division by zero\n");
            vm->is_running = 0;
        }
    } else {
        fprintf(stderr, "Error: Invalid register\n");
        vm->is_running = 0;
    }
    vm->program_counter += 4;
}
