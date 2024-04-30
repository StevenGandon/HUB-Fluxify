/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** object.c
*/

#include "fluxify.h"

FlObject *create_object(_type_object_t *object_type)
{
    FlObject *obj = malloc(sizeof(FlObject));

    if (!obj)
        return NULL;
    obj->ref_cnt = 1;
    obj->object_type = object_type;
    return obj;
}

void delete_object(FlObject *obj)
{
    if (!obj)
        return;
    if (--obj->ref_cnt == 0)
        free(obj);
}

void free_object(FlObject *obj)
{
    if (obj == NULL)
        return;
    for (_member_list_t **members = obj->object_type->members; members && *members; members++)
        decref((*members)->value);
    free(obj);
}
