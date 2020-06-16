import ply.lex as lex
import json

def addToLine(tagPair):
	global jsonLine
	jsonLine.append(tagPair)

def setSemantics(semantic):
	global lineSemantic
	if lineSemantic == "":
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

tokens = ("MAIN","VAR","DECLARE_FILTER","WHILE","TYPE","INPUT","INCREMENT","DECREMENT","ISGEQ","ISGREATER","ISLEQ","ISLESSER","ISDIVISIBLE","ISMULTIPLE","ISPRIME","ISFACTOR",\
		"LIST_ASSIGNMENT","L_EQUAL_ASSIGN","WITH_VALUES","ASSIGNMENT","PRINT","RETURN","FUNCTION","FUNCTIONCALL","PROGRAM","IF","ELSEIF","ELSE","EQUAL","BOOLSTRINGS","BOOLOPERATOR",\
			"OPERATOR","CONSTANT","STRING","IDENTIFIERS","OPENSQUARE","CLOSESQUARE","OPENCURLY","CLOSECURLY","COMMA",\
				"NEWLINE","SPACES","UNKNOWN") 
#Direct Replacemet

def t_MAIN(t):
	r'[(function)|(program)]+\s+[mM]ain[(\(\))]*'
	print("<main>")
	setSemantics("main")
	addToLine(("main","main"))

def t_VAR(t):
	r'[vV]ariable|of'
	print("",end="")

def t_DECLARE_FILTER(t):
	r'([Dd]eclare.*|(int|float|char|double|long).*)'
	print("ignored")

def t_BREAK(t):
	r'[Bb]reak'
	setSemantics("UnconditionalControl")
	addToLine(("break","break"))

def t_CONTINUE(t):
	r'[cC]ontinue'
	setSemantics("UnconditionalControl")
	addToLine(("continue","continue"))

def t_WHILE(t):
	r'while'
	print("<while>",end="")
	setSemantics("while")

def t_TYPE(t):
	r'type\s+[a-z]+'
	print("<type>",end="")
	addToLine(("type",t.value.split()[1]))

def t_INPUT(t):
	r'with\s+input[(\s+taken)]*\s+from\suser'
	print("<input>")
	addToLine(("input",t.value))

def t_INCREMENT(t):
	r'[Ii]ncrement\s+[a-zA-Z][0-9a-zA-Z_]*\s+by'
	print("<UniqueAssignment><identifier>")
	setSemantics("UAssignment")
	_,var,_=t.value.split()
	addToLine(("identifier",var))
	addToLine(("operator","+"))

def t_DECREMENT(t):
	r'[Dd]ecrement\s+[a-zA-Z][0-9a-zA-Z_]*\s+by'
	print("<UniqueAssignment><identifier>")
	setSemantics("UAssignment")
	_,var,_= t.value.split()
	addToLine(("identifier",var))
	addToLine(("operator","-"))

def t_UASSIGNEMNT(t):
	r'\+=|\-=|\*=|/=|%='
	setSemantics("UAssignment")
	print("<Uoperator>",end="")
	addToLine(("operator",t.value[0]))

def t_SIEQUAL(t):
	r'is\s+equal\s+to'
	print("<BoolOp>",end="")
	addToLine(("boolOp","eq"))

def t_ISGEQ(t):
	r'is\s+greater\s+than\sor\sequal\s+to'
	print("<BoolOp>",end="")
	addToLine(("boolOp","ge"))

def t_ISGREATER(t):
	r'is\s+[gG]reater\s+than'
	print("<boolOp>",end="")
	addToLine(("boolOp","g"))

def t_ISLEQ(t):
	r'is\s+[lL]ess[er]*\s+than\s+or\s+equal\s+to'
	print("<boolOp>",end="")
	addToLine(("boolOp","le"))

def t_ISLESSER(t):
	r'is\s+[lL]ess[er]*\s+than'
	print("<boolOp>",end="")
	addToLine(("boolOp","l"))

def t_ISDIVISIBLE(t):
	r'is\s+divisible\s+by'
	print("<boolStr>",end="")
	addToLine(("boolStr","d"))

def t_ISMULTIPLE(d):
	r'is\s+a\s+multiple\s+of'
	print("<boolStr>",end="")
	addToLine(("boolStr","#m"))

def t_ISPRIME(t):
	r'is\s+prime'
	print("<boolStr>",end="")
	addToLine(("boolStr","#p"))

