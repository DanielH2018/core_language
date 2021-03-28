from Id import Id
from Core import Core
import sys

class Input:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.id = Id()
		self.id.parse(parser)
		parser.expectedToken(Core.SEMICOLON)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.id.semantic(parser)
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("input ", end='')
		self.id.print()
		print(";\n", end='')

	def execute(self, executor):
		if executor.scanner.currentToken() == Core.CONST:
			self.id.executeAssign(executor, executor.scanner.getCONST())
			executor.scanner.nextToken()
		else:
			print("ERROR: Data file out of values!\n", end='')
			sys.exit()