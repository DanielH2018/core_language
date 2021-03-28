from Parser import Parser
from Executor import Executor
from Program import Program

import sys

def main():
  # Initialize the parser object (contains the scanner and some helper functions)
  parser = Parser(sys.argv[1])
  # Initialize the executor object (contains scanner with the data file and some helper functions)
  executor = Executor(sys.argv[2])

  p = Program()
  p.parse(parser)
  p.semantic(parser)
  #p.print()
  p.execute(executor)


if __name__ == "__main__":
    main()