from Id import Id
from Expr import Expr
from Core import Core

class Assign:
	
	def parse(self, parser):
		self.id = Id()
		self.id.parse(parser)
		parser.expectedToken(Core.ASSIGN)
		parser.scanner.nextToken()
		self.expr = Expr()
		self.expr.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.id.semantic(parser)
		self.expr.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		self.id.print()
		print("=", end='')
		self.expr.print()
		print(";\n", end='')

	def execute(self, executor):
		self.id.executeAssign(executor, self.expr.execute(executor))