import json


def takeNext(current,line,source,update = 1):
    current += update
    # return line[current][0]
    if current >= len(line):
        # print("lol",source)
        if source == "expression":
            print("</expression>")
        return
    TagDict = {"OpenOperator":OpenC,"identifier":Variable,"constant":Constant,"string":Str,"comma":comma,\
                "CloseOperator":CloseC,"boolOp":BoolOp,"operator":Operator,"type":Type,\
                "input":Input}
    TagDict[line[current][0]](current,line,source)
    pass

def expression(current,line,source):
    if source in ("args","print"):
        print("<expression>")
        takeNext(current,line,"expression")
        # print("</expression>")

    if source == "CloseC":
        print("</expression>")
        takeNext(current,line,"CLoseC")
    pass

def comma(current,line,source):
    print("</expression>\n<expression>")
    takeNext(current,line,source)

def OpenC(current,line,source):
    # print("called",source)
    if source == "args":
        expression(current,line,source)
    if source == "value":
        print("<operator>(</operator>")
        takeNext(current,line,source)
    pass

def CloseC(current,line,source):
    if source == "expression":
        expression(current,line,"CloseC") 
    if source == "value":
        print("<operator>)</operator>")
        takeNext(current,line,source)
# def BodyBeg(current,line,source):
#     print("<body>")


def Input(current,line,source):
    print("<input></input>")

def Type(current,line,source):
    typ = line[current][1]
    print("<type>{}</type>".format("typ"))
    takeNext(current,line,source=source)

def BoolOp(current,line,source):
    bop = line[current][1]
    print("<operator>{}</operator>".format(bop))

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
    print("<constant>{}</constant>".format(c))
    takeNext(current,line,source)

def Variable(current,line,source):
    print("<variable>")
    variable_name = line[current][1]
    print("<var_name>{}</var_name>".format(variable_name))
    print("</variable>")
    if source == "assignment":
        print("<value>")
        takeNext(current,line,"value")
        print("</value>")
    else:
        takeNext(current,line,source)
    pass


def Function(current,line):
    print("<function>")
    function_name = line[current][1]
    print("<function_name>{}</function_name>".format(function_name))
    print("<args>")
    takeNext(current,line,"args")
    # print(tag)
    print("<done><\done>")
    print("</args>")    
    print("</function>")
    
def Assignment(current,line):
    print("\n\n")
    print("<assignment>")
    takeNext(current,line,"assignment",0)
    # Variable(current,line,"assignment")
    print("</assignment>")

def If(current,line):
    print("\n\n")
    print("<if>")
    print("<condition>")
    takeNext(current,line,"if",0)
    print("</condition>")
    print("</if>")
    pass

def Else(current,line):
    print("\n\n")
    print("<else></else>")
    pass

def Print(current,line):
    print("\n\n")
    print("<print>")
    expression(current-1,line,"print")
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

def bodyTagger(old,newer):
    if old<newer:
        print("<body>")
    while(newer<old):
        print("<done></done>")
        print("</body>")
        old -=1
    pass

if __name__ == "__main__":
    with open("Table.json") as F:
        JFile = json.load(F)
    TagDict = {"function":Function,"assignment":Assignment,"if":If,\
				"else":Else,"print":Print,"while":While,\
                "OpenOperator":OpenC}
    print("<program>")
    old_indent = 0
    for line in JFile:
        # print(line)
        tag = line["tag"]
        new_indent = line["intendLevel"]
        line = line["data"]
        bodyTagger(old_indent,new_indent)
        old_indent = new_indent
        TagDict[tag](0,line)
    bodyTagger(old_indent,0)
    print("</program>")
    
