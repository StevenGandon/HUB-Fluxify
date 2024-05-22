/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** instruction_utils
*/

#include "fluxify.h"
#include <string.h>
#include <stdio.h>

void adjust_endianness(int *value)
{
    unsigned int uval = (unsigned int)(*value);

    uval = ((uval >> 24) & 0xff) |
           ((uval << 8) & 0xff0000) |
           ((uval >> 8) & 0xff00) |
           ((uval << 24) & 0xff000000);
    *value = (int)uval;
}

void execute_instruction(vm_state_t *vm, instruction_t *inst)
{
    switch (inst->opcode) {
        case OP_ADD:
            fun_add(vm);
            break;
        case OP_SUB:
            fun_sub(vm);
            break;
        case OP_MUL:
            fun_mul(vm);
            break;
        case OP_DIV:
            fun_div(vm);
            break;
        case OP_RESERVE_AREA:
            fun_reserve_area(vm);
            break;
        case OP_FREE_AREA:
            fun_free_area(vm);
            break;
        case OP_MV_FETCH_BLCKS:
            fun_mv_fetch_blcks(vm);
            break;
        case OP_MV_BLCKS_FETCH:
            fun_mv_blcks_fetch(vm);
            break;
        case OP_MV_CONSTANT_FETCH:
            fun_mv_constant_fetch(vm);
            break;
        default:
            fprintf(stderr, "Unknown opcode: %d\n", inst->opcode);
            vm->is_running = 0;
            break;
    }
}

void decode_and_execute_instructions(vm_state_t *vm,
    const unsigned char *byte_stream, size_t size)
{
    while (vm->is_running && vm->program_counter < size) {
        if (size - vm->program_counter < 9) {
            fprintf(stderr, "Unexpected end of instruction stream\n");
            break;
        }
        instruction_t inst;

        inst.opcode = byte_stream[vm->program_counter];
        memcpy(&inst.operands[0], byte_stream + vm->program_counter + 1, sizeof(int));
        memcpy(&inst.operands[1], byte_stream + vm->program_counter + 5, sizeof(int));
        adjust_endianness(&inst.operands[0]);
        adjust_endianness(&inst.operands[1]);
        execute_instruction(vm, &inst);
        vm->program_counter += 9;
    }
}
