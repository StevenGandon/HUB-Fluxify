/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** create_var
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_create_var(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;

    char *var_name = (char *)vm->fetch_src;
    FloVar *new_var = (FloVar *)malloc(sizeof(FloVar));
    if (!new_var) {
        return;
    }
    new_var->ref_cnt = 1;
    new_var->value = NULL;

    variable_map_t *new_var_map = (variable_map_t *)malloc(sizeof(variable_map_t));
    if (!new_var_map) {
        free(new_var);
        return;
    }

    printf("Creating variable '%p'\n", var_name);
    fflush(stdout);

    new_var_map->var_name = var_name;
    new_var_map->var_value = new_var;
    new_var_map->next = vm->var_map;
    vm->var_map = new_var_map;
}