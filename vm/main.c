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
    floff32_t *object = auto_floff("../compiler/test32.flo");

    if (!object)
        return (84);
    (void)destroy_floff32(object);
    return (0);
}
