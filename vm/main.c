/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** main.c
*/

#include "fluxify.h"
#include "floff.h"
#include "main.h"
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int
main(argc, argv)
    int argc;
    char **argv;
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
