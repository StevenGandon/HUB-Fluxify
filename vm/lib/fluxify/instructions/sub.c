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
    instruction_t inst;

    inst.opcode = vm->memory[vm->program_counter];
    inst.operands[0] = vm->memory[vm->program_counter + 1];
    inst.operands[1] = vm->memory[vm->program_counter + 2];
    vm->registers[0] = inst.operands[0] - inst.operands[1];
    printf("SUB: %d - %d = %d\n", inst.operands[0], inst.operands[1], vm->registers[0]);
}
