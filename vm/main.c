/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** main.c
*/

#include "floff.h"
#include "fluxify.h"
#include <string.h>
#include <unistd.h>
#include <stdio.h>

int parse_arguments(int argc, char **argv, config_t *config)
{
    int opt;
    config->arch = ARCH_X64_32;

    while ((opt = getopt(argc, argv, "a:")) != -1) {
        switch (opt) {
            case 'a':
                if (strcmp(optarg, "X86_64") == 0) {
                    config->arch = ARCH_X86_64;
                } else if (strcmp(optarg, "X64_32") == 0) {
                    config->arch = ARCH_X64_32;
                } else {
                    fprintf(stderr, "Unsupported architecture: %s\n", optarg);
                    return -1;
                }
                break;
            default:
                fprintf(stderr, "Usage: %s [-a ARCH] <filename>\n", argv[0]);
                return -1;
        }
    }

    if (optind < argc) {
        config->filename = argv[optind];
    } else {
        fprintf(stderr, "Missing filename.\n");
        return -1;
    }
    return 0;
}

static void load_program(const char *filename)
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
    config_t config;
    if (parse_arguments(argc, argv, &config) != 0)
        return 84;

    load_program(config.filename);
    return 0;
}
