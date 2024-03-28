from typing import Any, Callable, Iterable
from ..Graphic.Color import hex_to_rgb, code_fore_from_rgb, code_reset, code_bold
from ..System.Output import SilentExec

_STATUS: dict = {
    "passed": 0,
    "failed": 1,
    "crashed": 2
}

class Test(object):
    def __init__(self, name: str = "test",
                description: str = '', callback: Callable = print, args: tuple = ()) -> None:
        self.name: str = name
        self.description: str = description
        self.callback: Callable = callback
        self.args: tuple = args

        self.status: str = None

        if (not isinstance(name, str) or not isinstance(description, str) or
            not callable(self.callback) or not isinstance(args, Iterable)):
            raise (TypeError())

    def __repr__(self) -> str:
        name: str = self.name.replace("'", "\\'")
        description: str = self.description.replace("'", "\\'")

        if (self.status is None):
            return (f"Test('{name}', '{description}', {self.callback.__name__}, {str(self.args)})")
        return (f"{name}: {self.status}")
    
    def run(self) -> None:
        result: int = 0

        try:
            result: int = self.callback(*self.args)

            if (result):
                self.status: str = "passed"
            else:
                self.status: str = "failed"
        except Exception:
            self.status: str = "crashed"

class Sample(object):
    def __init__(self) -> None:
        self.tests: list = list()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        name: str = kwds["name"] if "name" in kwds else "test"
        description: str = kwds["description"] if "description" in kwds else ""
        args: str = kwds["args"] if "args" in kwds else ()

        def decorator_function(__original: Callable):
            self.tests.append(Test(name, description, __original, args))
        return decorator_function

    def run_debug(self, colored = True, palette: tuple = ("#43c928", "#c98928", "#c93328"), tests_outputs: bool = False) -> None:
        if (not isinstance(palette, Iterable)):
            raise (TypeError())
        if (len(palette) != 3):
            raise (ValueError())

        eol_color: str = code_reset()
        bold_color: str = code_bold()
        transformed_palette: tuple = tuple(map(lambda x: code_fore_from_rgb(*hex_to_rgb(x)), palette))

        for item in self.tests:
            print(f"Running {item.name}...\b\b\b", end = '', flush = True)

            if (tests_outputs):
                item.run()
            else:
                with SilentExec():
                    item.run()

            print(f': [{item.status.upper()}]' if (not colored) else f': [{transformed_palette[_STATUS[item.status]]}{item.status.upper()}{eol_color}]')

        passed: int = len(tuple('' for item in self.tests if item.status == "passed"))
        failed: int = len(tuple('' for item in self.tests if item.status == "failed"))
        crashed: int = len(tuple('' for item in self.tests if item.status == "crashed"))
        total: int = len(self.tests)

        print(f'Result: {passed}/{total} ({round((passed * 100) / (total if total != 0 else 1), 2)}%) [PASSED {passed} | FAILED {failed} | CRASH {crashed}]' if (not colored) else f'Result: {bold_color}{passed}{eol_color}/{bold_color}{total}{eol_color} ({bold_color}{round((passed * 100) / (total if total != 0 else 1), 2)}{eol_color}%) [{transformed_palette[0]}PASSED{eol_color} {bold_color}{passed}{eol_color} | {transformed_palette[1]}FAILED{eol_color} {bold_color}{failed}{eol_color} | {transformed_palette[2]}CRASH{eol_color} {bold_color}{crashed}{eol_color}]')

    def run(self, tests_outputs: bool = False) -> None:
        for item in self.tests:
            if (tests_outputs):
                item.run()
            else:
                with SilentExec():
                    item.run()
