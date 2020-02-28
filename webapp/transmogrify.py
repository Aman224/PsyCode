# from models.py import Content
# import os
import ply.lex as lex

tokens =('PROGRAM','ASSIGN','TO','LOOP','CONDITION','STRING','PRINT','ENDLINE','ENDSECTION','NUMBER','IDENTIFIER','UNKNOWN','ASSIGNOP','EQUALS')
def t_PROGRAM(t):
    r'program'
    print("<program> ",end="",file=fo)
    end_List.append("program")

def t_ASSIGN(t):
    r'set|assign|initiali[zs]e'
    print("<assign> ",end="",file=fo)
    line_List.append("assign")

def t_TO(t):
    r'to'
    print("= ",end = "",file=fo)

def t_EQUALS(t):
    r'=='
    print("<operator> ",end="",file=fo)    

def t_ASSIGNOP(t):
    r'='
    print("= ",end='',file=fo)

def t_OPERATOR(t):
    r'[\+=\-\*\\]+'
    print("<operator> ",end="",file=fo)

def t_LOOP(t):
    r'[dD]o'
    print("<loop> ",end="",file=fo)
    end_List.append("loop")

def t_CONDITION(t):
    r'[iI]f'
    print("<condition> ",end="",file=fo)
    # end_List.append("condition")

def t_STRING(t):
    r'\"(\\.|[^"\\])*\"'
    print("<string> ",end="",file=fo)

def t_PRINT(t):
    r'print\s'
    print("<keyword> <print> ",end="",file=fo)

def t_INTENDLEVEL(t):
    r'\n([\s ]*)'
    if len(line_List)>0:
        end_tag = line_List.pop()
        print("</{}>".format(end_tag),end="",file=fo)
    print("\n{}".format(' '*len(t.value)),end="",file=fo)
    #  print("IntendLevel:{}".format(len(t.value)-1))

def t_ENDSECTION(t):
    r'[eE]nd.*'
    if len(end_List)>0:
        end_tag = end_List.pop() 
        print("</{}>".format(end_tag),file=fo)
        
def t_NUMBER(t):
    r'\d+[.\d+]*'
    print("<int> ",end="",file=fo)

def t_IDENTIFIER(t):
    r'[0-9a-zA-Z][0-9a-zA-Z_]*'
    print("<identifier> ",end="",file=fo)

# def t_keyword(y):
#     r'auto|double|if|static|break|else|int|struct|case|enum|long|switch|char|extern|near|typedef|const|float|continue|register|union|unsigned|void|while|default|do|goto|signed|while|signed'
def t_UNKNOWN(t):
    r'[.*, ]'
    print(t.value,end="")

def t_error(t):
    print("Well you F*#ed Up :(\n I blame",t)

end_List = []
line_List = []
intend_level = 0
lexer = lex.lex()
# os.system("ls")
f = open("input.ini",'r')
fo = open("Phase1.intXML",'w')
lines = f.read()
lines=lines.replace('\r','')
print(lines)
lexer.input(lines)
print("Phase1")
while True: 
    tok = lexer.token()
    if tok:
        print(tok)
    else:
        break
