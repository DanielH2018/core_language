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
		self.gc = 0



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
		for varDict in self.variables[-1]:
			if len(list(varDict.keys())) != 0:
				key = list(varDict.keys())[0]
				if isinstance(varDict.get(key), list):
					if varDict.get(key)[-1] != None:
						self.gc = self.gc - len(varDict.get(key))
						self.printGc()
		self.variables[-1].pop()

	#Called from Id class to handle assigning variables
	def varSet(self, x, inputValue):
		index = -1
		id = x

		if(isinstance(x, dict)):
			id = list(x.keys())[0]
			index = x.get(id)

		value = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if id in temp:
				if (isinstance(temp[id], list)):
					if isinstance(temp[id][index], dict):
						value = temp[id][index]
					else:
						temp[id][index] = inputValue
				else:
					temp[id] = inputValue
			else:
				self.varSet(x, inputValue)
			self.variables[-1].append(temp)
		else:
			self.globalVars[x] = inputValue
		if value != None:
			self.varSet(value, inputValue)
		


	#Called from Id class to handle fetching the value of a variable
	def varGet(self, x):
		index = -1
		id = x
		if(isinstance(x, dict)):
			id = list(x.keys())[0]
			index = x.get(id)

		value = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if id in temp:
				if isinstance(temp[id], list):
					value = temp[id][index]
				else:
					value = temp[id]
			else:
				value = self.varGet(x)
			self.variables[-1].append(temp)
		else:
			value = self.globalVars[id]
		if isinstance(value, dict):
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
					if len(temp[x]) == 1 and temp[x][-1] == None:
						temp[x][-1] = value
					else:
						temp[x].append(value)
					self.gc = self.gc + 1
					self.printGc()
			else:
				self.refVarSet(x, value)
			self.variables[-1].append(temp)

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
			
		return value - 1

	def isRefVar(self, x):
		isRefVar = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if x in temp:
				if isinstance(temp[x], list):
					isRefVar = True
				else:
					isRefVar = False
			else:
				isRefVar = self.isRefVar(x)
			self.variables[-1].append(temp)
		else:
			isRefVar = False
		return isRefVar


	def printGc(self):
		print("gc:" + str(self.gc))
	
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
		if(self.gc != 0):
			self.gc = 0
			self.printGc()

	#Called to push a new frame onto the call stack and pass parameters
	def pushFrame(self, formals, arguments):
		newFrame = [{}]
		for i in range(len(formals)):
			if self.isRefVar(arguments[i]):
				newFrame[-1][formals[i]] = [self.varGet(arguments[i])]
			else:
				newFrame[-1][formals[i]] = self.varGet(arguments[i])
		self.variables.append(newFrame)

	#Called to pop a frame off the call stack and pass back parameters
	def popFrame(self, formals, arguments):
		oldFrame = self.variables.pop()
		for i in range(len(formals)):
			if self.isRefVar(arguments[i]):
				self.varSet(arguments[i], oldFrame[-1][formals[i]][-1])
			else:
				self.varSet(arguments[i], oldFrame[-1][formals[i]])
		for i in range(len(formals)):
			if self.isRefVar(arguments[i]):
				self.garbageCollection(arguments[i])

	def garbageCollection(self, x):
		value = None
		if not len(self.variables[-1]) == 0:
			temp = self.variables[-1].pop()
			if x in temp:
				for key in temp:
					new = []
					if isinstance(temp.get(key), list):
						for key2 in temp:
							if isinstance(temp.get(key2), list):
								if(isinstance(temp.get(key2)[-1], dict)):
									refKey = list(temp.get(key2)[-1].keys())[0]
									if refKey == key:
										new.append(temp.get(key2)[-1].get(refKey))
										temp.get(key2)[-1].update({refKey: len(new)-1})
						new.append(temp.get(key)[-1])
						diff = len(temp.get(key)) - len(new)
						if diff != 0:
							self.gc = self.gc - diff
							self.printGc()
						elif len(new) == 1 and new[-1] == None:
							self.gc = self.gc - 1
							self.printGc()
						temp.update({key: new})
			else:
				self.garbageCollection(x)
			self.variables[-1].append(temp)
			
