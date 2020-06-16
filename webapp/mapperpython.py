import xml.etree.ElementTree as ET

v_store = p_store = a_store =  0							#check the occurence of variable,print and assignment tag respectively			
condition_set = 0
indendation_count = 0 
set_prime = set_multiple_divisible = set_factor = 0      	#occurence of prime,multiple-divisble and factor operators 
body_list = []
parent_list = []
expression_list = []
value_list = []
condition_list = []
l_value = r_value = 0 
l_temp = r_temp = ""


def RecPy(Tree):
	'''
	Use -  For traversing through each tag depth wise
	Parmeters - Tree - child of the parent is passed			
	'''	
	global v_store,p_store,a_store
	global set_prime,set_multiple_divisible,set_factor
	global condition_set,indendation_count
	global l_value,r_value
	global l_temp,r_temp
	type_val = 0
	children = list(Tree)     
	# print(children)
	for child in children:

		if(child.tag == 'main'):
			f.write('if __name__ == "__main__":\n')
		
		elif(child.tag == 'expression'):
			store = int(children.index(child)==len(children)-1)	
			expression_list.insert(0,store)
			if(not(len(list(child)))):
				if(parent_list[0] == 'args' and expression_list[0]):
					if(parent_list[-1] in ('if','elif','while')):
						condition_list.append(')')
					else:
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
				if(len(parent_list) and parent_list[0] in ('value','if','elif','while') and not(expression_list)):
					if(value_list[0]):
						if(parent_list[0] in ('if','elif','while')):
							temp_string = "".join(condition_list)
							f.write(temp_string)
							del condition_list[:]
							condition_set = 0
							f.write(':')
						f.write('\n')
						parent_list.pop(0)
					value_list.pop(0)
				elif(not(len(parent_list)) and not(expression_list)):
					f.write('\n')
			
		elif(child.tag == 'variable'):
			v_store = int(children.index(child)==len(children)-1)
			assignment_value_check(v_store)	

		elif(child.tag == 'print'):
			p_store = int(children.index(child)==len(children)-1)
			parent_list.insert(0,"print")
			f.write("	" * indendation_count+'print(')
			
		elif(child.tag == 'assignment'):
			a_store = int(children.index(child)==len(children)-1)
			f.write("	" * indendation_count)
			
		elif(child.tag == 'value'):
			f.write(' = ')
			parent_list.insert(0,"value")
		
		elif(child.tag == 'function'):
			f.write('def ')
			condition_set = 1
		
		elif(child.tag == 'function_name'):
			if(len(parent_list) and (parent_list[-1] in ('if','elif','else'))):
				condition_list.append(child.text)
				condition_list.append('(')
			else:
				f.write(child.text+'(')

		elif(child.tag == 'function_call'):
			if(not(len(parent_list))):
				f.write("	" * indendation_count)
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
			store = int(children.index(child)==len(children)-1)
			if(len(parent_list) and parent_list[-1] in ('if','elif','while')):
				condition_list.append('"'+child.text+'"')
			else:
				f.write('"'+child.text+'"')
			assignment_value_check(store)
			setter(store)
		
		elif(child.tag == 'constant'):
			store = int(children.index(child)==len(children)-1)
			if(len(parent_list) and parent_list[-1] in ('if','elif','while')):
				condition_list.append(child.text)
			else:
				f.write(child.text)
			assignment_value_check(store)
			setter(store)
				
		elif(child.tag == 'var_name'):
			store = children.index(child)
			if(len(parent_list) and parent_list[-1] in ('if','elif','while')):
				condition_list.append(child.text)
			else:
				f.write(child.text)
			if(not(int(store == len(children)-1)) and children[store+1].tag == "index"):
				f.write('['+children[store+1].text+']')
			setter(v_store)
		

		elif(child.tag == 'break' or child.tag == 'continue'):
			f.write("	" * indendation_count+child.tag+'\n')
			indendation_check(0,1)

		elif(child.tag == 'return'):
			f.write("	" * indendation_count+'return ')
			parent_list.insert(0,"return")

		elif(child.tag == 'operator'):
			if(child.text == 'eq'):
				if(parent_list[-1] == 'if'):
					condition_list.append(' == ')
				else:
					f.write(' == ')
			elif(child.text == 'and' or child.text == 'or'):
				if (set_multiple_divisible):
					condition_list.append(' == ')
					condition_list.append(' 0 ')
					set_multiple_divisible = 0
				if(set_factor):
					if(l_value):
						for i in range(l_value+2,len(condition_list)):
							r_temp += condition_list[i]
						del condition_list[l_value+2:len(condition_list)]
						condition_list.insert(l_value+1,r_temp)
						condition_list.insert(len(condition_list),l_temp)
					elif(not(l_value)):
						for i in range(l_value+1,len(condition_list)):
							r_temp += condition_list[i]
						del condition_list[l_value+1:len(condition_list)]
						condition_list.insert(0,r_temp)
						condition_list.insert(l_value+2,l_temp)
					l_temp = ""
					r_temp = ""
					condition_list.append(' == ')
					condition_list.append(' 0 ')
					set_factor = 0
				if(parent_list[-1] in ('if','elif','while')):
					condition_list.append(' '+child.text+' ')
					r_value = len(condition_list)-1
					l_value = len(condition_list)-1
				else:
					f.write(' '+child.text+' ')
			elif(child.text == 'g'):
				if(parent_list[-1] in ('if','elif','while')):
					condition_list.append(' > ')
				else:
					f.write(' > ')
			elif(child.text == 'ge'):
				if(parent_list[-1] in ('if','elif','while')):
					condition_list.append(' >= ')
				else:
					f.write(' >= ')
			elif(child.text == 'l'):
				if(parent_list[-1] in ('if','elif','while')):
					condition_list.append(' < ')
				else:
					f.write(' < ')
			elif(child.text == 'le'):
				if(parent_list[-1] in ('if','elif','while')):
					condition_list.append(' <= ')
				else:
					f.write(' == ')
			elif(child.text == '#p'):
				if(l_value):
					for i in range(l_value+1,len(condition_list)):
						l_temp += condition_list[i]
					del condition_list[l_value+1:len(condition_list)]
				elif(not(l_value)):
					for i in range(l_value,len(condition_list)):
						l_temp += condition_list[i]
					del condition_list[l_value:len(condition_list)]
				condition_list.append('isPrime(')
				condition_list.append(l_temp)
				condition_list.append(')')
				l_temp = ""
				set_prime = 1
			elif(child.text == '#m' or child.text == 'd'):
				condition_list.append(' % ')
				set_multiple_divisible = 1
			elif(child.text == '#f'):
				condition_list.append(' % ')
				set_factor = 1
				if(l_value):
					for i in range(l_value+1,len(condition_list)-1):
						l_temp += condition_list[i]
					del condition_list[l_value+1:len(condition_list)-1]
				elif(not(l_value)):
					for i in range(0,len(condition_list)-1):
						l_temp += condition_list[i]
					del condition_list[0:len(condition_list)-1]
			else:
				if(parent_list[-1] in ('if','elif','while')):
					condition_list.append(child.text)
				else:
					f.write(child.text)
			store = int(children.index(child)==len(children)-1)
			assignment_value_check(store)
			setter(store)
		
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

		elif(child.tag == 'list'):
			f.write('[')
			parent_list.insert(0,"list")
			assignment_value_check(int(children.index(child)==len(children)-1))

		elif(child.tag == 'args'):
			parent_list.insert(0,"args")
		# print("c",condition_list,l_value,r_value)
		RecPy(child)


