from Term import Term
from Core import Core

class Expr:
	
	def parse(self, parser):
		self.option = 0
		self.term = Term()
		self.term.parse(parser)
		if parser.scanner.currentToken() == Core.ADD:
			self.option = 1
		elif parser.scanner.currentToken() == Core.SUB:
			self.option = 2
		if not self.option == 0:
			parser.scanner.nextToken()
			self.expr = Expr()
			self.expr.parse(parser)
	
	def semantic(self, parser):
		self.term.semantic(parser)
		if hasattr(self, 'expr'):
			self.expr.semantic(parser)
	
	def print(self):
		self.term.print()
		if self.option == 1:
			print("+", end='')
			self.expr.print()
		elif self.option == 2:
			print("-", end='')
			self.expr.print()

	#Returns the int value of the expression
	def execute(self, executor):
		result = self.term.execute(executor)
		if self.option == 1:
			result += self.expr.execute(executor)
		elif self.option == 2:
			result -= self.expr.execute(executor)
		return result