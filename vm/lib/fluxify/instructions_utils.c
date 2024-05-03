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

void decode_and_execute_instructions(vm_state_t *vm,
    const unsigned char *byte_stream, size_t size)
{
    size_t offset = 0;

    while (vm->is_running && offset < size) {
        if (size - offset < sizeof(int)) {
            fprintf(stderr, "Unexpected end of instruction stream\n");
            break;
        }
        instruction_t inst;

        inst.opcode = byte_stream[offset];
        memcpy(&inst.operands[0], byte_stream + offset + 1, sizeof(int));
        memcpy(&inst.operands[1], byte_stream + offset + 5, sizeof(int));
        adjust_endianness(&inst.operands[0]);
        adjust_endianness(&inst.operands[1]);
        //execute_instruction(vm, &inst);
        offset += 9;
    }
}
