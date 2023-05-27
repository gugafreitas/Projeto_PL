import json
import sys
import ply.lex as lex
from TP_lex import lexer
from TP_yacc import dictionary
from TP_yacc import parser


def main():
    #TP_lex.input(input)
    source = ""
#    dictionary = {}#adicionamos tudo para aqui para dentro
    
    f = open("text.toml",encoding="utf-8")
    lines = f.readlines()
    for linha in lines:
        source += linha
    
    lexer.input(source)
    while tok := lexer.token():
        print(tok)

    json_str = parser.parse(source)
    print(dictionary)

if __name__ == '__main__':
    main()