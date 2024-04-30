/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** fluxify.h
*/

#ifndef FLUXIFY_H_
    #define FLUXIFY_H_

    #include <stdint.h>
    #include <stdlib.h>

    typedef struct _object_s FlObject;

    typedef struct _member_list_s {
        const char *name;
        FlObject *value;
    } _member_list_t;

    typedef struct _type_object_s {
        const char *name;
        struct _member_list_s **members;
        struct _type_object_s *parent_type;
    } _type_object_t;

    struct _object_s {
        size_t ref_cnt;
        _type_object_t *object_type;
    };

    typedef struct header64_s {
        uint32_t magic;
        uint16_t format_version;
        uint16_t architecture;
        uint8_t compiler_name_size;
        char *compiler_name;
        uint8_t program_hash[40];
        uint64_t table_number;
        uint64_t start_label_address;
    } header64_t;

    typedef enum {
        NOOP = 0, ADD, SUB
    } InstructionCode;

    typedef struct instruction_s {
        InstructionCode code;
        int args[2];
    } instructions_t;

    typedef struct label_s {
        char *label;
        uint64_t address; // uint32_t for 32 bits ?
    } label_t;

    typedef struct constant_s {
        int type;
        union {
            int i;
            char *s;
        } value;
    } constant_t;

    typedef struct program_s {
        struct instruction_s *instructions;
        size_t num_instructions;
        struct label_s *labels;
        size_t num_labels;
        struct constant_s *constants;
        size_t num_constants;
        FlObject **objects;
        size_t num_objects;
        size_t capacity_objects;
    } program_t;

    FlObject *create_object(_type_object_t *type);
    void delete_object(FlObject *obj);
    void free_object(FlObject *obj);

    void incref(FlObject *obj);
    void decref(FlObject *obj);

    program_t *load_program(const char *filename);
    void run_program(program_t *program);
    void free_program(program_t *program);

    void gc_collect(program_t *program);

#endif /* FLUXIFY_H_ */
