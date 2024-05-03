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

In this repository, there are three main directories:
- `compiler` - The source code of the compiler
- `vm` - The source code of the interpreter
- `lib` - The standard library of the language

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

The language can handle different types of data, all in one : 'var'.

- `string` : a string of characters
- `int` : an integer
- `float` : a floating point number
- `array` : an array of values
- `object` : an object ('class' in other languages)
- `function` : a function
- `tuple` : a tuple of values

### Compilation

The language files are written with the extension `.fly`.

The language is compiled with a compiler written in Python. The compiler generates an intermediate code (OBJ file with extension `.flo`) that is interpreted by the virtual machine, written in C.


The compiler is named `fcc` (Fluxify Compiler) and the virtual machine is named `fvm` (Fluxify Virtual Machine).

To compile a program in Fluxify, you must use the following command:

```bash
$ fcc program.fly
```

`fcc` has more arguments than just the file name, you can see all of them with the man page of the compiler :

```bash
man ./docs/man/man1/fcc.1
```

### Standard Library

The standard library of the language is very simple, it is composed of a few functions to manipulate strings, arrays, objects, etc.

... More to come

## Installation

- [ ] Windows Binaries
- [ ] MacOS Makefile
- [ ] Linux Makefile
- [ ] Docker Image
- [ ] GitHub Publications
