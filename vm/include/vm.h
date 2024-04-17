/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** vm.h
*/

#ifndef VM_H
#define VM_H

enum Instruction {
    NOOP = 0x00,
    ADD = 0x01,
    SUB = 0x02
};

typedef struct instruction_s {
    uint8_t code;
    uint8_t arg_size;
    uint64_t args[2];
} instruction_t;

typedef struct program_table_s {
    size_t size;
    instruction_t *instructions;
} program_table_t;

typedef struct label_table_s {
    size_t size;
    char **label_names;
    uint64_t *ref_dests;
} label_table_t;

typedef struct constants_table_s {
    size_t size;
    Constant *constants;
} constants_table_t;

#endif
