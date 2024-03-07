##
## EPITECH PROJECT, 2024
## Hub project
## File description:
## Makefile
##

OBJ	=	./src/__pycache__

NAME	=	./fcc

all: setup

$(NAME):
	chmod +x ./fcc

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

.PHONY: clean fclean re setup
