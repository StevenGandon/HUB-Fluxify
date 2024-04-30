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
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename.flo>\n", argv[0]);
        return 84;
    }

    program_t *program = load_program(argv[1]);

    if (!program)
        return 84;
    run_program(program);
    gc_collect(program);
    free_program(program);
    return 0;
}
