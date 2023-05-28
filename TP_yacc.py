import ply.yacc as yacc
import json
import sys
from TP_lex import tokens



def p_toml(p):
    '''
    toml : contents
    '''
    p[0] = p[1]


def p_contents(p):
    '''
    contents : contents variables
             | contents table
             | contents subtable
             | variables
             | table
             | subtable
    '''
    if len(p) == 3:
        if isinstance(p[1], dict) and isinstance(p[2], dict):
            addDict(p[1], p[2])
        elif isinstance(p[1], dict) and isinstance(p[2], tuple):
            addDict(p[1], {p[2][0]: p[2][1]})
        else:
            addDict(p[1], {p[2][0][0]: p[2][0][1]})
        p[0] = p[1]
    else:
        if isinstance(p[1], tuple):
            p[0] = {p[1][0]: p[1][1]}
        else:
            p[0] = dict(p[1])




def p_variables1(p):
    '''
    variables : variables variable
              | NEWLINE
    '''
    if len(p) == 2:
        p[0] = []
    else:
        if p[1] is None:
            p[1] = []
        if isinstance(p[2], tuple):
            p[1].append(p[2])
        p[0] = p[1]

def p_variables2(p):
    '''
    variables : variables NEWLINE
              | variable
    '''
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = [p[1]]






def p_table(p):
    '''
    table : LSQBRACKET KEY RSQBRACKET NEWLINE
          | LSQBRACKET KEY RSQBRACKET NEWLINE variables
          | LSQBRACKET KEY RSQBRACKET NEWLINE subtable
    '''
    if len(p) == 5:
        p[0] = [(p[2], {})]
    else:
        p[0] = [(p[2], dict(p[5]))]




def p_subtable(p):
    '''
    subtable : LSQBRACKET KEY DOT KEY RSQBRACKET NEWLINE
             | LSQBRACKET KEY DOT KEY RSQBRACKET NEWLINE variables
    '''
    if len(p) == 7:
        p[0] = [p[2], {p[4]: {}}]
    else:
        p[0] = [(p[2], {p[4]: dict(p[7])})]







def p_variable(p):
    '''
    variable : KEY EQUALS value
    '''
    p[0] = (p[1], p[3])





def p_value(p):
    '''
    value : NUMBER
          | STRING
          | DATETIME
          | array
          | BOOLEAN
    '''
    p[0] = p[1]


def p_array(p):
    '''
    array : LSQBRACKET array_values RSQBRACKET
          | LSQBRACKET NEWLINE array_values RSQBRACKET
          | LSQBRACKET array_values NEWLINE RSQBRACKET
          | LSQBRACKET NEWLINE array_values NEWLINE RSQBRACKET
          | LSQBRACKET RSQBRACKET
    '''
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 5:
        if p[2] == r'\n':
            p[0] = p[3]
        elif p[3] == r'\n':
            p[0] = p[2]
    elif len(p) == 6:
        p[0] = p[3]
    else:
        p[0] = []


def p_array_values(p):
    '''
    array_values : array_values COMMA value
                 | array_values COMMA NEWLINE value
                 | value
    '''
    if len(p) == 4:
        p[0] = p[1]
        p[0] += [p[3]]
 
    if len(p) == 5:
        p[0] = p[1] + [p[4]]

    else:
        p[0] = [p[1]]


def p_error(p):
    print(f"Syntax error at line {p.lineno}, column {p.lexpos}, '{p.value}'")


def addDict(dic1, dic2):    
    for key, value in dic2.items():
        if key in dic1 and isinstance(dic1[key], dict):
            if isinstance(value, dict):
                addDict(dic1[key], value)
            else:
                print("Dictionary error!")
        else:
            if isinstance(value, dict):
                if len(value) == 1:
                    newKey, newV = next(iter(value.items()))
                    print(newKey)
                    dic1[newKey] = newV
                else:
                    dic1[key] = value
            else:
                dic1[key] = value

parser = yacc.yacc()
