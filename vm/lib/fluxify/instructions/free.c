/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** free_area
*/

#include "fluxify.h"
#include <stdlib.h>
#include <stdio.h>

void fun_free_area(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    unsigned int address = 0;
    size_t pc = vm->program_counter;

    for (unsigned int i = 0; i < 4; i++) {
        address |= (unsigned int)vm->fetch_char(vm, pc + i);
    }

    printf("%d\n", address);
    block_t *area_to_free = vm->blocks[address];
    if (area_to_free == NULL) {
        fprintf(stderr, "Memory area already freed or invalid address\n");
        vm->is_running = 0;
        return;
    }

    int count = 0;

    for (; vm->blocks[i] != NULL; count++);

    block_t **array = malloc(sizeof(block_t *) * count);

    for (int i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == address)
            continue;
        array[i] = malloc(sizeof(block_t));
        array[i] = vm->blocks[i];
        free(vm->blocks[i]);
    }

    vm->blocks = array;

    vm->program_counter += 4;
    printf("Freed area starting at address: %u\n", address);
}
