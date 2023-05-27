import datetime
import ply.lex as lex
import re

#literals = ['[', ']', '=', ',', '{', '}', '.','(',')']

tokens = (
    'DATETIME',
#    'TABLE',
#    'SUB_TABLE',
    'KEY',
#    'ARRAY',
    #'INLINETABLE', #?
    #'TABLENAME', #?
    #'SUBTABLENAME', #?
    'COMMENT',
    'STRING',
    'NUMBER',
    'BOOLEAN',
    'NEWLINE',
    'EQUALS',
    'LSQBRACKET', 
    'RSQBRACKET',
    'COMMA',
    'LCHAVETA', #?
    'RCHAVETA', #?
    'DOT', #?
    'LPAREN', #?
    'RPAREN' #?
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


#t_INLINETABLE = r'\{[^{}]*\}'
#t_TABLENAME = r'(?<=\[)[^\[\]""]+(?=\])'
#t_SUBTABLENAME = r'(?<=\[)[^\[\]"]+\.[^\[\]"]+(?=\])'
t_LSQBRACKET = r'\['
t_RSQBRACKET = r'\]'
t_COMMA = r'\,'
t_EQUALS = r'\='
t_LCHAVETA = r'\{'
t_RCHAVETA = r'\}'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore  = ' \t\r'

def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
