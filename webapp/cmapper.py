import xml.etree.ElementTree as ET,re
import os


def RecursiveTag(Tree,parent=None):
    children=list(Tree)
    #print(children)
    tag=Tree.tag 
    text=Tree.text
    global factor_list
    global prime  
    global variable_list
    global variable
    global expression
    global for_list
    global isPrime
    global isDivisible
    global isMultiple
    global isFactor
    global parameter_list
    global parameters
    global print_func
    #if(len(children)==0):
    #    pass
    #else:
    for child in children:
        if(child.tag=='main'):
            f.write('int main()\n')    
            RecursiveTag(child,'main')
            
        elif(child.tag=='body'):
            f.write('{\n')
            RecursiveTag(child,'body')
            if(parent=='main'):
                f.write('return 0;\n}\n')
            else:
                f.write('\n}\n')
        elif(child.tag=='assignment'):
            RecursiveTag(child,'assignment')
            f.write(expression)
            expression=''
            if(parent=='for_init'):
                f.write(';')
            else:
                f.write(';\n')
        elif(child.tag=='print'):
            f.write('printf("')
            RecursiveTag(child,'print')
            #print(variable_list)
            if(variable_list):
                statement='",'
                for j in range(len(variable_list)):
                    if(j!=len(variable_list)-1):
                        statement+=variable_list[j]+','
                    else:
                        statement+=variable_list[j]
                f.write(statement+');\n')
                variable_list=[]
            elif(print_func==1):
                f.write(';\n')
            else:
                f.write('");\n')
        elif(child.tag=='input'):
            f.write('scanf("')
            RecursiveTag(child,'input')
            statement='",'
            #print(variable_list)
            for j in range(len(variable_list)):
                if(j!=len(variable_list)-1):
                    statement+='&'+variable_list[j]+','
                else:
                    statement+='&'+variable_list[j]
            f.write(statement+');\n')
            variable_list=[]
        elif(child.tag=='header'):
            f.write('#include<'+child.text+'.h>\n')
        elif(child.tag=='type'):
            RecursiveTag(child,'var_declare')
        elif(child.tag=='var_declare'):
            RecursiveTag(child,'var_declare')
            statement=",".join(variable_list)
            f.write(statement+';\n')
            variable_list=[]
        elif(child.tag=='variable'):
            if(parent=='printf_expression'):
                RecursiveTag(child,'printf_expression_variable')
            elif(parent=='input'):
                RecursiveTag(child,'input_expression_variable')
            elif(parent=='function_call' or parent=='function' or parent=='print_func_call'):
                RecursiveTag(child,parent)
            elif(parent=='assignment'):
                RecursiveTag(child,'assignment')
            elif(parent=='function_expression'):
                RecursiveTag(child,'function_expression')
            elif(parent=='var_declare'):
                RecursiveTag(child,'var_declare')
            elif(parent=='condition'):
                RecursiveTag(child,'condition')
            else:
                RecursiveTag(child,parent)
        elif(child.tag=='expression'):
            if(parent=='print'):
                RecursiveTag(child,'printf_expression')
                print(variable_list)
                if(variable):
                    variable_list.append(variable)
                    variable=''
                
            elif(parent=='input'):
                RecursiveTag(child,'input_expression')
                variable_list.append(variable)
                variable=''           
            elif(parent=='assignment'):
                RecursiveTag(child, 'assignment')
            elif(parent=='function_call'):
                RecursiveTag(child,'function_call')
                if(variable):
                    variable_list.append(variable)
                    variable=''
            elif(parent=='print_func_call'):
                RecursiveTag(child,'print_func_call')
                if(parameters):
                    parameter_list.append(parameters)
                    parameters=''
            elif(parent=='function'):
                RecursiveTag(child,'function_expression')
                if(variable):
                    variable_list.append(variable)
                    variable=''
        
        elif(child.tag=='variable_type'):
            if(parent=='printf_expression_variable' or parent=='input_expression_variable' or parent=='print_call'):
                if(child.text=='int'):
                    f.write('%'+'d ')
                elif(child.text=='char'):
                    f.write('%'+'c')
                elif(child.text=='float'):
                    f.write('%'+'f')
                elif(child.text=='double'):
                    f.write('%'+'f')

            elif(parent=='input_expression_variable' or parent=='function_call'):
                continue
            elif(parent=='function_expression'):
                variable+=child.text+' '
            elif(parent=='print_func_call'):
                parameters+=child.text
            elif(parent=='assignment' or parent=='function_call' or parent=='condition'or parent=='for_init'\
     or parent=='for_update' or parent=='for_condition' or parent=='printf_expression_variable' or parent=='input_expression_variable'):
                continue
            else:
                f.write(child.text+' ')
        elif(child.tag=='variable_name'):
            if(parent=='printf_expression_variable' or parent=='function_call' or parent=='function_expression'):
                variable+=child.text
            elif(parent=='print_func_call'):
                parameters+=child.text
            elif(parent=='input_expression_variable'):
                variable_list.append(child.text)
                #variable+=child.text
            elif(parent=='assignment' or parent=='condition'):
                expression+=child.text+' '
                continue
            elif(parent=='condition' and isDivisible==1):
                f.write(child.text)
            elif(parent=='condition' and isMultiple==1):
                f.write(child.text)
            elif(parent=='condition' and isFactor==1):
                factor_list.append(child.text)
            
            elif(parent=='var_declare'):
                variable_list.append(child.text)
                #print(variable_list)
            else:
                f.write(child.text)
                
        elif(child.tag=='string'):
            if(parent=='printf_expression'):
                f.write(child.text+' ')
            elif(parent=='assignment'):
                expression+='"'+child.text+'" '

        elif(child.tag=='if'):
            f.write('if(')
            RecursiveTag(child,'if')
            f.write(')\n')
            if(isDivisible==1):
                isDivisible=0
            if(isMultiple==1):
                isMultiple=0
            if(isPrime==1):
                isPrime=0
        elif(child.tag=='elif'):
            f.write('else if(')
            RecursiveTag(child,'if')
            f.write(')\n')
            if(isDivisible==1):
                isDivisible=0
            if(isMultiple==1):
                isMultiple=0
            if(isPrime==1):
                isPrime=0
        elif(child.tag=='else'):
            f.write('else')
            RecursiveTag(child,'if')
            
        elif(child.tag=='condition'):
            expression=''
            RecursiveTag(child,child.tag)
            if(parent=='for'):
                for_list.append(expression)
                expression=''
                continue
            elif(isPrime==1):
                isPrime=0
                continue
            elif(isDivisible==1):
                f.write('==0 ')
                variable_list=[]
                isDivisible=0
            elif(isMultiple==1):
                f.write('==0 ')
                isMultiple=0
                variable_list=[]
            elif(isFactor==1):
                for j in range(len(factor_list)-1,-1,-1):
                    if(j!=0):
                        f.write(factor_list[j]+' ')
                    else:
                        f.write(factor_list[j])
                f.write('==0')
                isFactor=0
                factor_list=[]            
                #statement=" ".join(factor_list)
                #f.write(statement+'==0 ')

            else:
                f.write(expression)
                expression=''
        elif(child.tag=='constant'):
            if(parent=='function_call' or parent=='function'):
                variable+=child.text
                continue
            if(parent=='printf_expression' or parent=='input_expression'):
                variable+=child.text
            elif(parent=='print_func_call'):
                parameters+=child.text
                continue
            elif(parent=='condition' and isDivisible==1):
                f.write(child.text)
            elif(parent=='condition' and isMultiple==1):
                f.write(child.text)
            elif(parent=='condition' and isFactor==1):
                factor_list.append(child.text)
                #print(factor_list)
            if(parent=='assignment' or parent=='condition'):
                expression+=child.text+' '
                continue
            else: 
                f.write(child.text+' ')
        elif(child.tag=='value'):
            expression+='='
            RecursiveTag(child,'assignment')
        elif(child.tag=='index'):
            if(parent=='assignment'):
                expression+='['+child.text+']'
            f.write('['+child.text+']')
        elif(child.tag=='operator'):
            if(child.text == 'g'):
                child.text = '>'
            elif(child.text == 'l'):
                child.text = '<'
            elif(child.text == 'ge'):
                child.text = '>='
            elif(child.text == 'le'):
                child.text = '<='
            elif(child.text=='and'):
                child.text='&&'
            elif(child.text=='or'):
                child.text='||'
            elif(child.text=='not'):
                child.text=='!'
            elif(child.text=='eq'):
                child.text='=='
            if(parent=='function' or parent=='function_call'):
                variable+=child.text
                continue
            elif(parent=='print_func_call'):
                parameters+=child.text
                print_func=1
                continue
                
            elif(child.text=='#p' and parent=='condition'):
                f.write('isPrime('+expression+')')
                isPrime=1
                prime=1
                continue
            elif(child.text=='d' and parent=='condition'):
                f.write(expression+'% ')
                isDivisible=1
                continue
            elif(child.text=='#m' and parent=='condition'):
                f.write(expression+'% ')
                isMultiple=1
                continue
            elif(child.text=='#f' and parent=='condition'):
                factor_list.append(expression)
                factor_list.append('%')
                #print(factor_list)
                isFactor=1
                continue
            if(isFactor==1):
                factor_list.append(child.text)    

            if(parent=='printf_expression' or parent=='input_expression'):
                variable+=child.text
                continue
            if(parent=='assignment' or parent=='condition'):
                expression+=child.text+' '
                continue
            f.write(child.text+' ')
        elif(child.tag=='assignment'):
            expression=''
            RecursiveTag(child,child.tag)
            if(parent=='for_init' or parent=='for_update'):
                for_list.append(expression)
                expression=''
                continue
        #FUNCTIONCALL
        elif(child.tag=='function_call'):
            if(parent=='printf_expression'):
                RecursiveTag(child,'print_call')
            else:
                RecursiveTag(child,child.tag)
            
        elif(child.tag=='function_name'):
            if(parent=='print_call'):
                variable+=child.text+'('
            else:
                f.write(child.text+'(')
        elif(child.tag=='args'):
            if(parent=='function'):
                RecursiveTag(child,'function')
            elif(parent=='function_call'):
                RecursiveTag(child,'function_call')
            elif(parent=='print_call'):
                RecursiveTag(child,'print_func_call')
                statement=",".join(parameter_list)
                print(statement)
                variable+=statement+')'
                parameter_list=[]
                continue 
                

            statement=",".join(variable_list)
            #print(statement)
            f.write(statement+')')
            variable_list=[]
            if(parent=='function_call'):
                f.write(';\n')
        #FUNCTION
        elif(child.tag=='function'):
            RecursiveTag(child,child.tag)
        elif(child.tag=='function_return_type'):
            f.write(child.text+' ')
        elif(child.tag=='value'):
            f.write('=')
            RecursiveTag(child,child.tag)
        elif(child.tag=='while'):
            f.write('while(')
            RecursiveTag(child,'while')
            f.write(')\n')
             
        elif(child.tag=='break' or child.tag=='continue'):
            f.write(child.tag+';\n')         
variable_list=[]
for_list=[]
factor_list=[]
parameter_list=[]
parameters=''
prime=0
isPrime=0
isDivisible=0
isMultiple=0
isFactor=0
print_func=0
variable=''
expression=''
file="Final_XML.xml"
tree = ET.parse(file)
root = tree.getroot()
f = open("final_output.txt","w")
f.write('#include<iostream.h>')
RecursiveTag(root)
f.close()
if prime==1:
    filenames = ['./webapp/prime.txt', 'final_output.txt']
    with open('final.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
                outfile.write('\n')
    os.rename('final.txt', 'final_output.txt')
    


