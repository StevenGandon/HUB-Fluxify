##
## EPITECH PROJECT, 2022
## Hub project
## File description:
## Makefile
##

SRC	=	./vm_operation.c \
		./argument_parser.c \
		./instructions_utils.c \
		./instructions/add.c \
		./instructions/sub.c \
		./instructions/mul.c \
		./instructions/div.c \
		./instructions/mod.c \
		./instructions/and.c \
		./instructions/or.c \
		./instructions/xor.c \
		./instructions/reserve_area.c \
		./instructions/free.c \
		./instructions/mv_fetch_blcks.c \
		./instructions/mv_blcks_fetch.c \
		./instructions/mv_constant_fetch.c	\
		./instructions/halt.c	\
		./instructions/noop.c \
		./instructions/equal_equal.c \
		./instructions/and_and.c \
		./instructions/or_or.c \
		./instructions/mv_fetch_pc.c \
		./instructions/mv_pc_fetch.c \
		./instructions/get_label_address.c
OBJ	=	$(SRC:.c=.o)
NAME	=	libfluxify
CFLAGS	=	-g -O2 -I ../../include -Wall -Wextra -Werror	\
			-Wshadow -pedantic	-Wno-pointer-to-int-cast \
			-Waggregate-return -Wdouble-promotion	\
			-Walloc-zero -Wcast-qual -Wconversion -Winit-self	\
			-Wlogical-op -L ./lib -lfluxify

all: $(NAME)
	cp fluxify.h ../../include

$(NAME): $(OBJ)
	ar rc $(NAME).a $(OBJ)
	cp $(NAME).a ..

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME).a

re: fclean all
