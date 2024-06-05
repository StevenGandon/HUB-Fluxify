##
## EPITECH PROJECT, 2024
## Hub project FLUXIFY
## File description:
## Makefile of standard lib
##

NAME = libstdfly

all: $(NAME)

$(NAME):
	make -C cwrappers/
	make -C flywrappers/
	@echo -e "\e[1;32m[SUCCESS]\e[0m"

clean:
	make -C cwrappers/ clean
	make -C flywrappers/ clean

fclean:
	make -C cwrappers/ fclean
	make -C flywrappers/ fclean

# tests_run:
# 	make -C cwraappers/ tests_run

re: fclean all

.PHONY: all clean fclean re
