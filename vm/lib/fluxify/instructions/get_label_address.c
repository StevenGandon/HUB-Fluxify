/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** get_label_address
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_get_label_address(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    unsigned int fetch = 0;
    size_t pc = vm->program_counter;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    char *label_name = (char *)vm->fetch_src;

    for (size_t i = 0; i < vm->label_size; i++) {
        if (strcmp(label_name, vm->labels[i].name) == 0) {
            if (fetch == 0) {
                vm->fetch_src = (long int)vm->labels[i].position;
            } else {
                vm->fetch_dest = (long int)vm->labels[i].position;
            }
        }
    }

    printf("GET_LABEL_ADDRESS 0: %ld, 1: %ld\n", vm->fetch_src, vm->fetch_dest);
    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
