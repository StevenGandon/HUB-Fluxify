/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** equal_equal
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>

void fun_equal_equal(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    long int result = vm->fetch_src == vm->fetch_dest;

    printf("EQUAL_EQUAL 0: %ld, 1: %ld\n", vm->fetch_src, vm->fetch_dest);

    if (fetch == 0) {
        vm->fetch_src = result;
    } else {
        vm->fetch_dest = result;
    }
    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
