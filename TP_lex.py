import datetime
import ply.lex as lex
import re


tokens = (
    'DATETIME',
    'KEY',
    'COMMENT',
    'STRING',
    'NUMBER',
    'BOOLEAN',
    'NEWLINE',
    'EQUALS',
    'LSQBRACKET', 
    'RSQBRACKET',
    'COMMA',
    'LCHAVETA', 
    'RCHAVETA', 
    'DOT', 
    'LPAREN',
    'RPAREN' 
)


t_NEWLINE = r'\n'
    

def t_DATETIME(t):
    r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})? | \d{4}\-\d{2}\-\d{2} | \d{2}\:\d{2}\:\d{2})'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_STRING(t):
    r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')'
    t.value = t.value[1:len(t.value)-1]
    return t

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

t_ignore  = ' \t'

def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
