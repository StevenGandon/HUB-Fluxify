##
## EPITECH PROJECT, 2024
## Hub project FLUXIFY
## File description:
## Makefile for flywrappers
##

NAME = libfly.flo

SRC = libstd/libstd.fly		\
	  libsfml/libsfml.fly 	\

OBJ = $(SRC:.fly=.flo)

%.flo: %.fly
	@echo -e "\e[1;34m[GAMES] Building $@...\e[0m"
	../../compiler/fcc $<
	@echo -e "\e[1;32m[SUCCESS] $@ built\e[0m"

CC = gcc
CFLAGS += -Wall -Wextra -Werror -fpic -g

all: $(NAME)

$(NAME): $(OBJ)

clean:
	rm -f $(OBJ)

fclean: clean

re: fclean all

.PHONY: all clean fclean re
