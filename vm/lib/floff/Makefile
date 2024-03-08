##
## EPITECH PROJECT, 2022
## Hub project
## File description:
## Makefile
##

SRC	=	./floff64.c	\
		./floff32.c
OBJ	=	$(SRC:.c=.o)
NAME	=	libfloff
CFLAGS	=	-O2 -I ./ -Wall -Wextra -Werror	\
			-Wshadow -pedantic	\
			-Waggregate-return -Wdouble-promotion	\
			-Walloc-zero -Wcast-qual -Wconversion -Winit-self	\
			-Wlogical-op

all: $(NAME)
	cp floff.h ../../include

$(NAME): $(OBJ)
	ar rc $(NAME).a $(OBJ)
	cp $(NAME).a ..

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME).a

re: fclean all
