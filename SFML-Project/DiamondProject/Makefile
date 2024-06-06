##
## EPITECH PROJECT, 2024
## Hub project FLUXIFY
## File description:
## Makefile for flywrappers
##

NAME = 	result

SRC = 	diamond.fly		\
		move_sprite.fly	\
		mainFile.fly	\

OBJ = $(SRC:.fly=.flo)
FLYFLAGS += -Wall -Eall -sfml

%.flo: %.fly
	@echo "\e[1;35m[FLY] Building $@...\e[0m"
	../../compiler/fcc {OBJ} ${FLYFLAGS} -o ${NAME}
	@echo "\e[1;32m[SUCCESS] $@ built\e[0m"

all: $(NAME)

$(NAME): $(OBJ)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
