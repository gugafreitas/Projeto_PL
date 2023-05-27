import ply.yacc as yacc
import json
import sys
from TP_lex import tokens


def merge_dicts(d1, d2):
    for key, value in d2.items():
        if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
            merge_dicts(d1[key], value)
        else:
            if isinstance(value, dict) and len(value) == 1:
                k, v = next(iter(value.items()))
                d1[k] = v
            elif isinstance(value, tuple):
                d1[key] = { value[0]: value[1] }
            else:
                d1[key] = value

def p_toml0(p):
    '''
    toml : contents
    '''
    p[0] = p[1]


def p_contents(p):
    '''
    contents : contents variable
             | contents variable_list
             | contents table
             | contents subtable
             | variable
             | variable_list
             | table
             | subtable
    '''
    if len(p) == 3:
        if isinstance(p[1], dict) and isinstance(p[2], tuple):
            merge_dicts(p[1], {p[2][0]: p[2][1]})
        elif isinstance(p[1], dict) and isinstance(p[2], list) and len(p[2]) == 2:
            for item in p[2]:
                merge_dicts(p[1], {item[0]: item[1]})
        elif isinstance(p[1], dict) and isinstance(p[2], list) and len(p[2]) == 0:  # handle empty list
            pass
        else:
            merge_dicts(p[1], {p[2][0][0]: p[2][0][1]})
        p[0] = p[1]
    else:
        if isinstance(p[1], tuple):
            p[0] = {p[1][0]: p[1][1]}
        elif isinstance(p[1], list):
            p[0] = dict(p[1])


def p_variable_list1(p):
    '''
    variable_list : variable_list variable
    '''
    if p[1] is None:
        p[1] = []
    if isinstance(p[2], tuple):
        p[1].append(p[2])
    p[0] = p[1]

def p_variable_list2(p):
    '''
    variable_list : variable_list NEWLINE
    '''
    p[0] = p[1]

def p_variable_list3(p):
    '''
    variable_list : variable
    '''
    p[0] = [p[1]]

def p_variable_list4(p):
    '''
    variable_list : NEWLINE
    '''
    p[0] = []

def p_variable(p):
    '''
    variable : KEY EQUALS value
    '''
    key_parts = p[1].split('.')
    if len(key_parts) > 1:
        nested_dict = {key_parts[-1]: p[3]}
        for part in reversed(key_parts[:-1]):
            nested_dict = {part: nested_dict}
        p[0] = (key_parts[0], nested_dict)
    else:
        if isinstance(p[3], list):
            value = dict(value=p[3])
            if len(value) == 1 and 'value' in value:
                p[0] = (p[1], value['value'])
            else:
                p[0] = (p[1], value)
        else:
            p[0] = (p[1], p[3])

def p_subtable1(p):
    '''
    subtable : LSQBRACKET KEY DOT KEY RSQBRACKET NEWLINE
    '''
    p[0] = [p[2], {p[4]: {}}]

def p_subtable2(p):
    '''
    subtable : LSQBRACKET KEY DOT KEY RSQBRACKET NEWLINE variable_list
    '''
    names = p[2].split(".")
    p[0] = [(names[0], {names[1]: dict(p[5])})]


def p_table1(p):
    '''
    table : LSQBRACKET KEY RSQBRACKET NEWLINE
    '''
    p[0] = [(p[2], {})]

def p_table2(p):
    '''
    table : LSQBRACKET KEY RSQBRACKET NEWLINE variable_list
    '''
    p[0] = [(p[2], dict(p[5]))]

def p_table3(p):
    '''
    table : LSQBRACKET KEY RSQBRACKET NEWLINE subtable
    '''
    p[0] = [(p[2], dict(p[5]))]

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
        p[0] = p[1] + [p[4]]
    if len(p) == 5:
        p[0] = p[1] + [p[4]]
    else:
        p[0] = [p[1]]

#arrays com elementos na mesma linha n ta a dar direito

def p_error(p):
    print(f"Syntax error at line {p.lineno}, column {p.lexpos}, '{p.value}'")

parser = yacc.yacc()
