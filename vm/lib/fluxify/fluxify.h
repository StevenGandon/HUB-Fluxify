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

#endif /* FLOFF_H_ */
