/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** move_fetch_into_blocks
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_move_fetch_into_blocks(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t block_address = (size_t)vm->fetch_dest;
    long int value = vm->fetch_src;

    for (size_t i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == block_address) {
            vm->blocks[i]->value = value;
        }
    }
}
