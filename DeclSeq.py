from Decl import Decl
from Core import Core
from FuncDecl import FuncDecl

class DeclSeq:
	
	def parse(self, parser):
		if parser.scanner.currentToken() == Core.INT:
			self.decl = Decl()
			self.decl.parse(parser)
		else:
			self.function = FuncDecl()
			self.function.parse(parser)
		if not parser.scanner.currentToken() == Core.BEGIN:
			self.ds = DeclSeq()
			self.ds.parse(parser)
	
	def semantic(self, parser):
		if hasattr(self, 'decl'):
			self.decl.semantic(parser)
		else:
			self.function.semantic(parser)
		if hasattr(self, 'ds'):
			self.ds.semantic(parser)
	
	def print(self, indent):
		if hasattr(self, 'decl'):
			self.decl.print(indent)
		else:
			self.function.print(indent)
		if hasattr(self, 'ds'):
			self.ds.print(indent)

	def execute(self, executor):
		if hasattr(self, 'decl'):
			self.decl.execute(executor)
		else:
			self.function.execute(executor)
		if hasattr(self, 'ds'):
			self.ds.execute(executor)