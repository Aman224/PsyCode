import xml.etree.ElementTree as ET,re

def converter_python():
    mapper()

#no spaces inside the text in XML tags

def mapper():
    statement = '' 
    value = 0
    indendation_count = 0
    while value < len(tag):
        if(tag[value] != 'done' and  indendation_count):
            cond_statement_indendation(indendation_count)
        if(tag[value] == 'assignment'):
            count = 1                         # enables assignment operation
            for i in range(value+1,len(tag)):
                if(tag[i] == 'var_name' or tag[i] == 'operator' or tag[i] == 'constant' or tag[i] == 'string'):
                    f.write(text[i]+" ")
                    if (count):
                        f.write(" = ")
                        count = 0            # disables assignment operation
                elif tag[i] == 'variable' or tag[i] == 'expression' or tag[i] == 'value':
                    continue
                elif tag[i] == 'list':
                    f.write('[')
                else:
                    value = i-1
                    break
            f.write('\n')
        if(tag[value] == 'print'):
            statement = text[value]
            if(value != len(tag)-1 and tag[value+1] == 'assignment' and tag[value+4] == 'value'):   #for getting input from user
                for i in range(value+1,len(tag)):
                    if (tag[i] == 'var_name'):
                        f.write(text[i] + " = ")
                    elif (tag[i] == 'int' or tag[i] == 'float'):
                        f.write(tag[i]+'(')
                    elif (tag[i] == 'input'):
                        f.write(tag[i]+'('+statement+'))')
                        f.write('\n')
                        value = i
                        break
            else:
                print_expression(value)
        # if(tag[value] == 'function'):

        if(tag[value] == 'if'):
            value = cond_statement_expression(tag[value],value)
            indendation_count += 1
        if(tag[value] == 'elif'):
            value = cond_statement_expression(tag[value],value)
            indendation_count += 1
        if(tag[value] == 'else'):
            indendation_count += 1
            else_expression(value)
            value += 1              #to skip body tag
        if(tag[value] == 'while'):
            value = cond_statement_expression(tag[value],value)
            indendation_count += 1
        if(tag[value] == 'done'):                           #removes loop indendation
            indendation_count -= 1
        if(tag[value] == 'for_each'):
            value = for_expression(value)
            indendation_count += 1
        if(tag[value] == 'keyword'):
            f.write(text[value]+'\n')
        value += 1
 

def cond_statement_indendation(count):
    check = count
    while(check):
        f.write("   ")
        check -= 1

            
def cond_statement_expression(condition,i):
    statement = condition + ' '
    value = 0
    for j in range(i,len(tag)):
        if tag[j] == 'var_name' or tag[j] == 'constant': 
            statement += text[j] + ' '
        elif tag[j] == 'operator':
            if(text[j] == 'g'):
                text[j] = '>'
            elif(text[j] == 'l'):
                text[j] = '<'
            elif(text[j] == 'ge'):
                text[j] = '>='
            elif(text[j] == 'le'):
                text[j] = '<='
            elif(text[j] == 'eq'):
                text[j] = '=='
            statement += text[j] + ' '
        if tag[j] == 'body':
            value = j
            break
    statement += ":" 
    f.write(statement+'\n')
    return value


def else_expression(i):
    statement = 'else:'
    f.write(statement+'\n')


def for_expression(i):
    statement = 'for '
    value = 0
    for j in range(i,len(tag)):
        if tag[j] == 'var_name' :
            statement += text[j] + ' in '
        if tag[j] == 'iterator': 
            statement += text[j] + ' '
        if tag[j] == 'body':
            value = j
            break
    statement += ":" 
    f.write(statement+'\n')
    return value


def print_expression(i):
    statement = 'print' + '(' + text[i] + ')'
    f.write(statement+'\n')


# file = input("enter file to be parsed")
# f = open("Phase1.intXML", "r")
file = "input.ini"
file = file.lstrip()
mytree = ET.parse(file)
myroot = mytree.getroot()
tag = []
text = []
attribute = []
for elem in myroot.iter():
    tag.append(elem.tag)
    text.append(elem.text)
    attribute.append(elem.attrib)
print (tag)
print (text)
f = open("final_python.txt","w")
converter_python()
f.close()


