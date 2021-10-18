# 2bcmc
2-bit "golfing" language for [Redwolf Programs' Chat Mini Challenge](https://chat.stackexchange.com/transcript/message/59389303#59389303):

> CMC: Make a somewhat golf-oriented language with a two bit code page.  
> Brownie points if it's TC

## Documentation
2bcmc is a stack-based language, and its commands operate on a stack of integers.

If a command pops from an empty stack, an integer is instead read from STDIN.

After the program finishes, the stack is printed, separated by newlines.

There are <s>four</s> three commands:

- `=`: load integer literal
- `*`: repeat + eval
- `-`: subtract
- (there will be a fourth command, but there isn't yet)

Line feeds and spaces are ignored. All other characters are invalid.

### Load Integer Literal
This keeps reading commands until it finds another `=`, decodes those commands as a base-3 integer, and pushes the
result to the stack.

### Repeat + Eval
- pop a value from the stack, call it `p`
- decode `p` in bijective base 4, to an array of commands forming a `2bcmc` program
- pop another value from the stack (underneath `p`), call it `n`
- `n` times: execute that decoded program

If `n` is negative, the program is executed exactly once. If it is zero, the program is not executed.

### Subtract
This pops two values from the stack, subtracts them, and pushes the result.

Note the operation's order: if the top of the stack is `a` and the value underneath is `b`, then the result is **`a - b`**.
