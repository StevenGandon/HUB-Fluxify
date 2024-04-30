/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** read.c
*/

#include "fluxify.h"
#include <stdio.h>
#include <string.h>

program_t *load_program(const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (!file) {
        perror("Failed to open file");
        return NULL;
    }

    uint32_t magic;
    uint16_t format_version, architecture;

    if (fread(&magic, sizeof(uint32_t), 1, file) != 1 ||
        fread(&format_version, sizeof(uint16_t), 1, file) != 1 ||
        fread(&architecture, sizeof(uint16_t), 1, file) != 1) {
        perror("Failed to read header components");
        fclose(file);
        return NULL;
    }
    fseek(file, 1, SEEK_CUR);
    fseek(file, 256, SEEK_CUR);
    fseek(file, 40, SEEK_CUR);

    uint64_t table_number, start_label_address;

    if (architecture == 0x01) {
        if (fread(&table_number, sizeof(uint64_t), 1, file) != 1 ||
            fread(&start_label_address, sizeof(uint64_t), 1, file) != 1) {
            fclose(file);
            return NULL;
        }
    } else if (architecture == 0x02) {
        uint32_t table_number_32, start_label_address_32;
        if (fread(&table_number_32, sizeof(uint32_t), 1, file) != 1 ||
            fread(&start_label_address_32, sizeof(uint32_t), 1, file) != 1) {
            fclose(file);
            return NULL;
        }
        table_number = table_number_32;
        start_label_address = start_label_address_32;
    } else {
        fprintf(stderr, "Unsupported architecture code\n");
        fclose(file);
        return NULL;
    }

    program_t *program = calloc(1, sizeof(program_t));

    if (!program) {
        fclose(file);
        return NULL;
    }
    for (uint64_t i = 0; i < table_number; i++) {
        uint8_t table_type;
        uint64_t table_size;

        if (fread(&table_type, sizeof(uint8_t), 1, file) != 1) {
            free_program(program);
            fclose(file);
            return NULL;
        }

        if (architecture == 0x01) {
            if (fread(&table_size, sizeof(uint64_t), 1, file) != 1) {
                free_program(program);
                fclose(file);
                return NULL;
            }
        } else {
            uint32_t table_size_32;
            if (fread(&table_size_32, sizeof(uint32_t), 1, file) != 1) {
                free_program(program);
                fclose(file);
                return NULL;
            }
            table_size = table_size_32;
        }
        switch (table_type) {
            case 0x01:
                program->labels = realloc(program->labels, (program->num_labels + table_size) * sizeof(label_t));
                if (!program->labels || fread(program->labels + program->num_labels, sizeof(label_t), table_size, file) != table_size) {
                    free_program(program);
                    fclose(file);
                    return NULL;
                }
                program->num_labels += table_size;
                break;
            case 0x02:
                program->instructions = realloc(program->instructions, (program->num_instructions + table_size) * sizeof(instructions_t));
                if (!program->instructions || fread(program->instructions + program->num_instructions, sizeof(instructions_t), table_size, file) != table_size) {
                    free_program(program);
                    fclose(file);
                    return NULL;
                }
                program->num_instructions += table_size;
                break;
            case 0x03:
                program->constants = realloc(program->constants, (program->num_constants + table_size) * sizeof(constant_t));
                if (!program->constants || fread(program->constants + program->num_constants, sizeof(constant_t), table_size, file) != table_size) {
                    free_program(program);
                    fclose(file);
                    return NULL;
                }
                program->num_constants += table_size;
                break;
            default:
                fprintf(stderr, "Unknown table type encountered\n");
                break;
        }
    }
    fclose(file);
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
