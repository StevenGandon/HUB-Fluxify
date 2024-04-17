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
#include "command_line.h"

command_line_args_t *parse_arguments(int argc, char **argv)
{
    command_line_args_t *args = malloc(sizeof(command_line_args_t));
    if (!args) exit(84);

    int option;
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

    if (args->arch) {
        printf("Architecture: %s\n", args->arch);
    }
    printf("Filename: %s\n", args->filename);

    free(args);
    return 0;
}
