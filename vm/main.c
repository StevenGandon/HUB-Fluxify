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

static void print_usage(const char *program_name)
{
    fprintf(stderr, "Usage: %s [-arch ARCH] <filename>\n", program_name);
}

static int handle_arch_option(const char *option, config_t *config)
{
    if (strcmp(option, "X86_64") == 0) {
        config->arch = ARCH_X86_64;
    } else if (strcmp(option, "X64_32") == 0) {
        config->arch = ARCH_X64_32;
    }
    return 0;
}

static int parse_arguments(int argc, char **argv, config_t *config)
{
    int i = 1;

    config->arch = ARCH_X64_32;
    while (i < argc) {
        if (strcmp(argv[i], "-arch") == 0) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Option -arch requires an argument.\n");
                print_usage(argv[0]);
                return -1;
            }
            if (handle_arch_option(argv[i + 1], config) != 0) {
                print_usage(argv[0]);
                return -1;
            }
            i += 2;
        } else {
            config->filename = argv[i];
            i++;
        }
    }
    if (config->filename == NULL) {
        fprintf(stderr, "Missing filename.\n");
        print_usage(argv[0]);
        return -1;
    }
    return 0;
}

static void load_program(const char *filename, unsigned short arch)
{
    void *result = auto_floff(filename);

    if (result == NULL) {
        fprintf(stderr, "Corruped .flo file: %s\n", filename);
        return;
    }
    (void)arch;
}

int main(int argc, char **argv)
{
    config_t config;

    if (parse_arguments(argc, argv, &config) != 0)
        return 84;
    load_program(config.filename, config.arch);
    return 0;
}
