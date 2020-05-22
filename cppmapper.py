import xml.etree.ElementTree as ET
def operator_change():
     for index in range(len(text)):
             if(text[index]=='lt'):
                 text[index]='<'
             if(text[index]=='le'):
                 text[index]='<='
             if(text[index]=='gt'):
                 text[index]='>'
             if(text[index]=='ge'):        
                 text[index]='>='


def main_statement(i):
        if(tag[i]=='variable' or tag[i]=='constant' or tag[i]=='operator'):
            f.write(text[i])
        if(tag[i]=='print'):
            f.write('printf("')
            f.write(text[i])
            f.write('");\n')
        if(tag[i]=='input'):
            f.write('scanf("')
            f.write(text[i])
            f.write('");\n')
        if(tag[i]=='expression-end'):
            f.write(';\n')
        if(tag[i]=='if'):
            f.write('if(')
        if(tag[i]=='if_body_beg'):
            f.write(')\n{\n')
        if(tag[i]=='if_body_end'):
            f.write('\n}\n')
        if(tag[i]=='else'):
            f.write('else{\n') #use if body end tag
        if(tag[i]=='else-if'):
            f.write('else if(')
        
        if(tag[i]=='for'):
            f.write('for(')
        if(tag[i]=='for_initialize'):
            f.write(text[i+1])
            f.write('=')
            f.write(text[i+2])
            f.write(';')
            i+=3
        if(tag[i]=='for_condition'):
            f.write(text[i+1])
            f.write(text[i+2])
            f.write(text[i+3])
            f.write(';')
            i+=4
        if(tag[i]=='for_increment'):
            f.write(text[i+1])
            f.write(text[i+2])
            f.write('=')
            f.write(text[i+3])
            f.write(';')
            i+=4
        if(tag[i]=='for_body_beg'):
            f.write(')\n{\n')
        if(tag[i]=='for_body_end'):
            f.write('\n}\n')
        if(tag[i]=='while'):
            f.write('while(')
        if(tag[i]=='while_body_beg'):
            f.write(')\n{\n')
        if(tag[i]=='while_body_end'):
            f.write('\n}\n')
        if(tag[i]=='bracket_open'):
            f.write('(')
        if(tag[i]=='bracket_close'):
            f.write(')')
        if(tag[i]=='break'):
            f.write('break;\n')
        if(tag[i]=='continue'):
            f.write('continue;\n')
        if(tag[i]=='switch'):
            f.write('switch')
        if(tag[i]=='case'):
            f.write('case:\t')
        if(tag[i]=='default'):
            f.write('default:\t')
        if(tag[i]=='pointer'):
            f.write('*')
            f.write(text[i])
        if(tag[i]=='address'):
            f.write('&')
            f.write(text[i])
        if(tag[i]=='int-array-declare'):
            f.write('int ')
            f.write(text[i])
        if(tag[i]=='int-array'):
            f.write(text[i])
            f.write(' ')
        if(tag[i]=='int-array-index'):
            f.write('[')
            f.write(text[i])
            f.write(']')
        if(tag[i]=='string-declare'):
            f.write('char ')
            f.write(text[i])
            string_var.append(text[i])
        if(tag[i]=='string-index'):
            f.write('[')
            f.write(text[i])
            f.write(']')
        if(tag[i]=='string'):
            f.write(text[i])
        if(tag[i]=='strlen'):
            f.write('strlen(')
            if(text[i] in string_var):
                f.write(text[i]) #string-name
            else:
                f.write('\"')
                f.write(text[i])
                f.write('\"')
            f.write(');\n')
        if(tag[i]=='strcpy'):
            f.write('strcpy(')
            if(text[i+1] in string_var):
                f.write(text[i+1]) #string-name
            else:
                f.write('\"')
                f.write(text[i+1])
                f.write('\"')
            f.write(',')
            if(text[i+2] in string_var):
                f.write(text[i+2]) #string-name
            else:
                f.write('\"')
                f.write(text[i+2])
                f.write('\"')
            f.write(');\n')
        if(tag[i]=='strcat'):
            f.write('strcat(')
            if(text[i+1] in string_var):
                f.write(text[i+1]) #string-name
            else:
                f.write('\"')
                f.write(text[i+1])
                f.write('\"')
            f.write(',')
            if(text[i+2] in string_var):
                f.write(text[i+2]) #string-name
            else:
                f.write('\"')
                f.write(text[i+2])
                f.write('\"')
            f.write(');\n')
        if(tag[i]=='strcmp'):
            f.write('strcmp(')
            if(text[i+1] in string_var):
                f.write(text[i+1]) #string-name
            else:
                f.write('\"')
                f.write(text[i+1])
                f.write('\"')
            f.write(',')
            if(text[i+2] in string_var):
                f.write(text[i+2]) #string-name
            else:
                f.write('\"')
                f.write(text[i+2])
                f.write('\"')
            f.write(');\n')
        if(tag[i]=='concat'):
            f.write('+')
        if(tag[i]=='append'):
            f.write(text[i+1])
            f.write('.append(')
            f.write(text[i+2])
            f.write(');\n')
        if(tag[i]=='length'):
            f.write(text[i])
            f.write('.length();\n')
        if(tag[i]=='max'):
            f.write('max(')
            f.write(text[i+1])
            f.write(',')
            f.write(text[i+2])
            f.write(');')
        if(tag[i]=='min'):
            f.write('min(')
            f.write(text[i+1])
            f.write(',')
            f.write(text[i+2])
            f.write(');')
        if(tag[i]=='sqrt'):
            f.write('sqrt(')
            f.write(text[i+1])
            f.write(');') 
        if(tag[i]=='round'):
            f.write('round(')
            f.write(text[i+1])
            f.write(');') 
        if(tag[i]=='log'):
            f.write('log(')
            f.write(text[i+1])
            f.write(');')       
        if(tag[i]=='calloc'):
            f.write('calloc(')
            f.write(text[i+1])
            f.write(',')
            f.write(text[i+2])
            f.write(');\n')
            i+=3
        if(tag[i]=='free'):
            f.write('free(')
            f.write(text[i+1])
            f.write(');\n')
            i+=2
        if(tag[i]=='malloc'):
            f.write('malloc(')
            f.write(text[i+1])
            f.write(');\n')
            i+=2
        if(tag[i]=='realloc'):
            f.write('realloc(')
            f.write(text[i+1])
            f.write(',')
            f.write(text[i+2])
            f.write(');\n')
            i+=3

