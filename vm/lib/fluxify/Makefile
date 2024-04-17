##
## EPITECH PROJECT, 2022
## Hub project
## File description:
## Makefile
##

SRC	=	./main.c \
		./object.c \
		./garbage_collection.c \
		./read.c
OBJ	=	$(SRC:.c=.o)
NAME	=	fluxify
CFLAGS	=	-O2 -I ./ -Wall -Wextra -Werror	\
			-Wshadow -pedantic	\
			-Waggregate-return -Wdouble-promotion	\
			-Walloc-zero -Wcast-qual -Wconversion -Winit-self	\
			-Wlogical-op

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(OBJ) -o $(NAME)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all
