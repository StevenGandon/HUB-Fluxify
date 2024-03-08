/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** main.c
*/

#include "fluxify.h"
#include "floff.h"
#include "main.h"

int
main(argc, argv)
    int argc;
    char **argv;
{
    (void)argc;
    (void)argv;
    floff64_t *object = create_floff64();

    if (read_floff64(object, "../compiler/test64.flo") < -1)
        return (84);
    return (0);
}
