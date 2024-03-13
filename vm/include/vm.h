/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** vm.h
*/

#ifndef VM_H
#define VM_H

#include <stdlib.h>

#define INITIAL_MEMORY_SIZE = 256

enum {
    OP_LOAD = 0,
    OP_ADD,
    OP_SUB,
    OP_HALT
};

typedef struct vm_t {
    void *memory;
    size_t memory_size;
    unsigned char register_a;
    int program_counter;
} vm_t;

void vm_init(vm_t *vm);
void vm_destroy(vm_t *vm);
unsigned char vm_fetch(vm_t *vm);
void vm_decode(vm_t *vm, unsigned char opcode);
void vm_execute(vm_t *vm);
void *vm_allocate_memory(vm_t *vm, size_t size);
void vm_free_memory(vm_t *vm);

#endif
