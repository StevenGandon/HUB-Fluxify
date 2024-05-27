/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** main.c
*/

#include "fluxify.h"
#include <stdio.h>

int main(int argc, char **argv)
{
    vm_state_t vm;

    if (parse_arguments(argc, argv, &vm) != 0)
        return 84;
    return load_program(&vm);
}
