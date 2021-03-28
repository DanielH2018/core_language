from Core import Core
import sys

class Id:
	
	def parse(self, parser):
		parser.expectedToken(Core.ID)
		self.identifier = parser.scanner.getID()
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		if not parser.nestedScopeCheck(self.identifier):
			print("ERROR: No matching declaration found: " + self.identifier + "\n", end='')
			sys.exit()
	
	#Called by Decl.semantic to add the variable to the scopes data structure
	def addToScope(self, parser):
		parser.scopes[-1].append(self.identifier)
	
	#Called by Decl.semantic to check for doubly declared variables
	def doublyDeclared(self, parser):
		if parser.currentScopeCheck(self.identifier):
			print("ERROR: Doubly declared variable detected: " + self.identifier + "\n", end='')
			sys.exit()
	
	def print(self):
		print(self.identifier, end='')

	#Called by IdList.execute
	def executeAllocate(self, executor):
		executor.varInit(self.identifier)

	#Called by Assign.execute and Input.execute
	def executeAssign(self, executor, value):
		executor.varSet(self.identifier, value)

	#Called by Factor.execute
	def executeValue(self, executor):
		value = executor.varGet(self.identifier)
		#This is where we catch ininitialzed variables
		if value is None:
			print("Error: Using uninitialized variable " + self.identifier + "\n", end='')
			sys.exit()
		return value

	# Point self to reference variable
	def executeRefInit(self, executor):
		pass

	# Initialize reference variable
	def executeRefAssign(self, executor):
		pass

	def getString(self):
		return self.identifier