import json
import sys
import ply.lex as lex
from TP_lex import lexer
from TP_yacc import parser

example2 = '''
title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
date = 2010-04-23
time = 21:30:00

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

[servers.alpha]
ip = "10.0.0.1"
dc = "eqdc10"

[servers.beta]
ip = "10.0.0.2"
dc = "eqdc10"

# Line breaks are OK when inside arrays
hosts = [
"alpha",
"omega"
]
'''

example3 = '''title = "TOML Example"

hosts = [
"alpha",
"omega"
]'''


'''
{
  "title": "TOML Example",
  "owner": {
    "name": "Tom Preston-Werner",
    "date": "2010-04-23",
    "time": "21:30:00.000"
  },
  "database": {
    "server": "192.168.1.1",
    "ports": [
      8001,
      8001,
      8002
    ],
    "connection_max": 5000,
    "enabled": true
  },
  "servers": {
    "alpha": {
      "ip": "10.0.0.1",
      "dc": "eqdc10"
    },
    "beta": {
      "ip": "10.0.0.2",
      "dc": "eqdc10",
      "hosts": [
        "alpha",
        "omega"
      ]
    }
  }
}

'''


def main():
    #TP_lex.input(input)
    source = ""
#    dictionary = {}#adicionamos tudo para aqui para dentro
    
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