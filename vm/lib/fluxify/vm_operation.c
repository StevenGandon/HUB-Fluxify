/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** vm_opration
*/

#include "fluxify.h"
#include "floff.h"
#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

unsigned char fetch_char(vm_state_t *vm, size_t offset)
{
    if (offset < vm->program_size)
        return (*(vm->program + offset));
    else
        return (0);
}

void initialize_vm_state(vm_state_t *vm)//, size_t memory_size)
{
    vm->fetch_char = &fetch_char;
    vm->fetch_src = 0;
    vm->fetch_dest = 0;
    vm->blocks = NULL;
    vm->memory_size = 0;
    vm->program_counter = 0;
    vm->is_running = 1;
    vm->var_map = NULL;
}

void cleanup_vm_state(vm_state_t *vm)
{
    free(vm->program);
    free(vm->constants);
    if (vm->blocks) {
        for (size_t i = 0; i < vm->memory_size; ++i) {
            if (vm->blocks[i] != NULL && (i == 0 || vm->blocks[i] != vm->blocks[i - 1])) {
                printf("block not free: %ld\n", vm->blocks[i]->address);
                free(vm->blocks[i]);
            }
        }
        free(vm->blocks);
    }
}

// todo : rework this
char execute_program(vm_state_t *vm)//, size_t size)
{
    char status = 0;

    initialize_vm_state(vm); //, size);
    status = run_vm(vm);
    cleanup_vm_state(vm);
    return (status);
}

void load_constants32(floff32_t *flo_data, vm_state_t *vm)
{
    unsigned int constant_number = 0;

    for (unsigned int i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_CONSTANT) {
            for (unsigned int j = 0; j < flo_data->body[i]->table_size; ++j) {
                unsigned int size;

                j += 1;
                *((unsigned char *)(&size) + 3) = flo_data->body[i]->table_bytes[j];
                *((unsigned char *)(&size) + 2) = flo_data->body[i]->table_bytes[j + 1];
                *((unsigned char *)(&size) + 1) = flo_data->body[i]->table_bytes[j + 2];
                *((unsigned char *)(&size)) = flo_data->body[i]->table_bytes[j + 3];

                j += 4 + size - 1;

                constant_number += 1;
            }
        }
    }
    vm->constant_size = constant_number;
    if (constant_number == 0) {
        vm->constants = NULL;
        return;
    } else
        vm->constants = malloc(sizeof(int *) * constant_number);

    unsigned int number = 0;

    for (unsigned int i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_CONSTANT) {
            for (unsigned int j = 0; j < flo_data->body[i]->table_size; ++j) {
                unsigned int size;
                unsigned char type = flo_data->body[i]->table_bytes[j];

                j += 1;
                *((unsigned char *)(&size) + 3) = flo_data->body[i]->table_bytes[j];
                *((unsigned char *)(&size) + 2) = flo_data->body[i]->table_bytes[j + 1];
                *((unsigned char *)(&size) + 1) = flo_data->body[i]->table_bytes[j + 2];
                *((unsigned char *)(&size)) = flo_data->body[i]->table_bytes[j + 3];

                j += 4;

                if (type == FLO_TYPE_INT) {
                    *(vm->constants + number) = 0;
                    *((unsigned char *)(vm->constants + number) + 3) = flo_data->body[i]->table_bytes[j];
                    *((unsigned char *)(vm->constants + number) + 2) = flo_data->body[i]->table_bytes[j + 1];
                    *((unsigned char *)(vm->constants + number) + 1) = flo_data->body[i]->table_bytes[j + 2];
                    *((unsigned char *)(vm->constants + number)) = flo_data->body[i]->table_bytes[j + 3];
                }
                if (type == FLO_TYPE_STRING)
                    vm->constants[number] = (long int)memcpy(memset(malloc(sizeof(char) * (size + 1)), 0, sizeof(char) * (size + 1)), (char *)(flo_data->body[i]->table_bytes + j), size);
                j += size - 1;
                number += 1;
            }
        }
    }
}

