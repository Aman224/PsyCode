import ply.lex as lex
import json

def addToLine(tagPair):
	global jsonLine
	jsonLine.append(tagPair)

def setSemantics(semantic):
	global lineSemantic
	lineSemantic = semantic
	
def addToTable():
	global intend_level
	global jsonObj
	global jsonLine
	global lineSemantic
	objDict = dict()
	if len(jsonLine) == 0 and lineSemantic != "body":
		return
	objDict["intendLevel"] = intend_level
	objDict["tag"] = lineSemantic
	objDict["data"] = jsonLine
	lineSemantic = ""
	jsonLine=list()
	jsonObj.append(objDict)

tokens = ("MAIN","VAR","WHILE","TYPE","INPUT","ISGEQ","ISGREATER","ISLEQ","ISLESSER","ASSIGNMENT","EQUALS","PRINT","RETURN",\
		"FUNCTION","PROGRAM","IF","ELSE","BOOLOPERATOR","OPERATOR","CONSTANT","STRING","IDENTIFIERS","OPENSQUARE","CLOSESQUARE","OPENCURLY",\
			"CLOSECURLY","COMMA","NEWLINE","SPACES","UNKNOWN") 
#Direct Replacemet

def t_MAIN(t):
	r'[(function)|program]\s+[mM]ain'
	print("<main>")
	setSemantics="main"
	addToLine("main","main")

def t_VAR(t):
	r'[vV]ariable|of'
	print("",end="")

def t_WHILE(t):
	r'while'
	print("<while>",end="")
	setSemantics("while")

def t_TYPE(t):
	r'type\s[a-z]+'
	print("<type>",end="")
	addToLine(("type",t.value.split()[1]))

def t_INPUT(t):
	r'with\sinput[(\staken)]*\sfrom\suser'
	print("<input>")
	addToLine(("input",t.value))

def t_ISGEQ(t):
	r'is\sgreater\sthan\sor\sequal\sto'
	print("<boolOp>",end="")
	addToLine(("boolOp","ge"))

def t_ISGREATER(t):
	r'is\s[gG]reater\sthan'
	print("<boolOp>",end="")
	addToLine(("boolOp","g"))

def t_ISLEQ(t):
	r'is\s[lL]ess[er]*\sthan\sor\sequal\sto'
	print("<boolOp>",end="")
	addToLine(("boolOp","le"))

def t_ISLESSER(t):
	r'is\s[lL]ess[er]*\sthan'
	print("<boolOp>",end="")
	addToLine(("boolOp","l"))

def t_ASSIGNMENT(t):
	r'set|[Aa]ssign|initiali[zs]e'
	print("<assign>",end="")
	# addToLine(("assign",t.value))
	setSemantics("assignment")
	#return t

def t_EQUALS(t):
	r'=|[eE]quals|to|as'
	print('= ',end ="")
	# addToLine(("=",t.value))
	setSemantics("assignment")
	#return t

def t_PRINT(t):
	r'[Pp]rint'
	print("<print>",end="")
	setSemantics("print")

def t_RETURN(t):
	r'[Rr]eturn'
	print("<return>",end="")
	setSemantics("return")
	addToLine(("return",t.value))

#Top level stuff
def t_FUNCTION(t):
	r'[Ff]unction'
	print("<function>",end ="")
	# addToLine(("function",t.value))
	setSemantics("function")
	#return t

def t_PROGRAM(t):
	r'[pP]rogram'
	# print("\ttoken:program:",t,"\n")
	print("<program>",end="")
	# addToLine(("program",t.value))
	setSemantics("program")
	#return t

def t_IF(t):
	r'[iI]f'
	print("<if>",end="")
	# addToLine(("if",t.value))
	setSemantics("if")

def t_ELSE(t):
	r'[Ee]lse'
	print("<else>",end="")
	addToLine(("else",t.value))
	setSemantics("else")


#Mid level Stuff

def t_BOOLOPERATOR(t):
	r'>=|<=|!=|<|>|='
	print("<boolOp>",end="")
	boolDict ={"<":"l",">":"g","==":"eq",\
				"<=":"le",">=":"ge"}
	addToLine(("boolOp",boolDict[t.value]))

def t_OPERATOR(t):
	r'\+|\-|\\|\*\*|\*'
	print("<operator>",end="")
	addToLine(("operator",t.value))
	#return t

def t_CONSTANT(t):
	r'[0-9]+(\.\d+){0,1}'
	print("<constant>",end="")
	addToLine(("constant",t.value))
	#return t

#Bottom level 
def t_STRING(t):
	r'[\"\“](\\.|[^"\\])*[\"\”]'
	print("<string>",end="")
	addToLine(("string",t.value))
	#return t

def t_IDENTIFIER(t):
	r'[a-zA-Z][0-9a-zA-Z_]*'
	# print("\ttoken:identifier",t,"\n")
	print("<identifier>",end ="")
	addToLine(("identifier",t.value))
	#return t

def t_OPENSQUARE(t):
	r'\['
	print("<OpenSquareOp>",end="")
	addToLine("OpenSquareOp",t.value)

def t_CLOSESQUARE(t):
	r'\]'
	print("<CloseSquareOp>",end="")
	addToLine("CloseSquareOp",t.value)

def t_OPENCURLY(t):
	r'\('
	print("<openOperator>",end=" ")
	addToLine(("OpenOperator",t.value))
	#return t

def t_CLOSECURLY(t):
	r'\)'
	print("<CloseOperator>",end="")
	addToLine(("CloseOperator",t.value))

def t_COMMA(t):
	r','
	print(",",end="")
	addToLine(("comma",t.value))

def t_NEWLINE(t):
	r'[\s\.\r]*\n'
	print(t.value,end="")
	addToTable()

def t_SPACES(t):
	r'\s'
	print(t.value,end="")

def t_UNKNOWN(t):
	r'.*[\(\)=+<]'
	print("$",t,end ="")
	# addToLine(t.value)
	return 

def t_error(t):
	print(t,"\tunaccounted for\n\n",t,"\n\n")

def intendChecker(line,intend_level):
	new_intend_level = 0
	for i in line:
		if i=='\t':
			new_intend_level+=1
		else:
			break
	print(new_intend_level,end=":")
	if new_intend_level > intend_level:
		print("\t"*(new_intend_level)+"<body>")
		# print(new_intend_level,end=":")
		# setSemantics("body")
		# addToLine(("Beg","body"))
		# addToTable()
	count = 0
	while (new_intend_level+count) < intend_level:
		print("\t"*(intend_level-count),"<done></done>")
		print("\t"*(intend_level-count),"</body>")
		# setSemantics("body")
		# addToLine(("End","body"))
		# addToTable()
		count+=1

	return new_intend_level

if __name__ == "__main__":
	lexer = lex.lex()
	with open("input.ini","r") as inputFile:
		# linebyline = inputFile.readlines()
		intend_level = 0
		jsonObj = list()
		for line in inputFile.readlines():
			lineSemantic = ""
			jsonLine = list()
			intend_level = intendChecker(line,intend_level)
			lexer.input(line)
			# print("\t"*intend_level,end="")
			# while tok:= lexer.token():
			# 	# json_file.append(tok.value)
			# 	pass
			while True: 
				tok = lexer.token()
				if tok:
					pass
				else:
					break
	with open("Table.json",'w') as table:
		json.dump(jsonObj,table,indent=4)
	
	print("\n\n","#"*10)
	for line in jsonObj:
		print(line)
	#	print(i)
