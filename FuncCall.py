from Id import Id
from Core import Core
from Formals import Formals
import sys

class FuncCall:
	
	def parse(self, parser):
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		parser.expectedToken(Core.ID)
		self.name = Id()
		self.name.parse(parser)
		parser.expectedToken(Core.LPAREN)
		parser.scanner.nextToken()
		self.list = Formals()
		self.list.parse(parser)
		parser.expectedToken(Core.RPAREN)
		parser.scanner.nextToken()
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		if not parser.functionDeclaredCheck(self.name.getString()):
			print("ERROR: calling function " + self.name.getString() + " function is not declared!\n", end='')
			sys.exit()
		arguments = self.list.getListOfId()
		for test in arguments:
			test.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("begin ", end='')
		self.name.print()
		print("(", end='')
		self.list.print()
		print(");\n", end='')

	def execute(self, executor):
		definition = executor.retrieveFunction(self.name)
		formalParameters = definition.getFormalParametersList()
		actualParameters = self.list.getListOfStrings()
		if not len(formalParameters) == len(actualParameters):
			print("ERROR: Number of formal parameters does not match number of actual parameters!\n", end='')
			sys.exit()
		executor.pushFrame(formalParameters, actualParameters)
		definition.getBody().execute(executor)
		executor.popFrame(formalParameters, actualParameters)