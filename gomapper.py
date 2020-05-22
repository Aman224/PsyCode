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

def package_func():
    for i in range(len(tag)):
        if(tag[i]=='package'):
            f.write('package ')
            f.write(text[i])
def import_func():
    for i in range(len(tag)):
        if(tag[i]=='import'):
            f.write('import \"')
            f.write(text[i])
            f.write("\"")


def var_declare():
    for i in range(len(tag)):
        if(tag[i]=='var-declare'):
            f.write('var ')
            f.write(text[i+1]) #name
            f.write(' ')
            f.write(text[i+2]) #type
            f.write(';\n')
        if(tag[i]=='var-define'):
            f.write(text[i+1]) #name
            f.write('=')
            f.write(text[i+2]) #value
            f.write(';\n')
        if(tag[i]=='constant'):
            f.write('const var ')
            f.write(text[i+1]) #name
            f.write(' ')
            f.write(text[i+2]) #type
            f.write('=')
            f.write(text[i+3]) #value
            f.write(';\n')
        if(tag[i]=='map-variable-declare'):
            f.write('var ')
            f.write(text[i]) #map-var-name
            f.write(' map[')
            f.write(text[i+1]) #key-type
            f.write('] ') 
            f.write(text[i+2]) #value-type
            f.write(';\n')
    
def statement():
    if(tag[i]=='print'):
        f.write('fmt.Println(')
        f.write(text[i])
        f.write(')')
    if(tag[i]=='input'):
        f.write('fmt.Scanln(')
        f.write(text[i])
        f.write(')')
    
    if(tag[i]=='if'):
            f.write('if(')
    if(tag[i]=='variable' or tag[i]=='constant'):
        f.write(text[i])
    if(tag[i]=='main'):
        f.write('func main(){')
    if(tag[i]=='end')
        f.write('\n}\n') #for main tag
    if(tag[i]=='variable' or tag[i]=='constant' or tag[i]=='operator'):
        f.write(text[i])

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
        f.write('var ')
        f.write(text[i])
        f.write(' ')
        f.write(text[i+1]) #int-array-index-dec
        f.write(' int;\n')
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
        f.write('len(')
        f.write(text[i]) #string
        f.write(')')
    if(tag[i]=='create-map'):
        f.write('make(map[')
        f.write(text[i+1]) #key
        f.write(']')
        f.write(text[i+2]) #value
    if(tag[i]=='map-key'):
        f.write('[')
        f.write(text[i])
        f.write(']')
    if(tag[i]=='map-value'):
        f.write(text[i])
    
def function_statement():
    if(tag[i]=='function'):
            f.write('func ')
            f.write(text[i+1]) #func-name
            f.write('(')
    if(tag[i]=='function-parameter'):
        if(tag[i+1]=='function-parameter'):
            f.write(text[i])
            f.write(',')
        else:
            f.write(text[i])
            f.write(') ')
    if(tag[i]=='function-return-type'):
        f.write(text[i])
    if(tag[i]=='function-body-begin'):
        f.write('{\n')
    if(tag[i]=='function-body-end'):
        f.write('\n}\n')

def main_func():
    for i in range(len(tag)):
        if(tag[i]=='var-declare' or tag[i]=='var-define' or tag[i]=='constant')
            var_declare()
        else if (tag[i]=='function' or tag[i]=='function-parameter' or tag[i]=='function-return-type' or tag[i]=='function-body-begin' or tag[i]=='function-body-end'):
            function_statement():
        else:
            statement()

def gomapper():
    package_func()
    import_func()
    function_call()
    main_func()




file="xmlfile.xml"
mytree = ET.parse(file)
myroot = mytree.getroot()

    #print(child.tag, child.attrib)
tag=[]
text=[]
var_type=[]
var_name=[]
for elem in myroot.iter():
    tag.append(elem.tag)
    text.append(elem.text)
gomapper()

