import xml.etree.ElementTree as ET

e_store = 0 				
v_store = 0					
p_value = 0
p_store = 0
a_store = 0
value_set  = 0
condition_set = 0
indendation_count = 0 
set_divisible = 0
list_set = 0
body_list = []
parent_list = []
expression_list = []
value_list = []


def RecPy(Tree):
	global e_store,v_store,condition_set,indendation_count,a_store,set_divisible
	global p_value,value_set,p_value,p_store,f_call_store,list_set
	type_val = 0
	children = list(Tree)     
	print(children)
	for child in children:

		if(child.tag == 'main'):
			f.write('if __name__ == "__main__":\n')
		
		elif(child.tag == 'expression'):
			e_store = int(children.index(child)==len(children)-1)	
			expression_list.insert(0,e_store)
			if(not(len(list(child)))):
				if(parent_list[0] == 'args' and expression_list[0]):
					f.write(')')
					parent_list.pop(0)
					expression_list.pop(0)
				if(len(parent_list) and parent_list[0] == 'list'):
					if(not(expression_list[0])):
						f.write(',')
						expression_list.pop(0)
					elif(expression_list[0]):
						f.write(']')
						parent_list.pop(0)
						expression_list.pop(0)
				if(len(parent_list) and (parent_list[0] == 'value' or parent_list[0] == 'if' or parent_list[0] == 'elif' or parent_list[0] == 'while') and not(expression_list)):
					if(value_list[0]):
						if(parent_list[0] == 'if' or parent_list[0] == 'elif' or parent_list[0] == 'while'):
							f.write(':')
						f.write('\n')
						parent_list.pop(0)
					value_list.pop(0)
				elif(not(len(parent_list)) and not(expression_list)):
					f.write('\n')



			
			
				


		elif(child.tag == 'variable'):
			v_store = int(children.index(child)==len(children)-1)
			assignment_value_check(int(children.index(child)==len(children)-1))	


		elif(child.tag == 'print'):
			p_store = int(children.index(child)==len(children)-1)
			parent_list.insert(0,"print")
			indent = "	" * indendation_count

			f.write(indent+'print(')
			p_value = 1
			
		elif(child.tag == 'assignment'):
			a_store = int(children.index(child)==len(children)-1)
			indent = "	" * indendation_count
			f.write(indent)
			
		elif(child.tag == 'value'):
			f.write(' = ')
			parent_list.insert(0,"value")
			value_set = 1
		
	
		elif(child.tag == 'function'):
			f.write('def ')
			condition_set = 1
		
		elif(child.tag == 'function_name'):
			f.write(child.text+'(')

		elif(child.tag == 'function_call'):
			assignment_value_check(int(children.index(child)==len(children)-1))
			

		elif(child.tag == 'if' or child.tag == 'elif' or child.tag == 'while'):
			parent_list.insert(0,child.tag)
			indent = "	" * indendation_count
			f.write(indent+child.tag+' ')
		elif(child.tag == 'else'):
			indent = "	" * indendation_count
			f.write(indent+'else:\n')

		elif(child.tag == 'condition'):
			condition_set = 1
		
		elif(child.tag == 'body'):
			indendation_count += 1
			body_list.insert(0,int(children.index(child)==len(children)-1))

		elif(child.tag == 'string'):
			f.write('"'+child.text+'"')
			assignment_value_check(int(children.index(child)==len(children)-1))
			setter(int(children.index(child)==len(children)-1))
		
		elif(child.tag == 'constant'):
			f.write(child.text)
			if(set_divisible):
				f.write(' == 0')
				set_divisible = 0
			assignment_value_check(int(children.index(child)==len(children)-1))
			setter(int(children.index(child)==len(children)-1))
		



		
		elif(child.tag == 'var_name'):
			f.write(child.text)
			if(not(int(children.index(child)==len(children)-1)) and children[children.index(child)+1].tag == "index"):
				f.write('['+children[children.index(child)+1].text+']')
			setter(v_store)
		

		elif(child.tag == 'break' or child.tag == 'continue'):
			f.write(child.tag+'\n')

		elif(child.tag == 'return'):
			f.write("	" * indendation_count+'return ')
			parent_list.insert(0,"return")

		elif(child.tag == 'operator'):
			if(child.text == 'eq'):
				f.write(' == ')
			elif(child.text == 'and' or child.text == 'or'):
				f.write(' '+child.text+' ')
			elif(child.text == 'g'):
				f.write(' > ')
			elif(child.text == 'ge'):
				f.write(' >= ')
			elif(child.text == 'l'):
				f.write(' < ')
			elif(child.text == 'le'):
				f.write(' <= ')
			elif(child.text == 'd'):
				f.write(' % ')
				set_divisible = 1
			else:
				f.write(child.text)
			assignment_value_check(int(children.index(child)==len(children)-1))
			setter(int(children.index(child)==len(children)-1))
		
		elif(child.tag == 'type'):
			f.write(child.text+'(')
			type_val = 1

		elif(child.tag == 'input'):
			f.write('input()')
			parent_list.pop(0)
			if(type_val):
				f.write(')')
				type_val = 0
			f.write('\n')
			value_set = 0				#input being the last tag in an assignment with input tag

		elif(child.tag == 'list'):
			f.write('[')
			parent_list.insert(0,"list")
			assignment_value_check(int(children.index(child)==len(children)-1))
			list_set = 1


		elif(child.tag == 'function_name'):
			f.write(child.text+'(')

		elif(child.tag == 'args'):
			parent_list.insert(0,"args")

		

		print(child.tag," ",indendation_count," ",p_store," ",body_list)
		print('\n')
		RecPy(child)

	
