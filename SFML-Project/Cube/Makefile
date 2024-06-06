##
## EPITECH PROJECT, 2024
## Hub project FLUXIFY
## File description:
## Makefile for flywrappers
##

NAME = result

SRC = cube.fly

OBJ = $(SRC:.fly=.flo)
FLYFLAGS += -Wall -Eall -c

%.flo: %.fly
	@echo "\e[1;35m[FLY] Building $@...\e[0m"
	../../compiler/fcc $< ${FLYFLAGS} -o ${NAME}
	@echo "\e[1;32m[SUCCESS] $@ built\e[0m"

all: $(NAME)

$(NAME): $(OBJ)

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
