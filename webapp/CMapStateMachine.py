import json

def SymTab(opt,var_list,Type=None):
    global symbolTable
    # print(symbolTable)
    if opt == "add":
        for var in var_list:
            symbolTable[var] = Type
    elif opt == "get":
        return symbolTable[var_list]
        
def afterIndex(current):
    global nex
    nex= max(nex,current)

def Nex():
    global nex
    return nex

def takeNext(current,line,source,update = 1):
    current += update
    if current >= len(line):
        return
    
    TagDict = {"OpenOperator":OpenC,"identifier":Variable,"constant":Constant,"string":Str,
            "comma":comma,"CloseOperator":CloseC,"OpenSquareOp":OpenSquare,"boolStr":BoolStr,\
            "CloseSquareOp":CloseSquare,"boolOp":BoolOp,"operator":Operator,"type":Type,\
            "input":Input,"function_call":Function}
    
    if source in ("variable","closeSquare"):
        if line[current][0] == "OpenSquareOp":
            TagDict[line[current][0]](current,line,source)    
        else:
            return  
    else:
        TagDict[line[current][0]](current,line,source)
    pass

def expression(current,line,source):
    nextUpdate = {"args":1,"print":0}
    if source in nextUpdate:
            print("<expression>")
            takeNext(current,line,source,nextUpdate[source])
            print("</expression>")
            if source == "args":
                return
                # current = Nex()
                # takeNext(current,line,source)

def comma(current,line,source):
    # print("ok")
    # print(source)
    print("</expression>\n<expression>")
    takeNext(current,line,source)

def OpenC(current,line,source):
    print("<operator>(</operator>")
    if source == "args":
        takeNext(current,line,"OpenC")
        current = Nex()
        takeNext(current,line,source)
      
    if source == "value":
        takeNext(current,line,source)
    pass

def CloseC(current,line,source):
    # print("Im here")
    if source == "OpenC":
        print("<operator>)</operator>")
        afterIndex(current)
        # takeNext(current,line,source)
        return

    if source == "args":
        afterIndex(current)
        # print("end args")
        return

    if source == "value":
        print("<operator>)</operator>")
        takeNext(current,line,source)

def OpenSquare(current,line,source):
    # print("ok")
    if source in ("variable","closeSquare"):
        print("<index>",end="")
        takeNext(current,line,"index")
    else:
        takeNext(current,line,source)

def CloseSquare(current,line,source):
    if source == "index":
        print("</index>")
        takeNext(current,line,"closeSquare")
        afterIndex(current)
# take care of elif also take care of boolStrings

def Input(current,line,source = None):
    print("\n\n")
    print("<input>")
    takeNext(current,line,"Input",0)
    print("</input>")

def Type(current,line,source):
    typ = line[current][1]
    print("<type>{}</type>".format(typ))
    takeNext(current,line,source)

def BoolStr(current,line,source):
    # print("ok")
    bstr = line[current][1]
    print("<operator>{}</operator>".format(bstr))
    takeNext(current,line,source)

def BoolOp(current,line,source):
    bop = line[current][1]
    print("<operator>{}</operator>".format(bop))
    takeNext(current,line,source)

def Operator(current,line,source):
    op = line[current][1]
    print("<operator>{}</operator>".format(op))
    takeNext(current,line,source) #stil value as sourve

def Str(current,line,source):
    st = line[current][1]
    print("<string>{}</string>".format(st))
    takeNext(current,line,source)

def Constant(current,line,source):
    c = line[current][1]
    if source == "index":
        print(c,end="")
    else:
        print("<constant>{}</constant>".format(c))
    takeNext(current,line,source)

def Variable(current,line,source):
    variable_name = line[current][1]
    def ToPrintVar(current,line,source):
        print("<variable>")
        if source in ("print","Input"):
            print("<variable_type>{}</variable_type>".format(SymTab("get",variable_name)))
        print("<variable_name>{}</variable_name>".format(variable_name))
        # to check for index
        takeNext(current,line,"variable")
        global nex
        if nex > current:
            current= nex
            afterIndex(0)
        print("</variable>")
        return current
    # Print 
    current = ToPrintVar(current,line,source)
    # tag checker

    if source == "assignment":
        print("<value>")
        takeNext(current,line,"value")
        print("</value>")

    elif source == "Uassignment":
        print("<value>")
        ToPrintVar(current,line,source)
        takeNext(current,line,"value")
        print("</value>")
    else:
        takeNext(current,line,source)

