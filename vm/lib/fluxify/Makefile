##
## EPITECH PROJECT, 2022
## Hub project
## File description:
## Makefile
##

SRC	=	./main.c \
		./vm.c
OBJ	=	$(SRC:.c=.o)
NAME	=	libfluxify
CFLAGS	=	-O2 -I ./ -Wall -Wextra -Werror	\
			-Wshadow -pedantic	\
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
