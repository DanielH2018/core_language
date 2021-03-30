from Scanner import Scanner
import sys

# Parser class contains all the persistent data structures we will need, and some helper functions
class Executor:
	
	#Constructor for Executor.
	def __init__(self, s):
		self.scanner = Scanner(s)
		self.variables = []
		self.globalVars = {}
		self.funcMap = {}
	



	#
	#
	# These are the helper functions to handle variables
	# self.globalVars is a data structure to store the global variable values
	# self.variables represents the call stack
	#
	#

	#Push a nested scope onto the current frame, handles new nestes scope for If or Loop statements
	def pushScope(self):
		self.variables[-1].append({})

	#Pop a nested scope off of the current frame
	def popScope(self):
		self.variables[-1].pop()

	#Called from Id class to handle assigning variables
	def varSet(self, x, inputValue):
		index = -1
		id = None
		if(isinstance(x, dict)):
			id = list(x.keys())[0]
			index = x.get(id)
		else:
			id = x

		value = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if x in temp:
					if (isinstance(int, temp[id][index])):
						temp[id][index] = inputValue
					else:
						value = temp[id][index]
			else:
				self.varSet(x, inputValue)
			self.variables[-1].append(temp)
		if value != None:
			self.varSet(value, inputValue)

	#Called from Id class to handle fetching the value of a variable
	def varGet(self, x):
		index = -1
		id = None
		if(isinstance(x, dict)):
			id = list(x.keys())[0]
			index = x.get(id)
		else:
			id = x

		value = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if id in temp:
				if(isinstance(x, dict)):
					value = temp[id][index]
				else:
					value = temp[x]
			else:
				value = self.varGet(x)
			self.variables[-1].append(temp)
			
		if not isinstance(value, int):
			value = self.varGet(value)
		return value
	
	#Called from Id class to handle declaring a variable
	def varInit(self, x):
		#Put None here so we can tell later if variable is uninitialized
		if len(self.variables) == 0:
			self.globalVars[x] = None
		else:
			self.variables[-1][-1][x] = None
	
	# Called from Id class to declare a reference variable
	def refVarInit(self, x):
		self.variables[-1][-1][x] = [None]

	# Called from Id Class when 'id = new <expr>'
	def refVarSet(self, x, value):
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if x in temp:
					temp[x].append(value)
			else:
				self.refVarSet(x, value)
			self.variables[-1].append(temp)
		else:
			self.globalVars[x] = value

	# Called from Id Class when 'id = define id'
	def refVarListLength(self, x):
		value = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if x in temp:
				value = len(temp[x])
			else:
				value = self.refVarListLength(x)
			self.variables[-1].append(temp)
			
		return value
	
	#
	#
	# These are the helper functions to handle funciton calls
	# self.funcMap associates function names with defintiion, used in FuncDecl and FunCall
	#
	#

	#Called from FuncDecl to add function definition to funcMap
	def registerFunction(self, id, temp):
		self.funcMap[id.getString()] = temp

	#Called from FuncCall to retrieve definition of called function
	def retrieveFunction(self, id):
		return self.funcMap[id.getString()]

	


	#
	#
	# These are the helper fucntions to handle mainting the call stack self.variables
	#
	#

	#Called to push a new frame onto the call stack without parameter passing
	def pushMainFrame(self):
		self.variables.append([{}])

	#Called to pop a frame off the call stack without parameter passing
	def popMainFrame(self):
		self.variables.pop()

	#Called to push a new frame onto the call stack and pass parameters
	def pushFrame(self, formals, arguments):
		newFrame = [{}]
		for i in range(len(formals)):
			newFrame[-1][formals[i]] = self.varGet(arguments[i])
		self.variables.append(newFrame)

	#Called to pop a frame off the call stack and pass back parameters
	def popFrame(self, formals, arguments):
		oldFrame = self.variables.pop()
		for i in range(len(formals)):
			self.varSet(arguments[i], oldFrame[-1][formals[i]])