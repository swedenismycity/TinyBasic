from compiler.lexer import Lexer
from compiler.notToken import *
from compiler.parser import Parser
from compiler.emitter import Emitter

source = open('basicFile.txt', 'r').read()

lexer = Lexer(source)
emitter = Emitter('out.c')
parser = Parser(lexer, emitter)
parser.parseProgram()
emitter.writeFile()
