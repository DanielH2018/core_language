from Core import Core
from Id import Id

class NewDecl:

    def parse(self, parser):
        parser.expectedToken(Core.DEFINE)
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
        print("int ", end='')
        self.id.print()
        print(";\n", end='')

    def execute(self, executor):
        self.id.executeRefInit(executor)