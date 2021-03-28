from Id import Id
from Core import Core

class Formals:
	
	def parse(self, parser):
		self.id = Id()
		self.id.parse(parser)
		if parser.scanner.currentToken() == Core.COMMA:
			parser.scanner.nextToken()
			self.list = Formals()
			self.list.parse(parser)
	
	def semantic(self, parser):
		#Fill in later
		return
	
	def print(self):
		self.id.print()
		if hasattr(self, 'list'):
			print(",", end='')
			self.list.print()

	def getListOfStrings(self):
		temp = []
		temp.append(self.id.getString())
		if hasattr(self, 'list'):
			return self.list.getListOfStringsHidden(temp)
		else:
			return temp

	def getListOfStringsHidden(self, temp):
		temp.append(self.id.getString())
		if hasattr(self, 'list'):
			return self.list.getListOfStringsHidden(temp)
		else:
			return temp

	def getListOfId(self):
		temp = []
		temp.append(self.id)
		if hasattr(self, 'list'):
			return self.list.getListOfIdHidden(temp)
		else:
			return temp

	def getListOfIdHidden(self, temp):
		temp.append(self.id)
		if hasattr(self, 'list'):
			return self.list.getListOfIdHidden(temp)
		else:
			return temp