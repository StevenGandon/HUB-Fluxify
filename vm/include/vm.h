/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** vm.h
*/

#ifndef VM_H
    #define VM_H

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <stdint.h>

enum Instruction {
    NOOP = 0x00,
    ADD = 0x01,
    SUB = 0x02
};

typedef struct {
    uint8_t code;
    uint8_t arg_size;
    uint64_t args[2];
} instruction_t;

typedef struct {
    size_t size;
    instruction_t *instructions;
} program_table_t;

typedef struct {
    size_t size;
    char **label_names;
    uint64_t *ref_dests;
} label_table_t;

typedef struct {
    uint8_t value_type;
    uint32_t value_size;
    void *value;
} constant_t;

typedef struct {
    size_t size;
    constant_t *constants;
} constants_table_t;

int read_program(FILE *file, program_table_t *program);
int read_tables(FILE *file, label_table_t *labels,
    constants_table_t *constants);
int read_flo_file(const char *filename, program_table_t *program,
    label_table_t *labels, constants_table_t *constants);

#endif
