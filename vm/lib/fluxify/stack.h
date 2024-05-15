/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** fluxify.h
*/

#ifndef STACK_H_
    #define STACK_H_

    struct stack_s {
        void *name;
        struct stack_s *next;
    };

    typedef struct stack_s stack_t;

    stack_t *init_stack(void);
    void push(stack_t *stack, void *name);
    void *pop(stack_t *stack);
    stack_t *get_back(stack_t *stack);
    void destroy_stack(stack_t *stack);

#endif /* STACK_H_ */