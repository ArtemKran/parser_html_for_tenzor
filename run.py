#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from parser import Parser

__author__ = 'Artem Kraynev'


def set_help_text():
    help_text = """
Параметры:
-h - справка
url - полный путь Например: https://docs.python.org/3
"""
    sys.stdout.write(help_text)
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("""
Недостанточно аргументов

Используйте: python script.py <url>
Справка: python script.py -h
        """)
    elif len(sys.argv) == 2:
        if sys.argv == '-h' or '--help':
            set_help_text()
            sys.exit()
        else:
            parser = Parser(sys.argv[1])
    else:
        print("""
Слишком много аргументов

Используйте: python script.py <url>
Справка: python script.py -h
        """)
