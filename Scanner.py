from Core import Core

class Scanner:
  #some useful array constants defining delimiters and constants
  DELIMITING_CHARS = [',', ':', ';', '!', '+', '-', '*', '(', ')', '=', '<', '>', ' ', "\n", '\t', '\r']
  CONST_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

  # Initialize the scanner
  def __init__(self, filename):
    self.count = 0
    self.fileText = Scanner.importFile(filename)
    #build and array of all tokens as strings
    self.stringTokenArray = self.buildTokenArray()

  # Advance to the next token and return the current token
  def nextToken(self):
    tokenToReturn = self.currentToken()
    self.stringTokenArray.pop(0)
    return tokenToReturn

  # Return the current token as an enumerated type
  def currentToken(self):
    if len(self.stringTokenArray) > 0:
      currentTokenString = self.stringTokenArray[0]
      try:
        #raise exception for invalid token strings
        Scanner.validateTokenString(currentTokenString)
        return Scanner.determineToken(currentTokenString)
      except ScannerError as e:
          print(f'ERROR: {e.message}')
          return Core.EOF
    else:
      return Core.EOF

  # Return the token as a string for an identifier
  def getID(self):
    return self.stringTokenArray[0]

  #return the constant as an integer
  def getCONST(self):
    #raise exception for invalid const
    currentTokenString = self.stringTokenArray[0]
    try:
      Scanner.validateConst(currentTokenString)
      return int(currentTokenString)
    except ScannerError as e:
      print(f'ERROR: {e.message}')
      return Core.EOF

  ###  Helper functions

  # Given a filename, read in the entire file and return it as a string of text
  @staticmethod
  def importFile(filename):
    filestream = open(filename, 'r')
    fileText = filestream.read()
    filestream.close()
    return fileText

  # builds an array of tokens by advancing through self.fileText,
  # finding and enqueing a target token, and then updating the self.count variable to the next token
  # It ultimately returns an array of string tokens.
  def buildTokenArray(self):
    #file may start with white space - move the count to the first token
    stringTokenArray = []
    self.advanceCountPositionToNextToken(0)
    while self.count < len(self.fileText):
      stringTokenArray.append(self.parseNextTokenAndUpdateCount())
    return stringTokenArray

  # Finds the next token and returns it as a string. Also advances the Scanner's
  # count variable
  def parseNextTokenAndUpdateCount(self):
    nextTokenEndPos = Scanner.findTokenEnd(self.count, self.fileText)
    #signifies a token of length 1 - just return the char at the position
    if self.count == nextTokenEndPos:
      currentTokenString = self.fileText[nextTokenEndPos]
      nextTokenEndPos += 1
    else:
      currentTokenString = self.fileText[self.count:nextTokenEndPos]

    #move count forward
    self.advanceCountPositionToNextToken(nextTokenEndPos)
    return currentTokenString

  # given a count start position, advance the Scanner's counter to the next
  # token by skipping through the whitespace.
  def advanceCountPositionToNextToken(self, countStartPosition):
    self.count = countStartPosition
    fileLength = len(self.fileText)
    while self.count < fileLength and self.fileText[self.count] in [' ', "\n", '\t', '\r']:
      self.count += 1

  # Given a position representing the starting index of a token, and the corresponding string
  # to parse, find the end of that token in the string and return the end's index position
  @staticmethod
  def findTokenEnd(startingPos, parseString):
    isConstant = False
    #Edge case: check if starting position is on :, <, or >
    #If so, we'll need to check to see if the next character creates any
    # of the following tokens: :=, <=, or >
    if parseString[startingPos] in ['=', '<', '>'] and startingPos < len(parseString)-1:
      if parseString[startingPos + 1] == "=":
        return startingPos + 2
    # check if the char is a const for additional parsing logic downstream
    elif Scanner.isCharConst(parseString[startingPos]):
      isConstant = True

    index = startingPos
    while index < len(parseString):
      currentChar = parseString[index]
      # if the current token is identified as a constant and
      # the current index does not reference a constant character,
      # we have reached the end of the scanner
      if isConstant and not Scanner.isCharConst(parseString[index]):
        return index
      # return the index if we've found a delimiting char
      elif currentChar in Scanner.DELIMITING_CHARS:
        return index
      index += 1
    return index

  # checks if the character is a character
  @staticmethod
  def isCharConst(char):
    return char in Scanner.CONST_CHARS

  # A validation method that takes a general token string and ensures that it is valid.
  # It will return nothing, but if it finds an error it will throw an exception.
  @staticmethod
  def validateTokenString(str):
    #looks for lonely colons
    if str != ":=" and str.find(":") != -1:
      raise ScannerError(f'{str} is not valid')
    else:
      #iterate through each character in the string and ensure that it is a part of the language
      for char in str:
        if not Scanner.isCharInLanguage(char):
          raise ScannerError(f'{str} is not valid because one or more characters are not supported by the language. Cause: {char}')

  #given a char, return true if char is a delimiter, const, or an alphabetic character
  #AKA, the valid characters of the Core language
  @staticmethod
  def isCharInLanguage(char):
    return char in Scanner.DELIMITING_CHARS or char in Scanner.CONST_CHARS or Scanner.isCharAlphabetic(char)

  # by using ord to get the ascii value of a character, check if the character is in the range of
  # a through z, or A through Z
  @staticmethod
  def isCharAlphabetic(char):
    return (
      (ord("a") <= ord(char) and ord(char) <= ord("z"))
      or
      (ord("A") <= ord(char) and ord(char) <= ord("Z"))
    )

  #given a token string, return an enumerated value from the core language
  @staticmethod
  def determineToken(tokenString):
      if tokenString == "program":
        return Core.PROGRAM
      elif tokenString == "begin":
        return Core.BEGIN
      elif tokenString == "end":
        return Core.END
      elif tokenString == "new":
        return Core.NEW
      elif tokenString == "define":
        return Core.DEFINE
      elif tokenString == "extends":
        return Core.EXTENDS
      elif tokenString == "class":
        return Core.CLASS
      elif tokenString == "endclass":
        return Core.ENDCLASS
      elif tokenString == "int":
        return Core.INT
      elif tokenString == "endfunc":
        return Core.ENDFUNC
      elif tokenString == "if":
        return Core.IF
      elif tokenString == "then":
        return Core.THEN
      elif tokenString == "else":
        return Core.ELSE
      elif tokenString == "while":
        return Core.WHILE
      elif tokenString == "endwhile":
        return Core.ENDWHILE
      elif tokenString == "endfunc":
        return Core.ENDFUNC
      elif tokenString == "endif":
        return Core.ENDIF
      elif tokenString == ";":
        return Core.SEMICOLON
      elif tokenString == "(":
        return Core.LPAREN
      elif tokenString == ")":
        return Core.RPAREN
      elif tokenString == ",":
        return Core.COMMA
      elif tokenString == "=":
        return Core.ASSIGN
      elif tokenString == "!":
        return Core.NEGATION
      elif tokenString == "or":
        return Core.OR
      elif tokenString == "==":
        return Core.EQUAL
      elif tokenString == "<":
        return Core.LESS
      elif tokenString == "<=":
        return Core.LESSEQUAL
      elif tokenString == "+":
        return Core.ADD
      elif tokenString == "-":
        return Core.SUB
      elif tokenString == "*":
        return Core.MULT
      elif tokenString == "input":
        return Core.INPUT
      elif tokenString == "output":
        return Core.OUTPUT
      elif Scanner.isCharConst(tokenString[0]):
        #raise exception for invalid const
        try:
          Scanner.validateConst(tokenString)
          return Core.CONST
        except ScannerError as e:
          print(f'ERROR: {e.message}')
          return Core.EOF
      else:
        return Core.ID

  # validate that a constant does not start with 0 (unless the constant
  # is 0), and that it is within the range of 0 through 1023.
  # If validation succeeds, return constant as a string. Otherwise raise an
  # exception.
  @staticmethod
  def validateConst(constString):
    if constString[0] == "0" and len(constString) > 1:
      raise ScannerError(f"{constString} is not valid. A constant (which is not 0 itself) cannot begin with a 0")
    elif 1023 < int(constString):
      raise ScannerError(f'{constString} is not a valid constant (greater than 1023)')
    else:
      return constString

# A class used to throw scanner specific exceptions.
class ScannerError(Exception):
  def __init__(self, message):
    self.message = message