/*
** EPITECH PROJECT, 2024
** Hub project
** File description:
** floff.h
*/

#ifndef FLOFF_H_
    #define FLOFF_H_

    #define TABLE_LABEL 0x01
    #define TABLE_PROGRAM 0x02
    #define TABLE_CONSTANT 0x03

    #define ARCH_X86_64 0x01
    #define ARCH_X64_32 0x02

    #define DEFAULT_MAGIC "\xf1\x0f\xf0\x00"


    struct floff64_body_s {
        unsigned char table_type;

        unsigned long long int table_size;
        unsigned char *table_bytes;
    };

    struct floff64_s {
        unsigned char magic[4];
        unsigned char version[2];
        unsigned short architecture;

        unsigned char compiler_name_size;
        char *compiler_name;

        unsigned char program_hash[40];

        unsigned long long int table_number;
        unsigned long long int start_label_address;

        struct floff64_body_s **body;
    };

    struct floff32_body_s {
        unsigned char table_type;

        unsigned int table_size;
        unsigned char *table_bytes;
    };

    struct floff32_s {
        unsigned char magic[4];
        unsigned char version[2];
        unsigned short architecture;

        unsigned char compiler_name_size;
        char *compiler_name;

        unsigned char program_hash[40];

        unsigned int table_number;
        unsigned int start_label_address;

        struct floff32_body_s **body;
    };

    typedef struct floff64_s floff64_t;
    typedef struct floff64_body_s floff64_body_t;

    typedef struct floff32_s floff32_t;
    typedef struct floff32_body_s floff32_body_t;

    int read_floff64(floff64_t *, const char *);
    floff64_t *create_floff64(void);

    floff32_t *create_floff32(void);

#endif /* FLOFF_H_ */
