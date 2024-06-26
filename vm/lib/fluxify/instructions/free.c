/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** free_area
*/

#include "floff.h"
#include "fluxify.h"
#include <stdlib.h>
#include <stdio.h>

void fun_free_area(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    unsigned int address = 0;
    size_t pc = vm->program_counter;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        address |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    if (!vm->blocks) {
        vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
        return;
    }

    size_t count = 0;
    size_t dec = 0;

    for (; vm->blocks[count] != NULL; ++count) {};

    if (count) {
        block_t **array = malloc(sizeof(block_t *) * count);
        size_t i = 0;

        for (; i < count; i++) {
            if (vm->blocks[i]->address == address) {
                dec += 1;
                free(vm->blocks[i]);
                continue;
            }
            array[i - dec] = vm->blocks[i];
        }
        array[i - dec] = NULL;
        free(vm->blocks);
        vm->blocks = array;
    } else {
        free(vm->blocks);
        vm->blocks = NULL;
    }

    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