def t_ISFACTOR(t):
	r'is\s+a\s+factor\s+of'
	print("<boolStr>",end="")
	addToLine(("boolStr","#f"))

def t_LIST_ASSIGNMENT(t):
	r'(set|[Aa]ssign|initiali[zs]e|accept)\s*a\s*list'
	print("<assignment><list>")
	setSemantics("L_assignment")

def t_L_EQUAL_ASSIGN(t):
	r'[a-zA-Z0-9][a-zA-Z0-9]*\s*=\s*\['
	print("<assignment><list>")
	addToLine(("list_name",t.value.split("=")[0].rstrip().lstrip()))
	setSemantics("L_assignment")

def t_WITH_VAUES(t):
	r'with\svalues?'
	print("<values|",end ="")
	# ip = t.value.split()[2:]
	# addToLine(("values"))

def t_ASSIGNMENT(t):
	r'set|[Aa]ssign|initiali[zs]e|accept'
	print("<assign>",end="")
	# addToLine(("assign",t.value))
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
	# addToLine(("return",t.value))

#Top level stuff

def t_FUNCTION(t):
	r'(?:[cC]reate\sa)?\s*function\s*[a-zA-Z][a-zA-Z0-9_]*\('
	ip = t.value[:-1]
	print("<function>")
	setSemantics("function")
	ip = ip.split("(")
	fname = ip[0].split()[-1]
	# args = ip[1].split(",")
	addToLine(("Function_name",fname))
	# addToLine(("Arguments_list",args))

def t_FUNCTIONCALL(t):
	r'([cC]all\s[fF]unction)?\s*[a-zA-Z][0-9a-zA-Z_]*\('
	print("<function_call>",end ="")
	ip = t.value[:-1]
	fname = ip.split()[-1]
	addToLine(("function_call",fname))
	setSemantics("function_call")
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

def t_ELIF(t):
	r'([Ee]lse\s+[Ii]f|[eE]lif)'
	print("<elif>",end="")
	setSemantics("elif")
	
def t_ELSE(t):
	r'[Ee]lse:?'
	print("<else>",end="")
	addToLine(("else",t.value))
	setSemantics("else")


#Mid level Stuff

def t_BOOLOPERATOR(t):
	r'>=|<=|!=|<|>|==|[Ee]quals|[aA]nd|[oO]r|[Nn]ot\s+equal\s+to|[Nn]ot'
	print("<boolOp>",end="")
	boolDict ={"<":"l",">":"g","==":"eq","!=":"!=",\
				"equals":"eq","<=":"le",">=":"ge",\
				"and":"and","or":"or","not equal to":"!=","not":"!="}
	addToLine(("boolOp",boolDict[t.value.lower()]))

def t_EQUAL(t):
	r'=|to|as'
	print('= ',end ="")
	# addToLine(("=",t.value))
	setSemantics("assignment")
	#return t

def t_OPERATOR(t):
	r'\+\+|\-\-|\+|\-|/|\*\*|\*|%'
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
	# r'[\"\“](\\.|[^"\\|[^”])*["|”]'
	r'([\"\“])(.|[^"“”])*[\0”"]'
	print("<string>",end="")
	addToLine(("string",t.value[1:-1])) # decide if quotes are needed

def t_IDENTIFIER(t):
	r'[a-zA-Z][0-9a-zA-Z_]*'
	# print("\ttoken:identifier",t,"\n")
	print("<identifier>",end ="")
	addToLine(("identifier",t.value))
	#return t

def t_OPENSQUARE(t):
	r'\['
	print("<OpenSquareOp>",end="")
	addToLine(("OpenSquareOp",t.value))

def t_CLOSESQUARE(t):
	r'\]'
	print("<CloseSquareOp>",end="")
	addToLine(("CloseSquareOp",t.value))

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
	r'.*[:\(\)=+<]'
	# print("$",t,end ="")
	print("")
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

	count = 0
	while (new_intend_level+count) < intend_level:
		# print("\t"*(intend_level-count),"<done></done>")
		print("\t"*(intend_level-count),"</body>")
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
			while tok:= lexer.token():
				# json_file.append(tok.value)
				pass
	with open("Table.json",'w') as table:
		json.dump(jsonObj,table,indent=4)
	
	print("\n\n","#"*10)
	for line in jsonObj:
		print(line)
	#	print(i)