from CNLib_Min.Testing import Sample
from requests import post, get, options, delete, Response, put
from subprocess import Popen, PIPE
from sys import exit

import builtins

builtins.exit = exit

tests: Sample = Sample()

def exec_shell(command: str) -> tuple:
    result = Popen([command], stdout=PIPE, stderr=PIPE, shell=True)
    output = result.communicate(timeout=10)[0].decode()
    status = result.wait(10)

    if (result.stdout and not result.stdout.closed):
        result.stdout.close()
    if (result.stderr and not result.stderr.closed):
        result.stderr.close()
    if (result.stdin and not result.stdin.closed):
        result.stdin.close()

    return (status, output)