def header_func():
    for i in range(len(tag)):
        if(tag[i]=='header'):
            f.write('#include<')
            f.write(text[i])
            f.write('>\n')

def macro_func():
    for i in range(len(tag)):
        if(tag[i]=='macro'):
            f.write('#DEFINE ')
            f.write(tag[i+1])  #Macro-Name
            f.write(tag[i+2])  #macro-value
            i+=2

def function_declare():
    #while(function_start_index):
    #   start=function_start_index.pop()
    #   end= function_end_index.pop()
    for i in range(tag.index('function'), tag.index('function-body-end')):
        if(tag[i]=='function-return-type'):
            f.write(text[i])
        if(tag[i]=='function-name'):
            f.write(text[i])
            f.write('(')
        if(tag[i]=='function-body-begin'):
            f.write(')\n{\n')
        if(tag[i]=='function-parameter-type'):
            f.write(text[i])
            f.write(' ')
        if(tag[i]=='function-parameter-name'):
            f.write(text[i])
            if(tag[i+1]=='function-parameter-type'):
                f.write(',')
            else:
                f.write(');\n)
        if(tag[i]=='function-call'):
            f.write(text[i+1])
            f.write('(')
        else:
            main_statement(i)
def structure_declare():
    for i in range(tag.index('structure'), tag.index('structure-body-end')):
        if tag[i]=='structure':
            f.write('struct')
            f.write(' ')
        if(tag[i]=='structure-name'):
            f.write(text[i])
        if(tag[i]=='struct-define':
            f.write('{\n')
        if(tag[i]=='struct-variable'):
            f.write(text[i+1])
            f.write(' ')
            f.write(text[i+2])
            f.write(';')
        if(tag[i]=='struct-define-end'):
            f.write('}\n')
        else:
            main_statement(i)
        

    
def main_func(main_number):
    f.write('int_main(){\n')
    var_declare()
    for i in range(main_number, len(tag)):
        main_statement(i)
    f.write('return 0;\n}\n')



def var_declare():
    for i in range(len(tag)):
        if(tag[i]=='var-declare'):
            f.write(text[i+1])
            var_type.append(text[i+1])
            f.write(text[i+2])
            var_name.append(text[i+2])
            i+=2

def convertercpp():
    main_number=tag.index('main')
    header_func()
    macro_func()
    function_declare()
    structure_declare()
    main_func(main_number)


file="xmlfile.xml"
mytree = ET.parse(file)
myroot = mytree.getroot()

    #print(child.tag, child.attrib)
string_var=[]
for i in range(len(tag)):
    if(tag[i]=='function-body-begin'):
        function_start_index.append(tag.index('function-body-start'))
    if(tag[i]=='function-body-end'):
        function_end_index.append(tag.index('function-body-end'))
structure_index=[]
tag=[]
text=[]
var_type=[]
var_name=[]
for elem in myroot.iter():
    tag.append(elem.tag)
    text.append(elem.text)
convertercpp()