void load_constants64(floff64_t *flo_data, vm_state_t *vm)
{
    size_t constant_number = 0;

    for (size_t i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_CONSTANT) {
            for (size_t j = 0; j < flo_data->body[i]->table_size; ++j) {
                unsigned long int size;

                j += 1;
                *((unsigned char *)(&size) + 7) = flo_data->body[i]->table_bytes[j];
                *((unsigned char *)(&size) + 6) = flo_data->body[i]->table_bytes[j + 1];
                *((unsigned char *)(&size) + 5) = flo_data->body[i]->table_bytes[j + 2];
                *((unsigned char *)(&size) + 4) = flo_data->body[i]->table_bytes[j + 3];
                *((unsigned char *)(&size) + 3) = flo_data->body[i]->table_bytes[j + 4];
                *((unsigned char *)(&size) + 2) = flo_data->body[i]->table_bytes[j + 5];
                *((unsigned char *)(&size) + 1) = flo_data->body[i]->table_bytes[j + 6];
                *((unsigned char *)(&size)) = flo_data->body[i]->table_bytes[j + 7];

                j += 8 + size - 1;

                constant_number += 1;
            }
        }
    }
    vm->constant_size = constant_number;
    if (constant_number == 0) {
        vm->constants = NULL;
        return;
    } else
        vm->constants = malloc(sizeof(long int *) * constant_number);

    unsigned long int number = 0;

    for (size_t i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_CONSTANT) {
            for (size_t j = 0; j < flo_data->body[i]->table_size; ++j) {
                unsigned long int size;
                unsigned char type = flo_data->body[i]->table_bytes[j];

                j += 1;
                *((unsigned char *)(&size) + 7) = flo_data->body[i]->table_bytes[j];
                *((unsigned char *)(&size) + 6) = flo_data->body[i]->table_bytes[j + 1];
                *((unsigned char *)(&size) + 5) = flo_data->body[i]->table_bytes[j + 2];
                *((unsigned char *)(&size) + 4) = flo_data->body[i]->table_bytes[j + 3];
                *((unsigned char *)(&size) + 3) = flo_data->body[i]->table_bytes[j + 4];
                *((unsigned char *)(&size) + 2) = flo_data->body[i]->table_bytes[j + 5];
                *((unsigned char *)(&size) + 1) = flo_data->body[i]->table_bytes[j + 6];
                *((unsigned char *)(&size)) = flo_data->body[i]->table_bytes[j + 7];

                j += 8;

                if (type == FLO_TYPE_INT) {
                    *((unsigned char *)(vm->constants + number) + 7) = flo_data->body[i]->table_bytes[j];
                    *((unsigned char *)(vm->constants + number) + 6) = flo_data->body[i]->table_bytes[j + 1];
                    *((unsigned char *)(vm->constants + number) + 5) = flo_data->body[i]->table_bytes[j + 2];
                    *((unsigned char *)(vm->constants + number) + 4) = flo_data->body[i]->table_bytes[j + 3];
                    *((unsigned char *)(vm->constants + number) + 3) = flo_data->body[i]->table_bytes[j + 4];
                    *((unsigned char *)(vm->constants + number) + 2) = flo_data->body[i]->table_bytes[j + 5];
                    *((unsigned char *)(vm->constants + number) + 1) = flo_data->body[i]->table_bytes[j + 6];
                    *((unsigned char *)(vm->constants + number)) = flo_data->body[i]->table_bytes[j + 7];
                }
                if (type == FLO_TYPE_STRING)
                    vm->constants[number] = (long int)memcpy(memset(malloc(sizeof(char) * (size + 1)), 0, sizeof(char) * (size + 1)), (char *)(flo_data->body[i]->table_bytes + j), size);
                j += size - 1;
                number += 1;
            }
        }
    }
}

void load_instructions64(floff64_t *flo_data, vm_state_t *vm)
{
    size_t program_size = 0;

    for (size_t i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_PROGRAM) {
            program_size += flo_data->body[i]->table_size;
        }
    }
    vm->program_size = program_size;
    if (program_size == 0) {
        vm->program = NULL;
        return;
    } else
        vm->program = malloc(sizeof(unsigned char) * program_size);

    size_t index = 0;

    for (size_t i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_PROGRAM) {
            memcpy(vm->program + index, flo_data->body[i]->table_bytes, flo_data->body[i]->table_size);
            index += flo_data->body[i]->table_size;
        }
    }
}

void load_instructions32(floff32_t *flo_data, vm_state_t *vm)
{
    unsigned int program_size = 0;

    for (unsigned int i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_PROGRAM) {
            program_size += flo_data->body[i]->table_size;
        }
    }
    vm->program_size = program_size;
    if (program_size == 0) {
        vm->program = NULL;
        return;
    } else
        vm->program = malloc(sizeof(unsigned char) * program_size);

    unsigned int index = 0;

    for (unsigned int i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_PROGRAM) {
            memcpy(vm->program + index, flo_data->body[i]->table_bytes, flo_data->body[i]->table_size);
            index += flo_data->body[i]->table_size;
        }
    }
}

