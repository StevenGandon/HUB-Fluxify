/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** destroy_variable
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_destroy_variable(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    char *var_name = (char *)vm->fetch_src;

    variable_map_t *prev = NULL;
    variable_map_t *current = vm->var_map;

    while (current != NULL) {
        if (strcmp(current->var_name, var_name) == 0) {
            if (prev == NULL) {
                vm->var_map = current->next;
            } else {
                prev->next = current->next;
            }
            
            free(current->var_name);
            free(current->var_value);
            free(current);
            return;
        }

        prev = current;
        current = current->next;
    }
}