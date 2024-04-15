/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** garbage_collection.c
*/

#include "fluxify.h"

void incref(FlObject *obj)
{
    if (obj)
        obj->ref_cnt++;
}

void decref_members(FlObject *obj)
{
    if (obj->object_type && obj->object_type->members) {
        struct _member_list_s **members = obj->object_type->members;
        for (int i = 0; members[i]; i++)
            decref(members[i]->value);
    }
}

void decref(FlObject *obj)
{
    if (obj && --obj->ref_cnt == 0) {
        decref_members(obj);
        free(obj);
    }
}
