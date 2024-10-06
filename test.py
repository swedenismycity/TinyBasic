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
        awnser = [TokenType.NEWLINE] 
        self.assertEqual(enums_list, awnser)

    def testPrintString(self):
        lexer = Lexer('PRINT "hello world!"')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser = [TokenType.PRINT, TokenType.STRING, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)

    def testPrintVariable(self):
        lexer = Lexer('PRINT variable')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.PRINT, TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)

    def testFloats(self):
        lexer = Lexer('1.string')
        self.assertRaises(ValueError, lexer.getTokens)

    def testIntegers(self):
        lexer = Lexer('1string')
        self.assertRaises(ValueError, lexer.getTokens)

    def testIDENT(self):
        lexer = Lexer('ident123')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser, "Types must match")

    def testString(self):
        lexer = Lexer('"string123"')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.STRING, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser, "Types must match")
        self.assertEqual(tokens[0].value, "string123", "Input must match Token.value")

    def testNotIDENT(self):
        lexer = Lexer('!ident')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.NOT, TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)

    def testSpacing(self):
        lexer = Lexer('WHILEsdf')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)

    def testKeyWord(self):
        lexer = Lexer('WHILE')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.WHILE, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser)

    def testEQWithoutSpaces(self):
        lexer = Lexer('a=b')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.IDENT, TokenType.EQ, TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser, "a=b")
        
    def testEQWithSpaces(self):
        lexer = Lexer('a = b')
        tokens = lexer.getTokens()
        enums_list = [token.type for token in tokens]
        awnser =  [TokenType.IDENT, TokenType.EQ, TokenType.IDENT, TokenType.NEWLINE]
        self.assertEqual(enums_list, awnser, "a = b")



unittest.main()
