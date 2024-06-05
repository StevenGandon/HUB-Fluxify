#include <stdio.h>

void wout(char *text, char flush)
{
    printf(text);

    if (flush)
        fflush(stdout);
}

void werr(char *text, char flush)
{
    fprintf(text, stderr);

    if (flush)
        fflush(stdout);
}

int strlen(char *text)
{
    return strlen(text);
}
