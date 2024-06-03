##
## EPITECH PROJECT, 2024
## Hub project
## File description:
## Makefile
##

OBJ	=	./src/__pycache__

NAME	=	flo_to_exe

all: setup $(NAME)

$(NAME):
	chmod +x $(NAME)

run:
	python3 $(NAME)

setup:
	pip install -r ./requirements.txt

clean:
	rm -rf $(OBJ)

fclean: clean

re: fclean

build:
	echo "Not implemented"

.PHONY: clean fclean re setup $(NAME)
