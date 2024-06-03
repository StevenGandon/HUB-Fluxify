##
## EPITECH PROJECT, 2024
## Hub project
## File description:
## Makefile
##

all: vm compiler flo_to_exe

vm:
	@make -C vm

compiler:
	@make -C compiler

flo_to_exe:
	@make -C flo_to_exe

clean:
	@make -C vm clean
	@make -C compiler clean
	@make -C flo_to_exe clean

fclean:
	@make -C vm fclean
	@make -C compiler fclean

tests_run:
	chmod +x ./tests/unit_tests
	cd tests && ./unit_tests

install-docker-image:
	docker build --no-cache --tag fluxify .

run-docker:
	docker run -it fluxify

re:
	@make -C vm re
	@make -C compiler re
	@make -C flo_to_exe re

.PHONY: all vm compiler flo_to_exe