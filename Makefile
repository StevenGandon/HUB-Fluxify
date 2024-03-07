##
## EPITECH PROJECT, 2024
## Hub project
## File description:
## Makefile
##

all: vm compiler

vm:
	@make -C vm

compiler:
	@make -C compiler

clean:
	@make -C vm clean
	@make -C compiler clean

fclean:
	@make -C vm fclean
	@make -C compiler fclean

re:
	@make -C vm re
	@make -C compiler re
