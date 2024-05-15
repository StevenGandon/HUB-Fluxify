#include "stack.h"

#include <stdlib.h>

stack_t *init_stack(void)
{
    stack_t *stack = malloc(sizeof(stack_t));

    if (!stack)
        return NULL;
    stack->name = NULL;
    stack->next = NULL;
    return stack;
}

void push(stack_t *stack, void *name)
{
    stack_t *temp = stack;
    stack_t *new = NULL;

    if (stack->name == NULL) {
        stack->name = name;
        return;
    }
    new = malloc(sizeof(stack_t));
    if (!new)
        return;
    new->name = name;
    new->next = NULL;
    while (temp->next != NULL)
        temp = temp->next;
    temp->next = new;
}

void *pop(stack_t *stack)
{
    stack_t *temp = stack;
    char *name = NULL;

    if (temp == NULL || temp->name == NULL)
        return NULL;
    while (temp->next->next != NULL)
        temp = temp->next;
    name = temp->next->name;
    free(temp->next);
    temp->next = NULL;
    return name;
}

stack_t *get_back(stack_t *stack)
{
    stack_t *temp = stack;
    stack_t *next = NULL;

    while (temp->next != NULL) {
        temp = temp->next;
    }
    return (temp);
}

void destroy_stack(stack_t *stack)
{
    stack_t *temp = stack;
    stack_t *next = NULL;

    while (temp != NULL) {
        next = temp->next;
        free(temp);
        temp = next;
    }
}
