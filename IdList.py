from Id import Id
from Core import Core

class IdList:
	
	def parse(self, parser):
		self.id = Id()
		self.id.parse(parser)
		if parser.scanner.currentToken() == Core.COMMA:
			parser.scanner.nextToken()
			self.list = IdList()
			self.list.parse(parser)
	
	def semantic(self, parser):
		self.id.doublyDeclared(parser)
		self.id.addToScope(parser)
		if hasattr(self, 'list'):
			self.list.semantic(parser)
	
	def print(self):
		self.id.print()
		if hasattr(self, 'list'):
			print(",", end='')
			self.list.print()

	def execute(self, executor):
		self.id.executeAllocate(executor)
		if hasattr(self, 'list'):
			self.list.execute(executor)