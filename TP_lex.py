import datetime
import ply.lex as lex
import re

literals = ['[', ']', '=', ',', '{', '}', '.']

tokens = (
    'DATETIME',
#    'TABLE',
#    'SUB_TABLE',
    'KEY',
#    'ARRAY',
    'COMMENT',
    'STRING',
    'NUMBER',
    'BOOLEAN',
    'NEWLINE'
)

# [table-1]
# key1 = "some string"
# key2 = 123

# [table-2]
# key1 = "another string"
# key2 = 456

# String
# Integer
# Float
# Boolean
# Offset Date-Time
# Local Date-Time
# Local Date
# Local Time
# Array
# Inline Table

#t_ARRAY = r'\= \[(.*(,.*)*)\]'
#t_DATE = r'\d{4}\-\d{2}\-\d{2}' #YYYY-MM-DD
#t_TIME = r'\d{2}\:\d{2}\:\d{2}' #HH:MM:SS

t_NEWLINE = r'\n'
    

def t_DATETIME(t):
    r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})? | \d{4}\-\d{2}\-\d{2} | \d{2}\:\d{2}\:\d{2})'
    #t.value = datetime.fromisoformat(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

#def t_ARRAY(t):
#    r'\[\s*((?:".*?")|(?:\[[^\[\]]*\])|(?:-?\d+))(?:\s*,\s*((?:".*?")|(?:\[[^\[\]]*\])|(?:-?\d+)))*\s*\]'
#    #r'\[[\n]?[\s\t]*(-?\d+(\.\d+)?[\n]?[\s\t]*(,[\n]?[\s\t]*-?\d+(\.\d+)?)*|(\".*[^\"]\"|\'.*[^\']\')[\n]?[\s\t]*(,[\n]?[\s\t]*(\".*[^\"]\"|\'.*[^\']\'))*)\]'
#   return t

t_STRING = r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')'

def t_NUMBER(t):
    r'-?\d+(\.\d+)?' 
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'(true|false)'
    if t.value == 'true':
        t.value = True
    else:
        t.value = False
    return t

#def t_TABLE(t):
#    r'[a-zA-Z]\w+'
#    return t

#def t_SUB_TABLE(t):
#    r'[a-zA-Z]\w+(.[a-zA-Z]\w+)+'
#    return t

def t_KEY(t):
    r'[a-zA-Z]\w+'
    return t

t_ignore  = ' \t'

def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)
    
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

lexer = lex.lex()
lexer.input(example2)

while tok := lexer.token():
    print(tok)

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