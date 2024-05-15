#include "fluxify.h"
#include "stack.h"

unsigned char hasattr(FlObject *object, const char *name)
{
    stack_t *stack = init_stack();

    push(stack, object->object_type);

    while (stack->next) {
        // if (((_type_object_t *)get_back(stack)->name)->members == name) {
        //     destroy_stack(stack);
        //     return (1);
        // }
        pop(stack);
    }
    destroy_stack(stack);
    return (0);
}
