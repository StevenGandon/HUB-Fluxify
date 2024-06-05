#include <stdio.h>
#include <string.h>
#include <limits.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <math.h>

int duplicate_process(void)
{
    return fork();
}

int get_pid(void)
{
    return getpid();
}

void quit(int code)
{
    exit(code);
}

char *to_str(int num)
{

    if (num == 0)
        return "0";
    static char str[12];
    snprintf(str, 13, "%d", num);
    return str;
}

void wout(char *text, char flush)
{
    if (!text)
        return;
    printf(text);

    if (flush)
        fflush(stdout);
}

void print(char *text, int stdway, char flush)
{
    if (!text)
        return;
    if (stdway == 1)
        fprintf(stdout, "%s\n", text);
    else if (stdway == 2)
        fprintf(stderr, "%s\n", text);
    else
        fprintf(stdout, "%s\n", text);

    if (flush)
        fflush(stdout);
}

void werr(char *text, char flush)
{
    fprintf(stderr, text);

    if (flush)
        fflush(stdout);
}

size_t ft_len(char *text)
{
    return strlen(text);
}
