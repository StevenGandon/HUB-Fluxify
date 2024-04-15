/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** fluxify.h
*/

#ifndef FLUXIFY_H_
    #define FLUXIFY_H_

    #include <stdlib.h>

    struct _object_s;

    struct _member_list_s {
        const char *name;

        struct _object_s *value;
    };

    struct _type_object_s {
        const char *name;

        struct _member_list_s **members;

        struct _type_object_s *parent_type;
    };

    struct _object_s {
        size_t ref_cnt;

        struct _type_object_s *object_type;
    };

    typedef struct _object_s FlObject;

    FlObject *create_object(struct _type_object_s *object_type);
    void delete_object(FlObject *obj);
    struct _type_object_s *create_type(const char *name, struct _type_object_s *parent_type);
    void delete_type(struct _type_object_s *type);
    void incref(FlObject *obj);
    void decref_members(FlObject *obj);
    void decref(FlObject *obj);

#endif /* FLUXIFY_H_ */
