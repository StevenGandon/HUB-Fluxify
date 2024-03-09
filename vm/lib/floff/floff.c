/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** floff.c
*/

#include "floff.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

static void *
handle_arch(arch, path)
    unsigned short arch;
    const char *path;
{
    void *ret = NULL;

    if (arch == ARCH_X86_64) {
        ret = (void *)create_floff64();
        if (read_floff64((floff64_t *)ret, path) == -1) {
            (void)destroy_floff64(ret);
            ret = NULL;
        }
    }
    if (arch == ARCH_X64_32) {
        ret = (void *)create_floff32();
        if (read_floff32((floff32_t *)ret, path) == -1) {
            (void)destroy_floff32(ret);
            ret = NULL;
        }
    }
    return (ret);
}

void *
auto_floff(file_path)
    const char *file_path;
{
    int fd = open(file_path, O_RDONLY);
    unsigned short temp;

    if (fd < 0)
        return (NULL);
    if (0 > lseek(fd, 6, SEEK_SET)) {
        (void)close(fd);
        return (NULL);
    }
    if (0 > read(fd, &temp, 2)) {
        (void)close(fd);
        return (NULL);
    }
    temp = ((temp >> 8) & 0xFF) | ((temp << 8) & 0xFF00);
    (void)close(fd);
    return (handle_arch(temp, file_path));
}
