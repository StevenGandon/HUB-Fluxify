/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** variable_fetch
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_variable_fetch(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t pc = vm->program_counter;
    unsigned int fetch = 0;

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    char *variable_name = (char *)vm->fetch_src;

    variable_map_t *current_var = vm->var_map;
    while (current_var != NULL) {
        if (strcmp(current_var->var_name, variable_name) == 0) {
            if (current_var->var_value->value != NULL) {
                if (fetch == 0) {
                    vm->fetch_src = *(long int *)current_var->var_value->value;
                } else {
                    vm->fetch_dest = *(long int *)current_var->var_value->value;
                }
            } else {
                fprintf(stderr, "Error: Variable '%s' has no value.\n", variable_name);
            }
            return;
        }
        current_var = current_var->next;
    }
    fprintf(stderr, "Error: Variable '%s' not found.\n", variable_name);
    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
}
