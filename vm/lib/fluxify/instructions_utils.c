/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** instruction_utils
*/

#include "fluxify.h"
#include <string.h>
#include <stdbool.h>
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
    bool find = false;

    for (int i = 0; OPCODES[i].callback != NULL; i++){
        if (OPCODES[i].code == inst->opcode){
            OPCODES[i].callback(vm, inst);
            find = true;
            break;
        }
    }
    if (!find){
        fprintf(stderr, "Unknown opcode: %d\n", inst->opcode);
        vm->is_running = 0;
    }
}

char run_vm(vm_state_t *vm)
{
    while (vm->is_running) {
        instruction_t instruction;

        instruction.opcode = vm->fetch_char(vm, vm->program_counter);

        vm->program_counter += 1;

        execute_instruction(vm, &instruction);

        // inst.opcode = byte_stream[vm->program_counter];
        // memcpy(&inst.operands[0], byte_stream + vm->program_counter + 1, sizeof(int));
        // memcpy(&inst.operands[1], byte_stream + vm->program_counter + 5, sizeof(int));
        // memcpy(&inst.operands[2], byte_stream + vm->program_counter + 9, sizeof(int));
        // adjust_endianness(&inst.operands[0]);
        // adjust_endianness(&inst.operands[1]);
        // adjust_endianness(&inst.operands[2]);
        // if (vm->program_counter > vm->program_size)
        //     return;
        printf("%ld\n", vm->program_counter);
    }

    return ((char)vm->fetch_src);
}