def setter(flag):
	'''
	Use -  To check if args,print,assignment,return has ended
	Parmeters - flag - obtained from string,constant,variable_name,operator
	'''
	global condition_set,p_store,a_store,r_value,set_multiple_divisible
	global set_factor,r_temp,l_value,l_temp

	if(len(parent_list) and parent_list[0] == 'args'):
		if(expression_list[0] and flag):
			if(parent_list[-1] in ('if','elif','while')):
				condition_list.append(')')
			else:
				f.write(')')
			parent_list.pop(0)
			expression_list.pop(0)
			if(len(parent_list) == 0 and len(expression_list) == 0):
				if(condition_set):
					f.write(':')
					condition_set = 0
				f.write('\n') 
		elif(not(expression_list[0]) and flag):
			if(parent_list[-1] == 'if'):
				condition_list.append(',')
			else:
				f.write(',')
			expression_list.pop(0)

	if(len(parent_list) and parent_list[0] == 'print'):
		explore_print_list_return('print',')',flag)

	if(len(parent_list) and parent_list[0] == 'list'):
		explore_print_list_return('list',']',flag)

	if(len(parent_list) and parent_list[0] == 'return'):
		explore_print_list_return('return','',flag)

	if(len(parent_list) and parent_list[0] == "value"):
		if(len(value_list)):
			if(value_list[0]):
				parent_list.pop(0)
				indendation_check(0,a_store)
				f.write('\n')
			value_list.pop(0)

	if(len(parent_list) and parent_list[0] in ("if","elif","while")):
		if(len(value_list)):
			if(value_list[0]):
				r_value = len(condition_list)
				if(set_factor):
					if(not(l_value)):
						for i in range(l_value+1,r_value):
							r_temp += condition_list[i]
						del condition_list[1:r_value]
						condition_list.insert(0,r_temp)
						condition_list.insert(r_value,l_temp)
					elif(l_value):
						for i in range(l_value+2,r_value):
							r_temp += condition_list[i]
						del condition_list[l_value+2:r_value]
						condition_list.insert(l_value+1,r_temp)
						condition_list.insert(r_value,l_temp)
					condition_list.insert(len(condition_list),' == ')
					condition_list.insert(len(condition_list),' 0 ')
					l_temp = ""
					r_temp = ""
					set_factor = 0
				if(set_multiple_divisible):
					condition_list.insert(r_value,' == ')
					condition_list.insert(len(condition_list),' 0 ')
					set_multiple_divisible = 0
				temp_string = "".join(condition_list)
				f.write(temp_string)
				del condition_list[:]
				parent_list.pop(0)
				condition_set = 0
				f.write(':\n')
			value_list.pop(0)

		