def setter(flag):
	global value_set,p_value,e_store,condition_set,p_store,a_store,f_call_store,list_set
	

	
	
	if(len(parent_list) and parent_list[0] == 'args'):
		if(expression_list[0] and flag):
			f.write(')')
			parent_list.pop(0)
			expression_list.pop(0)
			if(len(parent_list) == 0 and len(expression_list) == 0):
				if(condition_set):
					f.write(':')
					condition_set = 0
				f.write('\n') 
		elif(not(expression_list[0]) and flag):
			f.write(',')
			expression_list.pop(0)

	
	if(len(parent_list) and parent_list[0] == 'print'):
		if(expression_list[0] and flag):
			f.write(')\n')
			parent_list.pop(0)
			expression_list.pop(0)
			p_value = 0
			indendation_check(p_value,p_store)
		elif(not(expression_list[0]) and flag):
			f.write(',')
			expression_list.pop(0)

	if(len(parent_list) and parent_list[0] == 'list'):
		if(expression_list[0] and flag):
			f.write(']')
			parent_list.pop(0)
			expression_list.pop(0)
		elif(not(expression_list[0]) and flag):
			f.write(',')
			expression_list.pop(0)


	if(len(parent_list) and parent_list[0] == 'return'):
		if(expression_list[0] and flag):
			f.write('\n')
			indendation_check(0,1)
			parent_list.pop(0)
			expression_list.pop(0)
		elif(not(expression_list[0]) and flag):
			f.write(',')
			expression_list.pop(0)

	if(len(parent_list) and parent_list[0] == "value"):
		if(value_list[0]):
			parent_list.pop(0)
			value_set = 0
			indendation_check(value_set,a_store)
			f.write('\n')
		value_list.pop(0)

	if(len(parent_list) and (parent_list[0] == "if" or parent_list[0] == "elif" or parent_list[0] == "while")):
		if(value_list[0]):
			parent_list.pop(0)
			condition_set = 0
			f.write(':\n')
		value_list.pop(0)




		
def indendation_check(sets,flag):	
	global indendation_count
	if(not(sets) and len(body_list)):
		if(not(body_list[0]) and flag):
			indendation_count -= 1
			body_list.pop(0)
		elif(body_list[0] and flag):
			if(len(body_list) == 1):
				indendation_count -= 1
				body_list.pop(0)
				print("z")
			else:
				print("f")
				indendation_count -= 2
				body_list.pop(0)
				body_list.pop(0)

	
def assignment_value_check(flag):
	if(len(parent_list)):
		if((parent_list[0] == 'value' or parent_list[0] == 'list' or parent_list[0] == 'if' or parent_list[0] == 'elif' or parent_list[0] == 'while') and not(len(expression_list)) and not(len(value_list))):
			value_list.insert(0,flag)

	
file = "Final_XML.xml"
file = file.lstrip()
mytree = ET.parse(file)   
myroot = mytree.getroot()
f = open("final_output.txt","w")
RecPy(myroot)
