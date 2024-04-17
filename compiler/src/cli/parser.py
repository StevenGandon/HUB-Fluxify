import os

class Parser:
    def __init__(self) -> None:
        self.arch: str = "X86_64"
        self.options: dict = {
            "-c": False,
            "-h": False
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
        if (arg.startswith("-W") and self.stop == False):
            warning: str = arg.replace("-W", "")
            if (warning == ""):
                self.error("[-] No warning specified after -W flag.\n")
            else:
                self.warns.append(arg.replace("-W", ""))

    def handle_errors(self, arg: str) -> None:
        if (arg.startswith("-E") and self.stop == False):
            error: str = arg.replace("-E", "")
            if (error == ""):
                self.error("[-] No error specified after -E flag.\n")
            else:
                self.errors.append(error)

    def handle_options(self, arg: str) -> None:
        if ((arg in self.options) and self.stop == False):
            self.options[arg] = True

    def handle_arch(self, arg: str) -> None:
        if (arg.startswith("-arch=") and self.stop == False):
            self.arch = arg.replace("-arch=", "")
            if (not self.arch in ["X86_64", "X86_32"]):
                self.error(f"[-] Invalid architecture {self.arch}.\n")

    def handle_name(self, arg: str, i: int, args: list) -> bool:
        if (arg.startswith("-o") and self.stop == False):
            if (i + 1 < len(args)):
                self.outputName = args[i + 1]
                if (self.outputName == ""):
                    self.error("[-] No output name specified after -o flag.\n")
                    return True
                if (self.outputName.startswith("-")):
                    self.error("[-] No output name specified after -o flag.\n")
                return True
            else:
                self.error("[-] No output name specified after -o flag.\n")
                return True
        return False

    def handle_entry(self, arg: str, i: int, args: list) -> bool:
        if (arg.startswith("-e") and self.stop == False):
            if (i + 1 < len(args)):
                self.entry = args[i + 1]
                if (self.entry == ""):
                    self.error("[-] No entry point specified after -e flag.\n")
                    return True
                if (self.entry.startswith("-")):
                    self.error("[-] No entry point specified after -e flag.\n")
                return True
            else:
                self.error("[-] No entry point specified after -e flag.\n")
        return False

def check_files(files: list) -> list:
    return_value: list = []

    if (len(files) == 0):
        return_value.append("[-] No input files specified.\n")
    for file in files:
        if (not os.path.exists(file)):
            return_value.append(f"[-] File {file} does not exist.\n")
    return return_value

def parse_args(args: list) -> object:
    parser: object = Parser()
    to_pass: bool = False

    for i, arg in enumerate(args):
        print(arg + " " + str(i) + " " + "True" if to_pass else "False")
        if (to_pass):
            to_pass = False
            continue
        parser.handle_warnings(arg)
        parser.handle_errors(arg)
        parser.handle_options(arg)
        parser.handle_arch(arg)
        to_pass = parser.handle_name(arg, i, args)
        to_pass = parser.handle_entry(arg, i, args)
        if (not arg.startswith("-") and not to_pass):
            if (not arg.endswith(".fly")):
                parser.error(f"[-] Invalid file extension for {arg}. Must be '.fly'.\n")
            else:
                parser.files.append(arg)
    checked_files: list = check_files(parser.files)
    for item in checked_files:
        parser.error(item)

    return parser