from compiler.lexer import Lexer
from compiler.notToken import *
from compiler.parser import Parser
from compiler.emitter import Emitter
import unittest

class testLexer(unittest.TestCase):
    def testEmpty(self):
        lexer = Lexer("")
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        self.assertEqual(enums_list, [TokenType.NEWLINE, TokenType.NEWLINE])

    def testPrintString(self):
        lexer = Lexer('PRINT "hello world!"')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser = [TokenType.PRINT, TokenType.STRING, TokenType.NEWLINE, TokenType.NEWLINE] 
        self.assertEqual(enums_list, awnser)

    def testPrintVariable(self):
        lexer = Lexer('PRINT variable')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.PRINT, TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)

    def testFloats(self):
        lexer = Lexer('1.string')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  []
        self.assertEqual(enums_list, awnser)

    def testIntegers(self):
        lexer = Lexer('1string')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  []
        self.assertEqual(enums_list, awnser)

    def testIDENT(self):
        lexer = Lexer('string123')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)


unittest.main()
