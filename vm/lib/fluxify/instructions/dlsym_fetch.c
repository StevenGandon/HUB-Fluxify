/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** dlsym_fetch
*/

#include "floff.h"
#include "fluxify.h"
#include <stdio.h>

#if defined(_WIN32)
    #include <libloaderapi.h>

    void fun_dlsym_fetch(vm_state_t *vm, instruction_t *inst)
    {
        (void)inst;
        void *symbol = NULL;
        size_t pc = vm->program_counter;
        unsigned int fetch = 0;

        for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
            fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
        }

        void *lib_handle = (void *)vm->fetch_src;
        char *symbol_name = (char *)vm->fetch_dest;

        if (!lib_handle) {
            fprintf(stderr, "[ERROR] Filepath of DLLopen does not exist or is not a valid file\n");
        } else {
            symbol = GetProcAddress(lib_handle, symbol_name);
        }

        if (fetch == 0) {
            vm->fetch_src = (long int)symbol;
        } else {
            vm->fetch_dest = (long int)symbol;
        }

        vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
    }
#else
    #include <dlfcn.h>

    void fun_dlsym_fetch(vm_state_t *vm, instruction_t *inst)
    {
        (void)inst;
        void *symbol = NULL;
        size_t pc = vm->program_counter;
        unsigned int fetch = 0;

        for (unsigned int i = 0; i < (vm->arch == ARCH_X86_64 ? 8 : 4); i++) {
            fetch |= (unsigned int)vm->fetch_char(vm, pc + i);
        }

        void *lib_handle = (void *)vm->fetch_src;
        char *symbol_name = (char *)vm->fetch_dest;

        if (!lib_handle) {
            fprintf(stderr, "[ERROR] Filepath of DLLopen does not exist or is not a valid file\n");
        } else {
            symbol = dlsym(lib_handle, symbol_name);
        }

        if (fetch == 0) {
            vm->fetch_src = (long int)symbol;
        } else {
            vm->fetch_dest = (long int)symbol;
        }

        vm->program_counter += vm->arch == ARCH_X86_64 ? 8 : 4;
    }
#endif
