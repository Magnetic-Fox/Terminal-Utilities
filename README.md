# Terminal Utilities (Python)

## In brief

This repository contains very simple utilities for classic terminal manipulation (*VT100/ANSI compatible*) written in Python.
These utilities can be used for BBS-like services, especially for dial-up connections.

## Packages needed to run these codes

You'll need to install `readchar` library for these codes to work. This can be installed using `pip` utility.

## How to use these codes?

Well, just dive in the manual of VT100 terminal to get the main goal of using such a device and then You'll probably get what's going on in these codes. ;) For short.

`ansi.py` contains some of the most useful procedures for controlling ANSI-like terminals, such as: `setFgColorT`, `setBgColorT`, `setCurPos`, `reset`, `clear`, `setBold`, `setReverse`, `setNoWrapAround`, etc. If You ever programmed in Turbo Pascal using CRT unit, You'll probably know what's going on. :)

`color.py` contains classic color definition. Useful for procedures from above code.

`listutil.py` is simple (but somehow powerful) utility to create text list selector with scrolling optimized for modem connections (full redraws occures when it's really necessary). Hope it's bug free (it was kinda tricky to code it properly).

`termsize.py` contains very useful procedure for gathering terminal's screen size (in chars). This code was inspired by idea suggested by someone on Stack Overflow (can't remind now what subject was it). The algorithm is simple: 1. set cursor position somewhere much beyond the real screen size (say, 999x999), 2. this will cause the terminal to set caret to the maximum possible position (say, 80x24), 3. ask terminal to give information about its cursor position, which, in fact, will reveal the terminal's screen size. Genius. :)

## Disclaimer

Codes are provided here "AS IS" in hope they'll be useful. I've tested them as much as I could and found no bugs (especially harmful). However, **I take no responsibility for anything. You're using these codes at your own risk!**

## License

**Free.** Please, just give me credits if You decide to use these codes somewhere in Your project. Thanks! :)
Well, I'll be happy too if You contact me before using these codes in any kind of a paid software (I don't think anybody would ever want to, but...).

*Bartłomiej "Magnetic-Fox" Węgrzyn,*
*5th July 2024*