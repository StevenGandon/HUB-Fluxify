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

    #define OP_NOOP 0
    #define OP_ADD  1
    #define OP_SUB  2
    #define OP_MUL  3
    #define OP_DIV  4
    #define OP_RESERVE_AREA 0x43
    #define OP_FREE_AREA 0x44
    #define OP_MV_FETCH_BLCKS 0x45
    #define OP_MV_BLCKS_FETCH 0x46
    #define OP_MV_CONSTANT_FETCH 0x47

    typedef enum {
        FLO_TYPE_INT = 1,
        FLO_TYPE_STRING = 2
    } FloType;

    typedef struct {
        int64_t ref_cnt;
        void *value;
    } FloVar;

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

    typedef struct config_s {
        const char *filename;
        unsigned short arch;
    } config_t;

    typedef struct instruction_s {
        int opcode;
        int operands[3];
    } instruction_t;

    typedef struct variable_map_s {
        char *var_name;
        FloVar *var_value;
        struct variable_map_s *next;
    } variable_map_t;

    typedef struct block_s {
        size_t address;
        long int value;
    } block_t;

    typedef struct vm_state_s {

        int is_running;
        unsigned short arch;
        const char *filename;

        size_t program_counter;
        size_t memory_size;
        variable_map_t *var_map;

        long int fetch_dest;
        long int fetch_src;
        block_t **blocks;

        size_t program_size;
        unsigned char *program;

        size_t constant_size;
        long int *constants;

        unsigned char (*fetch_char)(struct vm_state_s *vm, size_t offset);
    } vm_state_t;

    void run_vm(vm_state_t *vm);
    int parse_arguments(int argc, char **argv, vm_state_t *config);
    void adjust_endianness(int *value);
    void execute_instruction(vm_state_t *vm, instruction_t *inst);
    void initialize_vm_state(vm_state_t *vm);
    void cleanup_vm_state(vm_state_t *vm);
    void load_program(vm_state_t *vm);

    void fun_add(vm_state_t *vm, instruction_t *inst);
    void fun_sub(vm_state_t *vm, instruction_t *inst);
    void fun_mul(vm_state_t *vm, instruction_t *inst);
    void fun_div(vm_state_t *vm, instruction_t *inst);
    void fun_reserve_area(vm_state_t *vm, instruction_t *inst);
    void fun_free_area(vm_state_t *vm, instruction_t *inst);
    void fun_mv_fetch_blcks(vm_state_t *vm, instruction_t *inst);
    void fun_mv_blcks_fetch(vm_state_t *vm, instruction_t *inst);
    void fun_mv_constant_fetch(vm_state_t *vm, instruction_t *inst);

#endif /* FLUXIFY_H_ */
