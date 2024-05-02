import os

class Parser:
    def __init__(self) -> None:
        self.arch: str = "X86_64"
        self.options: dict = {
            "-c": False,
            "-h": False,
            "-help": False,
            "-?": False
        }
        self.entry: str = "_start"
        self.outputName: str = "a.out"
        self.errors: list = []
        self.warns: list = []
        self.files: list = []

        self.stop: bool = False
        self.whyStop: list = []

    def error(self, message: str) -> None:
        self.stop = True
        self.whyStop.append(message)

    def handle_warnings(self, arg: str) -> None:
        if (arg.startswith("-W")):
            warning: str = arg.replace("-W", "")
            if (warning == ""):
                self.error("[-] No warning specified after -W flag.\n")
            else:
                self.warns.append(arg.replace("-W", ""))

    def handle_errors(self, arg: str) -> None:
        if (arg.startswith("-E")):
            error: str = arg.replace("-E", "")
            if (error == ""):
                self.error("[-] No error specified after -E flag.\n")
            else:
                self.errors.append(error)

    def handle_options(self, arg: str) -> None:
        if (arg in self.options):
            self.options[arg] = True

    def handle_arch(self, arg: str) -> None:
        if (arg.startswith("-arch=")):
            self.arch = arg.replace("-arch=", "")
            if (not self.arch in ["X86_64", "X64_32"]):
                self.error(f"[-] Invalid architecture {self.arch}.\n")

    def handle_name(self, arg: str, i: int, args: list) -> bool:
        if (arg.startswith("-o")):
            if (i + 1 < len(args)):
                self.outputName = args[i + 1]
                if (self.outputName == ""):
                    self.error("[-] No output name specified after -o flag.\n")
                if (self.outputName.startswith("-")):
                    self.error("[-] No output name specified after -o flag.\n")
            else:
                self.error("[-] No output name specified after -o flag.\n")
            return True
        return False

    def handle_entry(self, arg: str, i: int, args: list) -> bool:
        if (arg.startswith("-e")):
            if (i + 1 < len(args)):
                self.entry = args[i + 1]
                if (self.entry == ""):
                    self.error("[-] No entry point specified after -e flag.\n")
                if (self.entry.startswith("-")):
                    self.error("[-] No entry point specified after -e flag.\n")
            else:
                self.error("[-] No entry point specified after -e flag.\n")
            return True
        return False

    def invalid_flag(self, flag: str) -> None:
        isInvalid = True
        if (flag.startswith("-")):
            if (flag in self.options):
                isInvalid = False
            if (flag.startswith("-arch=")):
                isInvalid = False
            if (flag.startswith("-E")):
                isInvalid = False
            if (flag.startswith("-W")):
                isInvalid = False
            if (flag.startswith("-o")):
                isInvalid = False
            if (flag.startswith("-e")):
                isInvalid = False
            if (isInvalid):
                self.error(f"[-] Invalid flag {flag}.\n")

def check_files(files: list) -> list:
    return_value: list = []

    if (len(files) == 0):
        return_value.append("[-] No input files specified.\n")
    for file in files:
        if (not os.path.exists(file)):
            return_value.append(f"[-] File {file} does not exist.\n")
    return return_value

def parse_args(args: list) -> object:
    parser: Parser = Parser()
    to_pass: bool = False

    for i, arg in enumerate(args):
        if (to_pass):
            to_pass = False
            continue
        parser.handle_warnings(arg)
        parser.handle_errors(arg)
        parser.handle_options(arg)
        parser.handle_arch(arg)
        if (parser.handle_name(arg, i, args)):
            to_pass = True
        if (parser.handle_entry(arg, i, args)):
            to_pass = True
        if (not arg.startswith("-") and not to_pass):
            if (not arg.endswith(".fly")):
                parser.error(f"[-] Invalid file extension for {arg}. Must be '.fly'.\n")
            else:
                parser.files.append(arg)
        parser.invalid_flag(arg)
    checked_files: list = check_files(parser.files)
    for item in checked_files:
        parser.error(item)

    return parser