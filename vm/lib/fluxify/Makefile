##
## EPITECH PROJECT, 2022
## Hub project
## File description:
## Makefile
##

SRC	=	./hello_world.c
OBJ	=	$(SRC:.c=.o)
NAME	=	libfluxify

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
