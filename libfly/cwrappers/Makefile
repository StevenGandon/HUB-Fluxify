##
## EPITECH PROJECT, 2024
## Hub project FLUXIFY
## File description:
## Makefile of standard lib
##

NAME = libstdfly

all: $(NAME)

$(NAME):
	make -C libsfml/
	make -C libstd/
	@mkdir -p /usr/lib64/
	@echo -e "\e[1;35m[FLY] COPY libfly.so in /usr/lib64/ ...\e[0m"
	cp libflystd.so /usr/lib64/
	cp libflysfml.so /usr/lib64/
	@echo -e "\e[1;32m[SUCCESS]\e[0m"

clean:
	make -C libsfml/ clean
	make -C libstd/ clean

fclean:
	make -C libsfml/ fclean
	make -C libstd/ fclean

re: fclean all

.PHONY: all clean fclean re
