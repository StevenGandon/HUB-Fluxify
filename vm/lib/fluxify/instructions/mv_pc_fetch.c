/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** mv_fetc_pc
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_mv_pc_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    vm->program_counter = fetch == 0 ? (size_t)vm->fetch_src : (size_t)vm->fetch_dest;
}