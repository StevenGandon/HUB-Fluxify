/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** move_fetch_into_blocks_bis
*/

#include "fluxify.h"
#include <stdio.h>

void fun_move_fetch_into_blocks_bis(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t block_address = (size_t)vm->fetch_src;
    long int value = vm->fetch_dest;

    for (size_t i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == block_address) {
            vm->blocks[i]->value = value;
        }
    }
}
