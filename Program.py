from Core import Core
from DeclSeq import DeclSeq
from StmtSeq import StmtSeq

class Program:
	
	def parse(self, parser):
		parser.expectedToken(Core.PROGRAM)
		parser.scanner.nextToken()
		if parser.scanner.currentToken() != Core.BEGIN:
			self.ds = DeclSeq()
			self.ds.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.END)
		parser.scanner.nextToken()
		parser.expectedToken(Core.EOF)
	
	def semantic(self, parser):
		parser.funcNames = []
		parser.scopes.append([])
		if hasattr(self, 'ds'):
			self.ds.semantic(parser)
		parser.scopes.append([])
		self.ss.semantic(parser)
		parser.scopes.pop()
	
	def print(self):
		print("program\n", end='')
		self.ds.print(1)
		print("begin\n", end='')
		self.ss.print(1)
		print("end\n", end='')

	def execute(self, executor):
		if hasattr(self, 'ds'):
			self.ds.execute(executor)
		#Add a frame for the local scope
		executor.pushMainFrame()
		self.ss.execute(executor)
		executor.popMainFrame()