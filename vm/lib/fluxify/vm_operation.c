/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** vm_opration
*/

#include "fluxify.h"
#include "floff.h"
#include <stdio.h>
#include <stdlib.h>

void initialize_vm_state(vm_state_t *vm, size_t memory_size)
{
    vm->blocks = calloc(memory_size, sizeof(block_t *));
    for (size_t i = 0; i < memory_size; ++i) {
        vm->blocks[i] = calloc(1, sizeof(block_t));
        vm->blocks[i]->address = i;
    }
    vm->memory_size = memory_size;
    vm->program_counter = 0;
    vm->is_running = 1;
}

void cleanup_vm_state(vm_state_t *vm)
{
    for (size_t i = 0; i < vm->memory_size; ++i) {
        free(vm->blocks[i]);
    }
    free(vm->blocks);
}

// todo : rework this
void execute_program(vm_state_t *vm, const unsigned char *bytes, size_t size)
{
    initialize_vm_state(vm, size);
    decode_and_execute_instructions(vm, bytes, size);
    cleanup_vm_state(vm);
}

void load_program(vm_state_t *vm)
{
    void *result = auto_floff(vm->filename);

    if (result == NULL) {
        fprintf(stderr, "Corrupted .flo file: %s\n", vm->filename);
        return;
    }

    if (((floff32_t *)result)->architecture != vm->arch) {
        printf("Incompatible architecture, architecture passed as argument is not the same as the file architecture.\n");
        return;
    }

    if (vm->arch == ARCH_X86_64) {
        floff64_t *flo_data = (floff64_t *)result;

        for (size_t i = 0; i < flo_data->table_number; ++i) {
            execute_program(vm, flo_data->body[i]->table_bytes, flo_data->body[i]->table_size);
        }
        printf("Loaded 64-bit .flo file successfully.\n");
    } else if (vm->arch == ARCH_X64_32) {
        floff32_t *flo_data = (floff32_t *)result;

        for (size_t i = 0; i < flo_data->table_number; ++i) {
            execute_program(vm, flo_data->body[i]->table_bytes, flo_data->body[i]->table_size);
        }
        printf("Loaded 32-bit .flo file successfully.\n");
    }
}
