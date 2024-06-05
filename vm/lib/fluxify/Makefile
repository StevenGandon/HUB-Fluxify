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
		./instructions/not_equal.c \
		./instructions/and_and.c \
		./instructions/or_or.c \
		./instructions/mv_fetch_pc.c \
		./instructions/mv_pc_fetch.c \
		./instructions/get_label_address.c \
		./instructions/swap_fetch.c \
		./instructions/move_fetch_into_blocks.c \
		./instructions/move_fetch_blocks_into_fetch.c \
		./instructions/reset_fetch.c \
		./instructions/create_var.c \
		./instructions/assign_var.c \
		./instructions/move_pc_cmp.c \
		./instructions/variable_fetch.c \
		./instructions/move_pc_cmpn.c	\
		./instructions/superior.c 		\
		./instructions/inferior.c		\
		./instructions/superior_equal.c	\
		./instructions/inferior_equal.c	\
		./instructions/dl_open_fetch.c \
		./instructions/dlsym_fetch.c	\
		./instructions/ccall.c

OBJ	=	$(SRC:.c=.o)
NAME	=	libfluxify
CFLAGS	=	-g -O2 -I ../../include -Wall -Wextra -Werror	\
			-Wshadow	-Wno-pointer-to-int-cast \
			-Waggregate-return -Wdouble-promotion	\
			-Walloc-zero -Wcast-qual -Wconversion -Winit-self -Wno-sign-conversion -Wno-int-to-pointer-cast	\
			-Wlogical-op -L ../lib -lfloff -ldl

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
