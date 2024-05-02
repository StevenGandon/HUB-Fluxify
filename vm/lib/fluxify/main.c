/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** main.c
*/

#include "floff.h"
#include <string.h>
#include <stdio.h>

static void load_x64_program(const char *filename)
{
    void *result = auto_floff(filename);

    if (result == NULL) {
        fprintf(stderr, "Corruped .flo file: %s\n", filename);
        return;
    }
    // TODO
    // program = convert_floff64_to_program(&floff64);
    // if (program == NULL) {
    //     fprintf(stderr, "Failed to convert .flo data to program structure\n");
    //     return NULL;
    // }
}

int main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    load_x64_program(argv[1]);
    return 0;
}
