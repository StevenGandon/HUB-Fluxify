/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** move_fetch_into_blocks_bis
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_move_blocks_into_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t block_address = (size_t)vm->fetch_src;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, vm->program_counter + i);
    }

    for (size_t i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == block_address) {
            if (fetch == 0) {
                vm->fetch_src = vm->blocks[i]->value;
            } else {
                vm->fetch_dest = vm->blocks[i]->value;
            }
        }
    }
    printf("MV_BLCK_FETCH 0: %ld, 1: %ld, fetch: %u\n", vm->fetch_src, vm->fetch_dest, fetch);
}
