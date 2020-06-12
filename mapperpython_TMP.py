
import xml.etree.ElementTree as ET

e_store = 0 				
v_store = 0					
p_value = 0
p_store = 0
assignment_set = 0
a_store = 0
value_set  = 0
condition_set = 0
indendation_count = 0 
body_list = []
parent_list = []
expression_list = []


def RecPy(Tree):
	global e_store,v_store,condition_set,indendation_count,a_store
	global p_value,assignment_set,value_set,p_value,p_store,f_call_store
	type_val = 0
	children = list(Tree)     
	print(children)
	for child in children:
		if(child.tag == 'expression'):
						
			e_store = int(children.index(child)==len(children)-1)	
			expression_list.insert(0,e_store)
			if(not(len(list(child)))):
				for i in range(len(parent_list)):
					f.write(')')
					parent_list.pop(0)
					expression_list.pop(0)
				f.write('\n')


		elif(child.tag == 'variable'):
			v_store = int(children.index(child)==len(children)-1)	

		elif(child.tag == 'print'):
			p_store = int(children.index(child)==len(children)-1)
			parent_list.insert(0,"print")
			for i in range(0,indendation_count):
				f.write('	')
			f.write('print(')
			p_value = 1
			
		elif(child.tag == 'assignment'):
			a_store = int(children.index(child)==len(children)-1)
			for i in range(0,indendation_count):
				f.write('	')
			assignment_set = 1
			
		elif(child.tag == 'value'):
			value_set = 1
		
	
			
		
		elif(child.tag == 'function_name'):
			f.write(child.text+'(')

		elif(child.tag == 'function_call'):
			if(value_set):
				f_call_store = int(children.index(child)==len(children)-1)

		elif(child.tag == 'if' or child.tag == 'elif' or child.tag == 'while'):
			for i in range(0,indendation_count):
				f.write('	')
			f.write(child.tag+' ')
		elif(child.tag == 'else'):
			for i in range(0,indendation_count):
				f.write('	')
			f.write('else:\n')

		elif(child.tag == 'condition'):
			condition_set = 1
		
		elif(child.tag == 'body'):
			indendation_count += 1
			body_list.insert(0,int(children.index(child)==len(children)-1))

		elif(child.tag == 'string'):
			f.write('"'+child.text+'"')
			setter(int(children.index(child)==len(children)-1))
		
		elif(child.tag == 'constant'):
			f.write(child.text)
			setter(int(children.index(child)==len(children)-1))
		



		
		elif(child.tag == 'var_name'):
			f.write(child.text)
			if(assignment_set):
				f.write(' = ')
				assignment_set = 0
			setter(v_store)
			
			
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
			else:
				f.write(child.text)
			setter(int(children.index(child)==len(children)-1))
		
		elif(child.tag == 'type'):
			f.write(child.text+'(')
			type_val = 1

		elif(child.tag == 'input'):
			f.write('input()')
			if(type_val):
				f.write(')')
				type_val = 0
			f.write('\n')
			value_set = 0				#input being the last tag in an assignment with input tag


		elif(child.tag == 'function_name'):
			f.write(child.text+'(')

		elif(child.tag == 'args'):
			parent_list.insert(0,"args")

		print(child.tag," ",indendation_count," ",p_store," ",body_list)
		print('\n')
		RecPy(child)

	
def setter(flag):
	global value_set,p_value,e_store,condition_set,p_store,a_store,f_call_store
	
	
	if(len(parent_list) and parent_list[0] == 'args'):
		if(expression_list[0] and flag):
			f.write(')')
			parent_list.pop(0)
			expression_list.pop(0)
			if(len(parent_list) == 0 and len(expression_list) == 0):
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
	

	if(value_set):
		if(flag):
			f.write('\n')
			value_set = 0				# check if assignment ends
			indendation_check(value_set,a_store)
		


	if(condition_set and flag): 		
		f.write(':\n')
		condition_set = 0				# if condition ends


		
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

	
file = "Final.xml"
file = file.lstrip()
mytree = ET.parse(file)   
myroot = mytree.getroot()
f = open("final_python.txt","w")
RecPy(myroot)

