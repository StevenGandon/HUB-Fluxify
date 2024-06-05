/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** assign_var
*/

#include "fluxify.h"
#include <string.h>
#include <stdio.h>

void fun_assign_var(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    char *var_name = (char *)vm->fetch_src;
    long int value = vm->fetch_dest;

    variable_map_t *var_map = vm->var_map;
    while (var_map) {
        if (strcmp(var_map->var_name, var_name) == 0) {
            if (var_map->var_value->value == NULL) {
                var_map->var_value->value = malloc(sizeof(long int));
            }
            *(long int *)(var_map->var_value->value) = value;
            break;
        }
        var_map = var_map->next;
    }
}