############ 

def Function(current,line,source=None):
    print("<function_call>")
    function_name = line[current][1]
    print("<function_name>{}</function_name>".format(function_name))
    print("<args>")
    expression(current,line,"args")
    # print(tag)
    print("</args>")    
    print("</function_call>")
    current = Nex()
    takeNext(current,line,source)

def Assignment(current,line):
    print("\n\n")
    print("<assignment>")
    takeNext(current,line,"assignment",0)
    # Variable(current,line,"assignment")
    print("</assignment>")

def UAssignment(current,line):
    print("\n\n")
    print("<assignment>")
    Variable(current,line,"Uassignment")

    print("</assignment>")

def If(current,line):
    print("\n\n")
    print("<if>")
    print("<condition>")
    takeNext(current,line,"if",0)
    print("</condition>")
    print("</if>")
    pass

def Elif(current,line):
    print("\n\n")
    print("<elif>")
    print("<condition>")
    takeNext(current,line,"if",0)
    print("</condition>")
    print("</elif>")

def Else(current,line):
    print("\n\n")
    print("<else></else>")
    pass

def Print(current,line):
    print("\n\n")
    print("<print>")
    expression(current,line,"print")
    print("</print>")
    pass

def While(current,line):
    print("\n\n")
    print("<while>")
    print("<condition>")
    takeNext(current,line,"If",0)
    print("</condition>")
    print("</while>")
    pass

def Declaration(current,line):
    print("\n\n")
    print("<var_declare>")
    Type = line[current][1]
    var_list = line[current+1][1]
    

    # SymTab("add",var_list,Type)
    print("<variable_type>{}</variable_type>".format(Type))
    for var in var_list[::-1]:
        print("<variable>")
        print("<variable_name>{}</variable_name>".format(var))
        print("</variable>")
        if "[" in var:
            var.split("[")
            var = var[0]
        SymTab("add",[var],Type)
    print("</var_declare>")
    pass

def Definition(current,line):
    print("\n\n")
    print("<var_define>")
    Type = line[current][1]
    var_declare_list = line[current+1][1]
    assign_list = line[current+2][1]
    # print(Type)
    # print(var_declare_list)
    # print(assign_list)
    print("<variable_type>{}</variable_type>".format(Type))
    # simple declarations:
    for var in var_declare_list:
        # print("variable",var.lstrip())
        SymTab("add",[var.lstrip().rstrip()],Type)
        print("<variable>")
        print("<variable_name>{}</variable_name>".format(var))
        print("</variable>")
    # assignments
    global lexer
    for var in assign_list:
        var = var.split("=")
        # print(":",var[0].lstrip().rstrip(),":")
        SymTab("add",[var[0].lstrip().rstrip()],Type)
        print("<assignment>")
        print("<variable>")
        print("<variable_name>{}</variable_name>".format(var[0].lstrip().rstrip()))
        print("</variable>")
        print("<value>")
        print("<variable>")
        print("<variable_name>{}</variable_name>".format(var[1].lstrip().rstrip()))
        print("</variable>")
        print("</value>")
        print("</assignment>")

    print("</var_define>")


def Main(current,line):
    print("<main>")

def bodyTagger(old,newer):
    if old<newer:
        print("<body>")
    while(newer<old):
        # print("<done></done>")
        print("</body>")
        old -=1
    pass

if __name__ == "__main__":
    with open("Table.json") as F:
        JFile = json.load(F)
    TagDict = {"function":Function,"assignment":Assignment,"if":If,\
				"else":Else,"elif":Elif,"print":Print,"while":While,\
                "OpenOperator":OpenC,"function_call":Function,\
                "UAssignment":UAssignment,"main":Main,\
                "Declaration":Declaration,"Definition":Definition,\
                "Input":Input}
    print("<program>")
    symbolTable = dict()
    global nex
    old_indent = 0
    isMain = False
    for line in JFile:
        nex = 0
        tag = line["tag"]
        new_indent = line["intendLevel"]
        line = line["data"]
        bodyTagger(old_indent,new_indent)
        old_indent = new_indent
        if tag == "main":
            print("<main>")
            isMain = True
        else:
            TagDict[tag](0,line)
    bodyTagger(old_indent,0)
    if isMain:
        print("</main>")
    print("</program>")

    