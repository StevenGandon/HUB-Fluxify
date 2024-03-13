/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** vm.c
*/

#include "vm.h"
#include <stdio.h>
#include <stdlib.h>

void vm_init(vm_t *vm)
{
    vm->memory = malloc(INITIAL_MEMORY_SIZE);
    if (vm->memory == NULL) {
        exit(84);
    }
    vm->memory_size = INITIAL_MEMORY_SIZE;
    vm->register_a = 0;
    vm->program_counter = 0;
}

unsigned char vm_fetch(vm_t *vm)
{
    if (vm->program_counter >= vm->memory_size) {
        return 0;
    }
    return ((unsigned char *)vm->memory)[vm->program_counter];
}

void vm_decode(vm_t *vm, unsigned char opcode)
{
    (void)vm;
    (void)opcode;
}

void vm_execute(vm_t *vm)
{
    unsigned char opcode = vm_fetch(vm);

    vm_decode(vm, opcode);
    vm->program_counter++;
}

void vm_destroy(vm_t *vm)
{
    if (vm->memory != NULL) {
        free(vm->memory);
        vm->memory = NULL;
        vm->memory_size = 0;
    }
}
