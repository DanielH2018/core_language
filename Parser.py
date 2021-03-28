from Scanner import Scanner
import sys

# Parser class contains all the persistent data structures we will need, and some helper functions
class Parser:
	
	#Constructor for Parser.
	#scanner is stored here so it is avaiable to the parse method of all contained classes
	#scopes is a data structure for the semantic checks performed after parsing
	def __init__(self, s):
		self.scanner = Scanner(s)
		self.scopes = [[]]
		self.funcNames = []
	
	#helper method for the semantic checks
	#returns true if the string x is the name of a variable that is in scope
	def nestedScopeCheck(self, x):
		match = False
		if not len(self.scopes) == 0:
			temp = self.scopes.pop()
			match = x in temp
			if not match:
				match = self.nestedScopeCheck(x)
			self.scopes.append(temp)
		return match
	
	#helper method for the semantic checks
	#returns true if the string x is the name of a variable that was declared in the current scope
	def currentScopeCheck(self, x):
		match = False
		if not len(self.scopes) ==0:
			match = x in self.scopes[-1]
		return match

	#helper method for the semantic checks
	#returns true if x is the name of a function that was declared
	def functionDeclaredCheck(self, x):
		return x in self.funcNames
	
	#helper method for handling error messages, used by the parse methods
	def expectedToken(self, expected):
		if self.scanner.currentToken() != expected:
			print("ERROR: Expected " + expected.name + ", recieved " + self.scanner.currentToken().name + "\n", end='')
			sys.exit()
