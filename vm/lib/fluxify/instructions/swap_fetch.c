/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** sub
*/

#include "fluxify.h"
#include <stdio.h>

void fun_swap_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    long int temp_src = vm->fetch_src;
    long int temp_dest = vm->fetch_dest;

    vm->fetch_src = temp_dest;
    vm->fetch_dest = temp_src;

    printf("SWAP_FETCH 0: %ld, 1: %ld\n", vm->fetch_src, vm->fetch_dest);
}
