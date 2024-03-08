/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** floff64.c
*/

#include "floff.h"

#include <stdlib.h>
#include <string.h>

floff32_t *
create_floff32(void)
{
    floff32_t *object = (floff32_t *)malloc(sizeof(floff32_t));

    if (!object)
        return (NULL);
    object->body = NULL;

    object->compiler_name = strdup("fcc");
    object->compiler_name_size = 3;

    (void)memcpy(object->magic, DEFAULT_MAGIC, 4);
    (void)memcpy(object->version, "10", 2);

    (void)memset(object->program_hash, (int)'0', 40);

    object->start_label_address = 0;
    object->table_number = 0;
    object->architecture = ARCH_X86_64;
    return (object);
}
