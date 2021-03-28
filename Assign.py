from Id import Id
from Expr import Expr
from Core import Core

class Assign:
	
	def parse(self, parser):
		self.id = Id()
		self.id.parse(parser)
		parser.expectedToken(Core.ASSIGN)
		parser.scanner.nextToken()
		if parser.scanner.currentToken() == Core.NEW:
			self.new = True
			parser.scanner.nextToken()
			self.expr = Expr()
			self.expr.parse(parser)
		elif parser.scanner.currentToken() == Core.DEFINE:
			parser.scanner.nextToken()
			self.assignId = Id()
			self.assignId.parse(parser)
		else:
			self.expr = Expr()
			self.expr.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.id.semantic(parser)
		if hasattr(self, 'expr'):
			self.expr.semantic(parser)
		else:
			self.assignId.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		self.id.print()
		print("=", end='')
		self.expr.print()
		print(";\n", end='')

	def execute(self, executor):
		if hasattr(self, 'assignId'):
			self.id.executeRefAssign(self, executor)
		elif hasattr(self, 'new'):
			self.id.executeRefInit(self, executor)
		else:
			self.id.executeAssign(executor, self.expr.execute(executor))