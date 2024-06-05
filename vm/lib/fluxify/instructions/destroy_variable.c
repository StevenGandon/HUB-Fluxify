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

    variable_map_t *to_delete_prev = NULL;
    variable_map_t *to_delete = NULL;
    variable_map_t *to_delete_next = NULL;

    while (current != NULL) {
        if (strcmp(current->var_name, var_name) == 0) {
            to_delete_prev = prev;
            to_delete = current;
            to_delete_next = current->next;
        }

        prev = current;
        current = current->next;
    }

    if (to_delete == NULL)
        fprintf(stderr, "Variable not found (destroy_variable)\n");
    else {
        if (to_delete_prev == NULL) {
            vm->var_map = to_delete_next;
        } else {
            to_delete_prev->next = to_delete_next;
        }

        free(to_delete);
    }
}