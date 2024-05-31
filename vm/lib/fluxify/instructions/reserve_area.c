/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** reserve_area
*/

#include "floff.h"
#include "fluxify.h"
#include <stdlib.h>
#include <stdio.h>

void fun_reserve_area(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    unsigned int address = 0;
    size_t pc = vm->program_counter;
    long int size = sizeof(long int);
    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        address |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    if (size <= 0) {
        fprintf(stderr, "Invalid size in reserve area operation\n");
        vm->is_running = 0;
        return;
    }

    if (vm->blocks == NULL) {
        vm->blocks = malloc(sizeof(block_t *) * 2);
        vm->blocks[0] = malloc(sizeof(block_t));
        vm->blocks[0]->address = address;
        vm->blocks[0]->value = 0;
        vm->blocks[1] = NULL;
        vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
        return;
    }

    int count = 0;

    for (; vm->blocks[count] != NULL; ++count);

    block_t **new_blocks = realloc(vm->blocks, (long unsigned int)(count + 2) * sizeof(block_t *));
    if (new_blocks == NULL) {
        fprintf(stderr, "Memory reallocation failed in reserve area operation\n");
        vm->is_running = 0;
        return;
    }
    vm->blocks = new_blocks;

    vm->blocks[count] = malloc(sizeof(block_t));
    if (vm->blocks[count] == NULL) {
        fprintf(stderr, "Memory allocation failed for new block\n");
        vm->is_running = 0;
        return;
    }
    vm->blocks[count]->address = address;
    vm->blocks[count]->value = 0;
    vm->blocks[count + 1] = NULL;

    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
    printf("Reserved area: %u, size: %zu\n", address, (size_t)size);
}
