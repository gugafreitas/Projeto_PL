import json
import sys
import ply.lex as lex
from TP_lex import lexer
from TP_yacc import parser


def main():
    #TP_lex.input(input)
    source = ""
    
    f = open("text.toml",encoding="utf-8")
    lines = f.readlines()
    f.close()
    for linha in lines:
        source += linha
    
    lexer.input(source)
    while tok := lexer.token():
        print(tok)

    dictionary = parser.parse(source, lexer=lexer)
    json_string = json.dumps(dictionary, indent=2)
    print(dictionary)

    f = open("out.json", "a")
    f.write(json_string)
    f.close()

if __name__ == '__main__':
    main()