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
	@mkdir -p /usr/lib64/
	@echo -e "\e[1;35m[FLY] COPY libfly.so in /usr/lib64/ ...\e[0m"
	sudo cp libfly.so /usr/lib64/
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
