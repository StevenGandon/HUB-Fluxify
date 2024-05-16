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
    instruction_t inst;

    inst.opcode = vm->memory[vm->program_counter];
    inst.operands[0] = vm->memory[vm->program_counter + 1];
    inst.operands[1] = vm->memory[vm->program_counter + 2];
    if (inst.operands[1] != 0) {
        vm->registers[0] = inst.operands[0] / inst.operands[1];
        printf("DIV: %d / %d = %d\n", inst.operands[0], inst.operands[1], vm->registers[0]);
    } else {
        fprintf(stderr, "Error: Division by zero\n");
    }
}
