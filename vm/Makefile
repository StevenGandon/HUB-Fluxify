##
## EPITECH PROJECT, 2024
## Hub project
## File description:
## Makefile
##

SRC	= ./main.c
OBJ	=	$(SRC:.c=.o)
NAME	=	fluxify-vm

CC	=	gcc
CFLAGS	=	-O2 -I ./include -Wall -Wextra -Werror	\
			-Wshadow -pedantic	\
			-Waggregate-return -Wdouble-promotion	\
			-Walloc-zero -Wcast-qual -Wconversion -Winit-self	\
			-Wlogical-op -L ./lib -lfluxify

all:
	@make -C ./lib/fluxify all
	@make $(NAME)

$(NAME): $(OBJ)
	$(CC) -o $(NAME) $(OBJ) $(CFLAGS)

clean:
	@make -C ./lib/fluxify clean
	rm -f $(OBJ)

fclean: clean
	@make -C ./lib/fluxify fclean
	rm -f $(NAME)

re: fclean all
	@make -C ./lib/fluxify re

.PHONY: clean fclean re
