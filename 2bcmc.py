#!/usr/bin/python
# © Patrick Reader <_@pxeger.com> 2021
# Licensed under the Artistic License 2.0 (https://github.com/pxeger/2bcmc/blob/main/LICENCE.txt)

# Created for Redwolf Programs' CMC (https://chat.stackexchange.com/transcript/message/59389303#59389303)
# a somewhat golf-oriented language with a two bit code page

from collections.abc import Iterator, Iterable


codepage = {
    "=": 0,  # push literal integer
    "*": 1,  # repeat + eval
    "-": 2,  # subtract
    # TODO: op 3??
    " ": None,  # ignored
    "\n": None,  # ignored
}


def interpret(qits: Iterable[int]):
    stack = []
    _interpret(iter(qits), stack)
    print("\n".join(stack))


def _interpret(qits: Iterator[int], stack: list):
    def pop():
        try:
            return stack.pop()
        except IndexError:
            # implicit input
            return eval(input())

    for qit in qits:
        if qit == 0:
            # push literal integer
            n = 0
            while x := next(qits, 0):
                n *= 3
                n += x - 1
            stack.append(n)
        elif qit == 1:
            # repeat + eval
            qits2 = []
            p = pop()
            while n:
                qits2.append(p & 0b11)
                p >>= 2
            n = pop()
            for _ in range(n if n >= 0 else 1):
                _interpret(qits2, stack)
        elif qit == 2:
            # subtract
            a = pop()
            b = pop()
            stack.append(a - b)
        elif qit == 3:
            raise NotImplementedError("command 3 is unimplemented")
        elif qit is None:
            # gracefully ignore to facilitate parsing lol
            pass
        else:
            assert False


if __name__ == "__main__":
    import sys

    prog, args = sys.argv

    if "--help" in args:
        print(f"""\
Usage: {prog} (-b | -u | -c) <program>

Executes `2bcmc` code from <program>

Options:
\t-b\tread code from the file <program> in binary mode (4 commands per byte)
\t-u\tread code from the file <program> in unicode mode (using code page)
\t-c\t<program> is a literal string of code (using the code page)

More info: https://github.com/pxeger/2bcmc""")
    sys.exit(0)
    
    match args:
        case ["-b", path]:
            with open(path, "rb") as file:
                code = file.read()
            qits = reversed([(byte >> n) & 0b11 for byte in code for n in range(0, 8, 2)])
        case ["-u", path]:
            with open(path, encoding="utf-8") as file:
                code = file.read()
            try:
                qits = [codepage[char] for char in code]
            except KeyError:
                sys.exit(f"invalid character in code")
        case ["-c", code]:
            qits = [codepage[char] for char in code]
        case _:
            sys.exit(f"{prog}: invalid options. Try `{prog} --help`")

    interpret(qits)
