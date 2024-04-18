/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** object.c
*/

#include "fluxify.h"

FlObject *create_object(struct _type_object_s *object_type)
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

struct _type_object_s *create_type(const char *name,
    struct _type_object_s *parent_type)
{
    struct _type_object_s *type = malloc(sizeof(struct _type_object_s));

    if (!type)
        return NULL;
    type->name = name;
    type->members = NULL;
    type->parent_type = parent_type;
    return type;
}

void delete_type(struct _type_object_s *type)
{
    if (!type)
        return;
    free(type);
}
