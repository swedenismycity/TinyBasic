from tinybasic.lexer import Lexer
from tinybasic.notToken import *
from tinybasic.parser import Parser
from tinybasic.emitter import Emitter

source = open('basicFile.txt', 'r').read()

lexer = Lexer(source)
emitter = Emitter('out.c')
parser = Parser(lexer, emitter)
parser.parseProgram()
emitter.writeFile()
