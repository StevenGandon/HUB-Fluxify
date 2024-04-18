/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** main.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <string.h>
#include "vm.h"
#include "command_line.h"

command_line_args_t *parse_arguments(int argc, char **argv)
{
    command_line_args_t *args = malloc(sizeof(command_line_args_t));
    int option = 0;

    if (!args) {
        free(args);
        exit(84);
    }
    while ((option = getopt(argc, argv, "a:f:")) != -1) {
        switch (option) {
            case 'a':
                args->arch = optarg;
                break;
            case 'f':
                args->filename = optarg;
                break;
            default:
                fprintf(stderr, "Usage: %s -a <arch> -f <filename>\n", argv[0]);
                exit(84);
        }
    }
    return args;
}

int main(int argc, char **argv)
{
    command_line_args_t *args = parse_arguments(argc, argv);
    program_table_t program_table;
    label_table_t label_table;
    constants_table_t constants;

    if (read_flo_file(args->filename, &program_table, &label_table, &constants) != 0) {
        printf("Failed to read the .flo object file: %s\n", args->filename);
        return 84;
    }
    free(args);
        free(program_table.instructions);
    for (size_t i = 0; i < label_table.size; ++i)
        free(label_table.label_names[i]);
    free(label_table.label_names);
    free(label_table.ref_dests);
    for (size_t i = 0; i < constants.size; ++i)
        free(constants.constants[i].value);
    free(constants.constants);
    return 0;
}
