##
## EPITECH PROJECT, 2024
## Hub project FLUXIFY
## File description:
## Makefile for cwrappers
##

NAME = libfly.so

SRC = libstd/libstd.c	\
	  libsfml/libsfml.c \

OBJ = $(SRC:.c=.o)

CC = gcc
CFLAGS += -Wall -Wextra -Werror -fpic -g -lsfml-graphics -lsfml-window -lsfml-system -lsfml-audio -lsfml-network

all: $(NAME)

$(NAME): $(OBJ)
	@echo -e "\e[1;34m[GAMES] Building $(NAME)...\e[0m"
	$(CC) -shared -o $(NAME) $(OBJ) $(CFLAGS)
	mv $(NAME) ../
	@echo -e "\e[1;32m[SUCCESS] $(NAME) built\e[0m"

%.o: %.c
	@echo "Compilation of $<"
	@if gcc -c -o $@ $< $(CFLAGS); then \
		echo -e "\033[0;34m[OK]\e[0;m | $@ <- $<"; \
	else \
		echo -e "\033[0;31m[FAILED]\e[0;m | $@ <- $<"; \
		exit 1; \
	fi

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f ../$(NAME)

re: fclean all

.PHONY: all clean fclean re