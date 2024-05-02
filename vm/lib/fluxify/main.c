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
    floff64_t floff64;
    int result = 0;

    memset(&floff64, 0, sizeof(floff64));
    result = read_floff64(&floff64, filename);
    if (result == -1) {
        fprintf(stderr, "Failed to read .flo file: %s\n", filename);
        return;
    }
    // TODO
    // program = convert_floff64_to_program(&floff64);
    // if (program == NULL) {
    //     fprintf(stderr, "Failed to convert .flo data to program structure\n");
    //     return NULL;
    // }
    destroy_floff64(&floff64);
}

int main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    load_x64_program(argv[1]);
    return 0;
}
