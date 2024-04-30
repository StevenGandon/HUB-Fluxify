/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** read.c
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

program_t *load_program(const char *filename)
{
    FILE *file = fopen(filename, "rb");

    if (!file)
        return NULL;

    header64_t header;
    size_t result = fread(&header, sizeof(header64_t), 1, file);

    if (result != 1) {
        fclose(file);
        return NULL;
    }
    fclose(file);

    program_t *program = malloc(sizeof(header64_t));

    if (!program)
        return NULL;
    program->instructions = NULL;
    program->num_instructions = 0;
    program->labels = NULL;
    program->num_labels = 0;
    program->constants = NULL;
    program->num_constants = 0;
    program->objects = NULL;
    program->num_objects = 0;
    program->capacity_objects = 0;
    return program;
}

void run_program(program_t *program)
{
    for (size_t i = 0; i < program->num_instructions; i++) {
        instructions_t instr = program->instructions[i];

        switch (instr.code) {
            case ADD:
                printf("Executing ADD\n");
                break;
            case SUB:
                printf("Executing SUB\n");
                break;
            default:
                printf("Unknown instruction\n");
                break;
        }
    }
}

void free_program(program_t *program)
{
    if (program) {
        free(program->instructions);
        free(program->labels);
        free(program->constants);
        free(program);
    }
}

void gc_collect(program_t *program)
{
    size_t compactIndex = 0;

    if (program == NULL)
        return;
    for (size_t i = 0; i < program->num_objects; i++) {
        if (program->objects[i]->ref_cnt == 0) {
            free_object(program->objects[i]);
            program->objects[i] = NULL;
        }
    }
    for (size_t i = 0; i < program->num_objects; i++) {
        if (program->objects[i] != NULL) {
            program->objects[compactIndex++] = program->objects[i];
        }
    }
    program->num_objects = compactIndex;
}
