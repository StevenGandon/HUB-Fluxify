/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** floff32.c
*/

#include "floff.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

floff32_t *
create_floff32(void)
{
    floff32_t *object = (floff32_t *)malloc(sizeof(floff32_t));

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
    object->architecture = ARCH_X64_32;
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
    unsigned int *value;
{
    *value = (*value & 0x000000ff) << 24u |
        (*value & 0x0000ff00) << 8u |
        (*value & 0x00ff0000) >> 8u |
        (*value & 0xff000000) >> 24u;
}

static int
read_file_informations(fd, object)
    int fd;
    floff32_t *object;
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
    if (object->compiler_name_size == 0) {
        object->compiler_name = NULL;
        return (0);
    }
    object->compiler_name = malloc(sizeof(unsigned char) * (object->compiler_name_size));
    if (!object->compiler_name || 0 > read(fd, object->compiler_name, object->compiler_name_size))
        return (file_failed(fd));
    return (0);
}

static int
read_program_informations(fd, object)
    int fd;
    floff32_t *object;
{
    if (0 > read(fd, object->program_hash, 40))
        return (file_failed(fd));
    if (0 > read(fd, &object->table_number, 4))
        return (file_failed(fd));
    (void)little_endian_to_big_endian(&object->table_number);
    if (0 > read(fd, &object->start_label_address, 4))
        return (file_failed(fd));
    (void)little_endian_to_big_endian(&object->start_label_address);
    return (0);
}

static int
read_program_datas(fd, object)
    int fd;
    floff32_t *object;
{
    if (object->table_number == 0) {
        object->body = NULL;
        return (file_sucess(fd));
    }
    object->body = (floff32_body_t **)malloc(sizeof(floff32_body_t *) * object->table_number);
    if (!object->body)
        return (file_failed(fd));

    for (size_t i = 0; i < object->table_number; ++i) {
        object->body[i] = (floff32_body_t *)malloc(sizeof(floff32_body_t));
        if (!object->body[i])
            return (file_failed(fd));
        if (0 > read(fd, &object->body[i]->table_type, 1))
            return (file_failed(fd));

        if (0 > read(fd, &object->body[i]->table_size, 4))
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
read_floff32(object, file_path)
    floff32_t *object;
    const char *file_path;
{
    int fd = open(file_path, O_RDONLY);

    if (fd < 0)
        return (-1);
    if (read_file_informations(fd, object) == -1)
        return (-1);
    if (strcmp((const char *)object->magic, DEFAULT_MAGIC) != 0)
        return (-1);
    if (object->architecture != ARCH_X64_32)
        return (-1);
    if (read_program_informations(fd, object) == -1)
        return (-1);
    return (read_program_datas(fd, object));
}

void
destroy_floff32(object)
    floff32_t *object;
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
