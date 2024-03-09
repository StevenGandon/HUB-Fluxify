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
    floff64_t *object = auto_floff("../compiler/test64.flo");

    if (!object)
        return (84);
    (void)destroy_floff64(object);
    return (0);
}
