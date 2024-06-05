/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** floff64.c
*/

#include "floff.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

floff64_t *
create_floff64(void)
{
    floff64_t *object = (floff64_t *)malloc(sizeof(floff64_t));

    if (!object)
        return (NULL);
    object->body = NULL;

    object->compiler_name = strdup("fcc");
    object->compiler_name_size = 3;

    (void)memcpy(object->magic, DEFAULT_MAGIC, 4);
    (void)memcpy(object->version, "10", 2);

    (void)memset(object->program_hash, (int)'0', 40);

    object->start_label_address = 0;
    object->table_number = 0;
    object->architecture = ARCH_X86_64;
    return (object);
}

static int
file_failed(fd)
    int fd;
{
    (void)close(fd);
    return (-1);
}

static int
file_sucess(fd)
    int fd;
{
    (void)close(fd);
    return (0);
}

static void
little_endian_to_big_endian(value)
    unsigned long int *value;
{
    *value = ((*value >> 56UL) & 0xFFULL) |
             ((*value << 40UL) & 0xFF000000000000ULL) |
             ((*value << 24UL) & 0xFF0000000000ULL) |
             ((*value << 8UL)  & 0xFF00000000ULL) |
             ((*value >> 8UL)  & 0xFF000000ULL) |
             ((*value >> 24UL) & 0xFF0000ULL) |
             ((*value >> 40UL) & 0xFF00ULL) |
             ((*value << 56UL) & 0xFF00000000000000ULL);
}

static int
read_file_informations(fd, object)
    int fd;
    floff64_t *object;
{
    if (0 > read(fd, object->magic, 4))
        return (file_failed(fd));
    if (0 > read(fd, object->version, 2))
        return (file_failed(fd));
    if (0 > read(fd, &object->architecture, 2))
        return (file_failed(fd));
    object->architecture = (unsigned short)(((object->architecture >> 8) & 0xFF) |
        ((object->architecture << 8) & 0xFF00));
    if (0 > read(fd, &object->compiler_name_size, 1))
        return (file_failed(fd));
    if (object->compiler_name)
        (void)free(object->compiler_name);
    object->compiler_name = malloc(sizeof(unsigned char) * (object->compiler_name_size));
    if (!object->compiler_name || 0 > read(fd, object->compiler_name, object->compiler_name_size))
        return (file_failed(fd));
    return (0);
}

static int
read_program_informations(fd, object)
    int fd;
    floff64_t *object;
{
    if (0 > read(fd, object->program_hash, 40))
        return (file_failed(fd));
    if (0 > read(fd, &object->table_number, 8))
        return (file_failed(fd));
    (void)little_endian_to_big_endian(&object->table_number);
    if (0 > read(fd, &object->start_label_address, 8))
        return (file_failed(fd));
    (void)little_endian_to_big_endian(&object->start_label_address);
    return (0);
}

static int
read_program_datas(fd, object)
    int fd;
    floff64_t *object;
{
    if (object->table_number == 0) {
        object->body = NULL;
        return (file_sucess(fd));
    }

    object->body = (floff64_body_t **)malloc(sizeof(floff64_body_t *) * object->table_number);
    if (!object->body)
        return (file_failed(fd));

    for (size_t i = 0; i < object->table_number; ++i) {
        object->body[i] = (floff64_body_t *)malloc(sizeof(floff64_body_t));
        if (!object->body[i])
            return (file_failed(fd));
        if (0 > read(fd, &object->body[i]->table_type, 1))
            return (file_failed(fd));

        if (0 > read(fd, &object->body[i]->table_size, 8))
            return (file_failed(fd));
        (void)little_endian_to_big_endian(&object->body[i]->table_size);

        object->body[i]->table_bytes = (unsigned char *)malloc(sizeof(unsigned char) * object->body[i]->table_size);
        if (!object->body[i]->table_bytes)
            return (file_failed(fd));
        if (0 > read(fd, object->body[i]->table_bytes, object->body[i]->table_size))
            return (file_failed(fd));
    }
    return (file_sucess(fd));
}

int
read_floff64(object, file_path)
    floff64_t *object;
    const char *file_path;
{
    int fd = open(file_path, O_RDONLY);

    if (fd < 0)
        return (-1);
    if (read_file_informations(fd, object) == -1)
        return (-1);
    if (strcmp((const char *)object->magic, DEFAULT_MAGIC) != 0)
        return (-1);
    if (object->architecture != ARCH_X86_64)
        return (-1);
    if (read_program_informations(fd, object) == -1)
        return (-1);
    return (read_program_datas(fd, object));
}

int
read_floff64_fd(object, fd)
    floff64_t *object;
    int fd;
{
    if (fd < 0)
        return (-1);
    if (read_file_informations(fd, object) == -1)
        return (-1);
    if (strcmp((const char *)object->magic, DEFAULT_MAGIC) != 0)
        return (-1);
    if (object->architecture != ARCH_X86_64)
        return (-1);
    if (read_program_informations(fd, object) == -1)
        return (-1);
    return (read_program_datas(fd, object));
}

int
read_floff64_fp(object, fp)
    floff64_t *object;
    FILE *fp;
{
    int fd = fileno(fp);

    if (fd < 0)
        return (-1);
    if (read_file_informations(fd, object) == -1)
        return (-1);
    if (strcmp((const char *)object->magic, DEFAULT_MAGIC) != 0)
        return (-1);
    if (object->architecture != ARCH_X86_64)
        return (-1);
    if (read_program_informations(fd, object) == -1)
        return (-1);
    return (read_program_datas(fd, object));
}

void
destroy_floff64(object)
    floff64_t *object;
{
    size_t i = 0;

    if (!object)
        return;
    if (object->compiler_name_size != 0 && object->compiler_name)
        (void)free(object->compiler_name);
    if (object->table_number != 0 && object->body) {
        for (; i < object->table_number; ++i) {
            if (object->body[i]) {
                (void)free(object->body[i]->table_bytes);
                (void)free(object->body[i]);
            }
        }
        (void)free(object->body);
    }
    (void)free(object);
}
