#! /usr/bin/python
#---------------------------------------------------------------------------#
#- Beast - An Panda3d user interface library - See included "License.txt" - #
#---------------------------------------------------------------------------#
#- Beast, styleDocument.py parses a style document (syntaxually close to Cascading Style Sheets)
import string
import re

def parseVariableData(data):
	before = str(data)
	data = data.replace(' ', '').replace('\t', '').replace('\r', '').replace('\n', '')
	if data.endswith('px'): #- Pixels are converted just to ints (or floats) later on
		data = data[:-2]

	#- INT CHECK
	tmp = str(data)
	for c in string.digits:
		tmp = tmp.replace(c, '')
	if len(tmp) == 0:
		return int(data)

	#- FLOAT CHECK
	tmp = str(data)
	for c in string.digits + '.':
		tmp = tmp.replace(c, '')
	if len(tmp) == 0:
		return float(data)

	#- BOOL CHECK
	if data == 'true' or data == 'True':
		return True
	if data == 'false' or data == 'False':
		return False

	#- NULL CHECK
	if data == 'null' or data == 'NULL' or data == 'None' or data == 'none':
		return None

	#- Split things seperated by spaces
	tmp = before.strip(' ').strip('\t').replace('\r', '').replace('\n', '')
	if ' ' in tmp:
		ttmp = []
		for i in tmp.split(' '):
			if i:
				ttmp.append(i)
		return ttmp
	return before


variable_prog = re.compile(r'\s*([\w\s-]+?)\s*:\s*([\w\d\.\s]+?)\s*;') #- 
def parseVariables(data):
	variables = {}
	for variableName, variableData in variable_prog.findall(data):
		variables[variableName] = parseVariableData(variableData)
	return variables

class styleClass:
	def __init__(self, name, classData):
		self.__name = name.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
		self.__variables = parseVariables(classData)

	def setVariable(self, name, value):
		self.__variables[name] = value

	def getVariables(self):
		return self.__variables

	def getName(self):
		return self.__name

	def __str__(self):
		s = str()
		s += 'class %s\n' % self.__name
		for variableName, variableData in self.__variables.items():
			s += '    %s %s: %s\n' % (type(variableData), variableName, variableData)
		return s[:-1]

	def __repr__(self):
		return '<styleClass("%s") object at %s>' % (self.__name, hex(id(self)))

#- Cheezy, only supports one line comments..
def stripComments(data):
	ndata = str()
	for line in data.splitlines():
		if '//' in line:
			line = line[:line.index('//')]
		ndata += line + '\n'
	return ndata

section_prog = re.compile(r'\.*([\w\s:]+?){([\w\b\s\S\d]*?)}')
class styleDocument:
	def __init__(self):
		self.__classes = {}

	def getClassByName(self, name):
		if name in self.__classes:
			return self.__classes[name]
		else:
			return None

	def getClasses(self):
		return self.__classes.values()

	def append(self, data):
		if type(data) == file:
			data = data.read() #- Maybe work with file later instead of just reading
	#	print 'BEFORE', repr(data)
	#	print 'AFTER', repr(stripComments(data))
		data = stripComments(data)
		sections = section_prog.findall(data)
		for className, classData in sections:
		#	print 'STYLEDOCUMENT', repr(className)
			self.__classes[className] = styleClass(className, classData)

	def parseFile(self, filePath):
		if type(filePath) == str:
			filePath = open(filePath).read()
		self.parse(filePath)

	def parse(self, data):
		self.__classes = {}
		self.append(data)

	def __str__(self):
		s = str()
		if len(self.__classes.values()) == 0:
			return repr(self)
		for instance in self.__classes.values():
			s += str(instance) + '\n\n'
		return s[:-2]


if __name__ == '__main__':
	dom = styleDocument()
	"""
	dom.parse('''
	.[].{}}{}{}{}{{}{}.}{}{>}{>}.}{}{}{.{}{}{}diwjaodij29081 u398u#(@!*#
	.myclass{abc}
	.class{abd}
	.blanko{bacd}
	.abcdef{basdwasd}
	''')

	dom.parse('''
	.myclass{
		line1: 1;
		line2: 2.4;
		line3: true;
		line4: False;
	}

	// Code comments go in //'s only... NO /* */ multiline.. sorry
	//.myclass	abc{
		tdb: Hello jhonny cache;
	}

	.my_class_2 : hover{
		abc: 1;
	} // comment
	''')

	dom.parse(open('data/styleDocument.css'))
	"""
	dom.parseFile('data/styleDocument.css')

	print dom.getClasses()
	print dom
