from tinybasic.notToken import *
import sys
class Lexer:
    def __init__(self, input):
        #self.tokens = []
        self.string = input + '\n'
        self.curChar = ''
        self.curPos = -1
        self.step()

    def peek(self):
        if self.curPos + 1 >= len(self.string):
            return '\0'
        return self.string[self.curPos + 1]
        
    def step(self):
        self.curPos += 1
        if self.curPos >= len(self.string):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.string[self.curPos]

    def previous(self):
        pass

    def removeWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\r' or self.curChar == '\t':
            self.step()

    def abort(self, message):
        import unittest
        raise ValueError("Lexing error. " + message)
        #sys.exit("Lexing error. " + message)
        
    def getToken(self):
        #--------------OPS---------------#
        if self.curChar == '+':
            if self.peek() == '=':
                token = Token('+=', TokenType.PLUSEQ)
                self.step()
            else:
                token = Token('+', TokenType.PLUS)
        elif self.curChar == '-':
            if self.peek() == '=':
                token = Token('-=', TokenType.MINUSEQ)
                self.step()
            else:
                token = Token('-', TokenType.MINUS)
        elif self.curChar == '*':
            if self.peek() == '=':
                token = Token('*=', TokenType.ASTERISKEQ)
                self.step()
            else:
                token = Token('*', TokenType.ASTERISK)
        elif self.curChar == '/':
            if self.peek() == '=':
                token = Token('/=', TokenType.SLASHEQ)
                self.step()
            else:
                token = Token('/', TokenType.SLASH)
        elif self.curChar == '>':
            if self.peek() == '=':
                token = Token('>=', TokenType.GTEQ)
                self.step()
            else:
                token = Token('>', TokenType.GT)
        elif self.curChar == '<':
            if self.peek() == '=':
                token = Token('<', TokenType.LTEQ)
                self.step()
            else:
                token = Token('<=', TokenType.LT)
        elif self.curChar == '=':
            if self.peek() == '=':
                token = Token('==', TokenType.EQEQ)
                self.step()
            else:
                token = Token('=', TokenType.EQ)
        elif self.curChar == '!':
            if self.peek() == '=':
                token = Token('!=', TokenType.NOTEQ)
                self.step()
            else:
                token = Token('!', TokenType.NOT)
        #------------------LINE----------------#
        elif self.curChar == '\n':   
            token = Token('\n', TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('\0', TokenType.EOF)

        #-----------------TYPE-----------------#
       
        elif self.curChar.isdigit():
            start = self.curPos
            while self.peek().isdigit():
                self.step()

            if self.peek().isalpha():
                self.abort("Letter found in Number dumbass!")

            if self.peek() == '.': #FLOAT??????
                self.step()
                while self.peek().isdigit():
                    self.step()
                if self.peek().isalpha():
                    self.abort("Letter found in Number dumbass!")
            end = self.curPos + 1 
            value = self.string[start:end]
            token = Token(value, TokenType.NUMBER)
            
        elif self.curChar.isalpha():
            start = self.curPos
            while self.peek().isalnum():
                self.step()
            end  = self.curPos + 1
            value = self.string[start:end]
            keyWord = Token.isKeyword(value)
            token = (Token(value, keyWord) if keyWord 
                     else Token(value, TokenType.IDENT))

        elif self.curChar == '"':
            self.step()
            start = self.curPos 
            while self.curChar != '"':
                self.step()
                if self.curChar == '\0':
                    self.abort("Close the string moron!")
            end = self.curPos 
            value = self.string[start:end]
            token = Token(value, TokenType.STRING)

        else:
            self.abort("Illegal Character")
            
        return token

    def getTokens(self): #This is the API 
        tokens = []
        while self.curChar != '\0':
            self.removeWhitespace()
            #return self.getToken()
            tokens.append(self.getToken())
            self.step()
        return tokens