def indendation_check(sets,flag):
	'''
	Use -  Keeps check of indendation
	Parmeters - sets - to see if statement has ended
				flag - obtained from setter function for print,return,break,continue statements
	'''	
	global indendation_count
	if(not(sets) and len(body_list)):
		if(not(body_list[0]) and flag):
			indendation_count -= 1
			body_list.pop(0)
		elif(body_list[0] and flag):
			if(len(body_list) == 1):
				indendation_count -= 1
				body_list.pop(0)
			else:
				indendation_count -= 2
				body_list.pop(0)
				body_list.pop(0)

	

def assignment_value_check(flag):
	'''
	Use -  For adding on to value list if('value','list','if','elif','while') tags occur
	Parmeters - sets - to see if statement has ended
				flag - if the tag is the last element in the list
	'''	
	if(len(parent_list)):
		if(parent_list[0] in ('value','list','if','elif','while') and not(len(expression_list)) and not(len(value_list))):
			value_list.insert(0,flag)
		

def explore_print_list_return(tag,close,end_value):
	'''
	Use -  For checking if print,list or return statements have ended or not
	Parmeters - tag - to check if print,list,or return tag
				close - ),],'' for print,list or return tag
				end_value - if the tag is the last element in the list,obtained from setter function
	'''	
	global p_store
	if(expression_list[0] and end_value):
		f.write(close)
		if(tag == 'print' or tag == 'return'):
			f.write('\n')
		parent_list.pop(0)
		expression_list.pop(0)
		if(tag == 'print'):
			indendation_check(0,p_store)
		elif(tag =='return'):
			indendation_check(0,1)
	elif(not(expression_list[0]) and end_value):
		f.write(',')
		expression_list.pop(0)


	
file = "Final_XML.xml"
file = file.lstrip()
mytree = ET.parse(file)   
myroot = mytree.getroot()
f = open("final_output.txt","w")
RecPy(myroot)
f.close()
if(set_prime):
	set_prime = 0
	with open("./webapp/prime_function.txt", "r") as prime:
		with open("final_output.txt", "r+") as result:
			content = result.read()
			result.seek(0)
			result.write(prime.read())
			result.write('\n\n\n'+content)
