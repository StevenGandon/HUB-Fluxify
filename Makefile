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

tests_run:
	chmod +x ./tests/unit_tests
	cd tests && ./unit_tests

re:
	@make -C vm re
	@make -C compiler re
