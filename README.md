# HUB-Fluxify

The repository for the fluxify programming language.

## Badges

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/StevenGandon/HUB-Fluxify/blob/main/LICENSE)

## License

[License](https://github.com/StevenGandon/HUB-Fluxify/blob/main/license)

## Authors

- [Steven GANDON](https://www.github.com/goldenapple3619)
- [Keenan DEBOISSY](https://www.github.com/kdeboissy)
- [Bhuvan ARNAUD](https://www.github.com/BhuvanArn)
- [Erwann TANGUY](https://www.github.com/Fizo55)

## Documentation

Fluxify is an easy to learn programming language, with a minimalist syntax like Python. It is a very high level programming language, it has high-level data types (only one, actually). It is a compiled and interpreted with linkage language.

In this repository, there are five main directories:
- `compiler` - The source code of the compiler
- `vm` - The source code of the interpreter
- `libfly` - The standard library of the language
- `fli` - The command line interface of the language
- `flo_to_exe` - Executable to convert a `.flo` file to a `.exe` file (in windows) or a `binary` file (in linux)

### Syntax

The syntax of the language is very simple, it is a minimalist language. Here is an example of a program in Fluxify:

```fluxify
=> This is a comment

=> This is a function
fun main(argc, argv) [

    var a = 1

    ==>
    Multiline
    Comment
    <==
]

```

### Data Types

The language can handle different data, all in two : 'var' and 'fun'.

- `string` : a string of characters
- `int` : an integer
- `function` : a function

## Compilation

The language files are written with the extension `.fly`.

The language is compiled with a compiler written in Python. The compiler generates an intermediate code (OBJ file with extension `.flo`) that is interpreted by the virtual machine, written in C.


The compiler is named `fcc` (Fluxify Code Compiler) and the virtual machine is named `fvm` (Fluxify Virtual Machine).

To compile a program in Fluxify, you must use the following command:

```bash
$ fcc program.fly
```

`fcc` has more arguments than just the file name, you can see all of them with the man page of the compiler :

```bash
man ./docs/man/man1/fcc.1
```

## Execution

To execute a program in Fluxify, you must use the following command:

```bash
$ fvm program.flo
```

`fvm` by default will execute the program with the architecture it recognises with the .flo file. If you want to execute the program with a specific architecture, you can use the `-arch` option :

```bash
$ fvm program.flo -arch X86_64
```
or
```bash
$ fvm program.flo -arch X64_32
```

`fvm` will execute the program with the architecture you specified and will return the output of the program in the terminal. I will **not** create a file with the output of the program (binary or exe).

## Standard Library

The standard library of the language is very simple, it is composed of a few functions to manipulate strings, to add functionality to the language (like write in a file), etc.

When you compile your own Fluxify program, the compiler will automatically link the standard library to your program. You don't have to do anything, the compiler will do it for you (it won't call the functions at your place tho!).

## Command Line Interface

The command line interface of the language is a simple program named `fli` that allows you to compile and execute a program in Fluxify with a single command.

To compile and execute a program in Fluxify, you must use the following command:

```bash
$ fli program.fly [path_to_fcc] [path_to_fvm]
```

- `path_to_fcc` is the path to the compiler
- `path_to_fvm` is the path to the virtual machine

This command will open a simple shell where you can write code in Fluxify and this code will be compiled in a file named `fly.out`, you can now run this file with the virtual machine.

## Converter

The converter is a simple program that allows you to convert a `.flo` file to a `.exe` file (in windows) or a `binary` file (in linux). It's name is `flo_to_exe`.

How to use it :

```bash
$ flo_to_exe program.flo [os] [arch]
```

- `os` is the operating system of the computer (`posix` for linux or `nt` for windows)
- `arch` is the architecture of the computer (`X86_64` for 64 bits or `X64_32` for 32 bits)

The program will create a file named `result.exe` (in windows) or `result` (in linux) that is the executable of the program in Fluxify.

## Installation

- [X] Windows Binaries
- [X] MacOS Makefile
- [X] Linux Makefile
- [X] Docker Image
- [X] GitHub Publications
