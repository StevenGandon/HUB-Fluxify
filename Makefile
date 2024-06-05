##
## EPITECH PROJECT, 2024
## Hub project
## File description:
## Makefile
##

all: vm compiler flo_to_exe libfly

vm:
	@make -C vm

compiler:
	@make -C compiler

flo_to_exe:
	@make -C flo_to_exe

libfly:
	@make -C libfly

clean:
	@make -C vm clean
	@make -C compiler clean
	@make -C flo_to_exe clean
	@make -C libfly clean

fclean:
	@make -C vm fclean
	@make -C compiler fclean
	@make -C flo_to_exe fclean
	@make -C libfly fclean

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
	@make -C libfly re

.PHONY: all vm compiler flo_to_exe