import ply.yacc as yacc
import json
import sys
from TP_lex import tokens

def p_toml(p):
    '''
    toml : contents
    '''
    p[0] = json.dumps(p[1], indent = 2)

#json_object = json.dumps(dictionary, indent=len(dictionary))

def p_contents(p):
    '''
    contents : content
            | content NEWLINE contents
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}

def p_content(p):
    '''
    content : table 
           | variable
    '''
    p[0] = p[1]

def p_table(p):
    '''
    table : LSQBRACKET KEY RSQBRACKET NEWLINE table_contents
          | LSQBRACKET KEY DOT KEY RSQBRACKET NEWLINE table_contents
    '''
    if len(p) == 6:
        p[0] = {p[2]: p[5]}
    else:
        p[0] = {p[2]: {p[4]: p[7]}}

def p_table_empty(p):
    '''
    table : LSQBRACKET KEY RSQBRACKET NEWLINE
          | LSQBRACKET KEY DOT KEY RSQBRACKET NEWLINE
    '''
    if len(p) == 5:
        p[0] = {p[2]: {}}
    else:
        p[0] = {p[2]: {p[4]: {}}}

def p_table_contents(p):
    '''
    table_contents : variable
                   | variable table_contents
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]
        p[0].update(p[3])



def p_variable(p):
    '''
    variable : KEY EQUALS value
             | KEY EQUALS value NEWLINE
    '''
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    else:
        p[0] = {p[1]: p[3]}

def p_value(p):
    '''
    value : STRING
          | BOOLEAN
          | NUMBER
          | DATETIME
          | list
    '''
    p[0] = p[1]

def p_list(p):
    '''
    list : LSQBRACKET RSQBRACKET
         | LSQBRACKET list_values RSQBRACKET
    '''
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]

def p_list_values(p):
    '''
    list_values : value
                 | value COMMA list_values
                 | value COMMA NEWLINE list_values
    '''
    if len(p) == 2:
        p[0] = []
        p[0].append(p[1])
    elif len(p) == 4:
        p[0] = []
        p[0].append(p[1])
        p[0] = p[0] + p[3]
    else:
        p[0] = []
        p[0].append(p[1])
        p[0] = p[0] + p[4]
        
def p_error(p):
    print("Syntax error in input!",p)
    #parser.success=False

    

parser = yacc.yacc()
parser.success=True

source = ""
dictionary = {}#adicionamos tudo para aqui para dentro
    
f = open("text.toml",encoding="utf-8")
for linha in f:
    source += linha



parser.pareseIn = parser.parse(source)

#json_str = json.dumps(pareseIn, indent=2)

#json_object = json.dumps(dictionary, indent=len(dictionary))

#print(source)
if parser.success:
   print('Parsing completed!')
   with open("output.json", "a") as outfile:
        outfile.write(parser.pareseIn)
else:
   print('Parsing failed!')