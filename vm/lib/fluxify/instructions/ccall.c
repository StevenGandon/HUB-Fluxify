/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** ccall
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>
#include <string.h>

void fun_ccall(vm_state_t *vm, instruction_t *inst)
{
    (void)inst;
    size_t block_address_start = (size_t)vm->fetch_src;
    size_t size = (size_t)vm->fetch_dest;
    unsigned int fetch = 0;
    void *function = 0;
    long int *arguments = malloc(sizeof(long int) * (size - 1));
    long int ret_val = 0;

    memset(arguments, 0, sizeof(long int) * (size - 1));

    for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
        fetch |= (unsigned int)vm->fetch_char(vm, vm->program_counter + i);
    }

    for (size_t i = 0; vm->blocks[i] != NULL; i++) {
        if (vm->blocks[i]->address == block_address_start) {
            function = (void *)vm->blocks[i]->value;
        }
    }

    for (size_t i = 1; i < size; i++) {
        for (size_t j = 0; vm->blocks[j] != NULL; j++) {
            if (vm->blocks[j]->address == block_address_start + i) {
                arguments[i - 1] = vm->blocks[j]->value;
            }
        }
    }

    if (size == 1)
        ret_val = ((long int (*)())function)();
    if (size == 2)
        ret_val = ((long int (*)(long int arg))function)(arguments[0]);
    if (size == 3)
        ret_val = ((long int (*)(long int arg, long int arg1))function)(arguments[0], arguments[1]);
    if (size == 4)
        ret_val = ((long int (*)(long int arg, long int arg1, long int arg2))function)(arguments[0], arguments[1], arguments[2]);
    if (size == 5)
        ret_val = ((long int (*)(long int arg, long int arg1, long int arg2, long int arg3))function)(arguments[0], arguments[1], arguments[2], arguments[3]);
    if (size == 6)
        ret_val = ((long int (*)(long int arg, long int arg1, long int arg2, long int arg3, long int arg4))function)(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4]);
    if (size == 7)
        ret_val = ((long int (*)(long int arg, long int arg1, long int arg2, long int arg3, long int arg4, long int arg5))function)(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5]);
    if (size == 8)
        ret_val = ((long int (*)(long int arg, long int arg1, long int arg2, long int arg3, long int arg4, long int arg5, long int arg6))function)(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5], arguments[6]);
    if (size == 9)
        ret_val = ((long int (*)(long int arg, long int arg1, long int arg2, long int arg3, long int arg4, long int arg5, long int arg6, long int arg7))function)(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4], arguments[5], arguments[6], arguments[7]);


    if (fetch == 0) {
        vm->fetch_src = ret_val;
    } else {
        vm->fetch_dest = ret_val;
    }

    vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
    free(arguments);
}
