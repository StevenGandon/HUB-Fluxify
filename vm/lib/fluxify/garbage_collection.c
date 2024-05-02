/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** garbage_collection.c
*/

#include "fluxify.h"

void incref(FlObject *obj)
{
    if (obj) {
        obj->ref_cnt++;
    }
}

void decref(FlObject *obj)
{
    if (obj && obj->ref_cnt-- == 0) {
        free_object(obj);
    }
}
