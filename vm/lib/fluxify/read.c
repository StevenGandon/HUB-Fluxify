/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** read.c
*/

#include "vm.h"

int read_program(FILE *file, program_table_t *program)
{
    if (fread(&program->size, sizeof(size_t), 1, file) != 1)
        return 84;
    program->instructions = malloc(program->size * sizeof(instruction_t));
    if (!program->instructions)
        return 84;
    if (fread(program->instructions, sizeof(instruction_t),
        program->size, file) != program->size) {
        free(program->instructions);
        return 84;
    }
    return 0;
}

int read_tables(FILE *file, label_table_t *labels,
    constants_table_t *constants)
{
    size_t name_size;

    if (fread(&labels->size, sizeof(size_t), 1, file) != 1)
        return 84;
    labels->label_names = malloc(labels->size * sizeof(char *));
    labels->ref_dests = malloc(labels->size * sizeof(uint64_t));
    if (!labels->label_names || !labels->ref_dests) {
        return 84;
    }
    for (size_t i = 0; i < labels->size; ++i) {
        if (fread(&name_size, sizeof(size_t), 1, file) != 1)
            return 84;
        labels->label_names[i] = malloc(name_size * sizeof(char));
        if (!labels->label_names[i])
            return 84;
        if (fread(labels->label_names[i], sizeof(char),
            name_size, file) != name_size)
            return 84;
        if (fread(&labels->ref_dests[i], sizeof(uint64_t), 1, file) != 1)
            return 84;
    }
    if (fread(&constants->size, sizeof(size_t), 1, file) != 1)
        return 84;
    constants->constants = malloc(constants->size * sizeof(constant_t));
    if (!constants->constants)
        return 84;
    for (size_t i = 0; i < constants->size; ++i) {
        if (fread(&constants->constants[i].value_type,
            sizeof(uint8_t), 1, file) != 1) {
            return 84;
        }
        if (fread(&constants->constants[i].value_size,
            sizeof(uint32_t), 1, file) != 1)
            return 84;
        constants->constants[i].value =
            malloc(constants->constants[i].value_size);
        if (!constants->constants[i].value)
            return 84;
        if (fread(constants->constants[i].value, sizeof(char),
            constants->constants[i].value_size, file)
            != constants->constants[i].value_size) {
            return 84;
        }
    }
    return 0;
}

int read_flo_file(const char *filename, program_table_t *program,
    label_table_t *labels, constants_table_t *constants)
{
    FILE *file = fopen(filename, "rb");
    int error = 0;

    if (!file)
        return 84;
    if (read_program(file, program) != 0) {
        error = 84;
    } else {
        if (read_tables(file, labels, constants) != 0) {
            error = 84;
        }
    }
    fclose(file);
    return error;
}