void load_labels32(floff32_t *flo_data, vm_state_t *vm)
{
    unsigned int label_number = 0;

    for (unsigned int i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_LABEL) {
            size_t j = 0;

            while (j < flo_data->body[i]->table_size) {
                unsigned char name_length = flo_data->body[i]->table_bytes[j];
                j += 1;
                j += name_length;
                j += 4;

                label_number += 1;
            }
        }
    }
    vm->label_size = label_number;
    if (label_number == 0) {
        vm->labels = NULL;
        return;
    } else {
        vm->labels = malloc(sizeof(label_t) * label_number);
        memset(vm->labels, 0, sizeof(label_t) * label_number);
    }

    unsigned int index = 0;

    for (unsigned int i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_LABEL) {
            unsigned int offset = 0;
            while (offset < flo_data->body[i]->table_size) {
                unsigned char name_length = flo_data->body[i]->table_bytes[offset];
                vm->labels[index].name = malloc(name_length + 1);
                memcpy(vm->labels[index].name, &flo_data->body[i]->table_bytes[offset + 1], name_length);
                vm->labels[index].name[name_length] = 0;
                offset += name_length + 1;

                vm->labels[index].position = 0;

                *((unsigned char *)(&vm->labels[index].position) + 3) = flo_data->body[i]->table_bytes[offset];
                *((unsigned char *)(&vm->labels[index].position) + 2) = flo_data->body[i]->table_bytes[offset + 1];
                *((unsigned char *)(&vm->labels[index].position) + 1) = flo_data->body[i]->table_bytes[offset + 2];
                *((unsigned char *)(&vm->labels[index].position) + 0) = flo_data->body[i]->table_bytes[offset + 3];
                offset += sizeof(unsigned int);

                index++;
            }
        }
    }
}

void load_labels64(floff64_t *flo_data, vm_state_t *vm)
{
    size_t label_number = 0;

    for (size_t i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_LABEL) {
            size_t j = 0;

            while (j < flo_data->body[i]->table_size) {
                unsigned char name_length = flo_data->body[i]->table_bytes[j];
                j += 1;
                j += name_length;
                j += 8;

                label_number += 1;
            }
        }
    }
    vm->label_size = label_number;
    if (label_number == 0) {
        vm->labels = NULL;
        return;
    } else {
        vm->labels = malloc(sizeof(label_t) * label_number);
        memset(vm->labels, 0, sizeof(label_t) * label_number);
    }

    size_t index = 0;

    for (size_t i = 0; i < flo_data->table_number; ++i) {
        if (flo_data->body[i]->table_type == TABLE_LABEL) {
            size_t offset = 0;
            while (offset < flo_data->body[i]->table_size) {
                unsigned char name_length = flo_data->body[i]->table_bytes[offset];
                vm->labels[index].name = malloc(name_length + 1);
                memcpy(vm->labels[index].name, &flo_data->body[i]->table_bytes[offset + 1], name_length);
                vm->labels[index].name[name_length] = 0;
                offset += name_length + 1;

                *((unsigned char *)(&vm->labels[index].position) + 7) = flo_data->body[i]->table_bytes[offset];
                *((unsigned char *)(&vm->labels[index].position) + 6) = flo_data->body[i]->table_bytes[offset + 1];
                *((unsigned char *)(&vm->labels[index].position) + 5) = flo_data->body[i]->table_bytes[offset + 2];
                *((unsigned char *)(&vm->labels[index].position) + 4) = flo_data->body[i]->table_bytes[offset + 3];
                *((unsigned char *)(&vm->labels[index].position) + 3) = flo_data->body[i]->table_bytes[offset + 4];
                *((unsigned char *)(&vm->labels[index].position) + 2) = flo_data->body[i]->table_bytes[offset + 5];
                *((unsigned char *)(&vm->labels[index].position) + 1) = flo_data->body[i]->table_bytes[offset + 6];
                *((unsigned char *)(&vm->labels[index].position)) = flo_data->body[i]->table_bytes[offset + 7];
                offset += sizeof(uint64_t);

                index++;
            }
        }
    }
}

void push_call_stack(vm_state_t *vm, uint64_t return_address)
{
    if (vm->call_stack_size >= vm->call_stack_capacity) {
        vm->call_stack_capacity *= 2;
        vm->call_stack = realloc(vm->call_stack, vm->call_stack_capacity * sizeof(uint64_t));
    }
    vm->call_stack[vm->call_stack_size++] = return_address;
}

uint64_t pop_call_stack(vm_state_t *vm)
{
    if (vm->call_stack_size == 0) {
        exit(EXIT_FAILURE);
    }
    return vm->call_stack[--vm->call_stack_size];
}

char load_program(vm_state_t *vm)
{
    void *result = auto_floff(vm->filename);

    if (result == NULL) {
        fprintf(stderr, "Invalid .flo file: %s\n", vm->filename);
        return (1);
    }

    vm->arch = ((floff64_t *)result)->architecture;

    if (vm->arch == ARCH_X86_64) {
        floff64_t *flo_data = (floff64_t *)result;

        load_constants64(flo_data, vm);
        load_instructions64(flo_data, vm);
        load_labels64(flo_data, vm);
        printf("Loaded 64-bit .flo file successfully.\n");
        return execute_program(vm);
    } else if (vm->arch == ARCH_X64_32) {
        floff32_t *flo_data = (floff32_t *)result;

        load_constants32(flo_data, vm);
        load_instructions32(flo_data, vm);
        load_labels32(flo_data, vm);
        printf("Loaded 32-bit .flo file successfully.\n");
        return execute_program(vm);
    }
    return (1);
}
