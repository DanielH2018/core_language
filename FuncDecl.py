from Formals import Formals
from StmtSeq import StmtSeq
from Id import Id
from Core import Core
import sys

class FuncDecl:
	
	def parse(self, parser):
		parser.expectedToken(Core.ID)
		self.name = Id()
		self.name.parse(parser)
		parser.expectedToken(Core.LPAREN)
		parser.scanner.nextToken()
		self.list = Formals()
		self.list.parse(parser)
		parser.expectedToken(Core.RPAREN)
		parser.scanner.nextToken()
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.body = StmtSeq()
		self.body.parse(parser)
		parser.expectedToken(Core.ENDFUNC)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		if parser.functionDeclaredCheck(self.name.getString()):
			#Function name has already been used, print error msg
			print("ERROR: function " + self.name.getString() + " declared twice!\n", end='')
			sys.exit()
		parser.funcNames.append(self.name.getString())
		formals = self.list.getListOfStrings()
		if len(formals) != len(set(formals)):
			print("ERROR: function " + self.name.getString() + " has duplicate formal parameters!\n", end='')
			sys.exit()
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		self.name.print()
		print("(", end='')
		self.list.print()
		print(") begin\n", end='')
		self.body.print(indent+1)
		print("endfunc\n", end='')

	def execute(self, executor):
		executor.registerFunction(self.name, self)

	def getFormalParametersList(self):
		return self.list.getListOfStrings()

	def getBody(self):
		return self.body