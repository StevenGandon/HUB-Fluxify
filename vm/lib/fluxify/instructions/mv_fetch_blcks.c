/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_fetch_blcks
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_mv_fetch_blcks(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;
    unsigned int dest_addr = 0;

    for (unsigned int i = 0; i < 4; i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
        dest_addr |= (unsigned int)vm->fetch_char(vm, pc + 4 + i);
    }

    for (int i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == dest_addr) {
            vm->blocks[i]->value = fetch == 0 ? vm->fetch_src : vm->fetch_dest;
            break;
        }
    }

    vm->program_counter += 8;
    printf("Fetched dest: %ld, Fetched src: %ld\n", vm->fetch_dest, vm->fetch_src);
}
