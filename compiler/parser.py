from compiler.lexer import Lexer
from compiler.notToken import * 
import sys
class Parser: #Like a lexer but for Tokens! 
    def __init__(self, lexer, emitter):
        self.tokens = lexer.getTokens()
        self.emitter = emitter
        self.curPos = 0
        self.curTok = self.tokens[0]

        self.symbols = set()    # Variables declared so far.
        self.labelsDeclared = set() # Labels declared so far.
        self.labelsGotoed = set() # Labels goto'ed so far.

        
    def step(self):
        self.curPos += 1
        if len(self.tokens) <= self.curPos + 1:
            self.curTok = Token('\0', TokenType.EOF)
        else:
            self.curTok = self.tokens[self.curPos] 
        
    def peek(self):
        if len(self.tokens) >= self.curPos + 1:
            return Token('\0', TokenType.EOF)
        return self.tokens[self.curPos + 1]    
        
    # Return true if the current token matches.
    def checkToken(self, type):
        return self.curTok.type == type

    # Return true if the next token matches.
    def checkPeek(self, type):
        if len(self.tokens) >= (self.curPos + 1) and type == TokenType.EOF:
            return True
        elif len(self.tokens) >= (self.curPos + 1):
            return False
        return self.tokens[self.curPos + 1].type == type
    
    def abort(self, message):
        sys.exit("Error. " + message)
    
    def match(self, type):
        if not self.checkToken(type):
            self.abort(f"Expected {type}, got {self.curTok}")
        self.step()

        
    def parseProgram(self):
        print("PROGRAM")

        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void){")

        while not self.checkToken(TokenType.EOF):
            self.parseNEWLINE()
            self.parseStatement()

        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")
        
        for label in self.labelsDeclared:
            if label not in self.labelsGotoed:
                self.abort("Trying to GOTO a LABEL that doesn't exist" + self.curTok.value)
            
    def parseStatement(self):
        
        #"PRINT" (expression | string) nl
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT - PRINT")
            self.step()
            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine('printf(\"' + self.curTok.value + '\\n\");')
                print("STRING")
                self.step()
            else:
                self.emitter.emit('printf(\"%.2f\\n\", (float)(')
                self.parseExpression()
                self.emitter.emitLine('));')

        #| "IF" comparison "THEN" nl {statement} "ENDIF" nl
        elif self.checkToken(TokenType.IF):
            print("STATEMENT - IF")
            self.emitter.emit("if (")
            self.step()
            self.parseComparison()
            self.match(TokenType.THEN)
            self.emitter.emitLine(") {")
            print("THEN")
            while not self.checkToken(TokenType.ENDIF):
                self.parseNEWLINE()
                if self.checkToken(TokenType.EOF):
                    assert False, f"Expected {TokenType.ENDIF}, got {self.curTok}"
                self.parseStatement()
            self.emitter.emitLine("}")
            print("ENDIF")
            self.step()

        #| "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
        elif self.checkToken(TokenType.WHILE):  
            print("STATEMENT - WHILE")
            self.emitter.emit("while (")
            self.step()
            self.parseComparison()
            self.match(TokenType.REPEAT)
            self.emitter.emitLine(") {")
            while not self.checkToken(TokenType.ENDWHILE):
                self.parseNEWLINE()
                if self.checkToken(TokenType.EOF):
                    assert False, f"Expected {TokenType.ENDWHILE}, got {self.curTok}"
                self.parseStatement()
            self.emitter.emitLine("}")
            print("ENDWHILE")
            self.step()

        #| "LABEL" ident nl
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT - LABEL")
            self.step()
            if self.curTok.value in self.labelsDeclared:
                self.abort("Label already exists: " + self.curTok.value)
            eimitter.emitLine(self.curTok+":")
            self.labelsDeclared.add(self.curTok.value)
            self.match(TokenType.IDENT)
            print("IDENT")

        #| "GOTO" ident nl
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT - GOTO")
            self.step()
            self.labelsGotoed.add(self.curTok.value)
            eimitter.emitLine("goto " + self.curTok)
            self.match(TokenType.IDENT)
            print("IDENT")

        #| "LET" ident "=" expression nl
        elif self.checkToken(TokenType.LET):
            print("STATEMENT - LET")
            self.step()
            if self.curTok.value not in self.symbols:
                self.symbols.add(self.curTok.value) 
                self.emitter.headerLine("float " + self.curTok.value + ";")
            self.emitter.emit(self.curTok.value + " = ")
            self.match(TokenType.IDENT)
            print("IDENT")
            self.match(TokenType.EQ)
            print("=")
            self.parseExpression()
            self.emitter.emitLine(";")

        #| "INPUT" ident nl
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT - INPUT")
            self.step()
            if self.curTok.value not in self.symbols:
                self.symbols.add(self.curTok.value) 
                self.emitter.headerLine("float " + self.curTok.value + ";")

            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curTok.value + ")) {")
            self.emitter.emitLine(self.curTok.value + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")
            self.match(TokenType.IDENT)
            print("IDENT")

        elif self.checkToken(TokenType.EOF):
            pass
        else:
            self.abort(f"Expected a STATMENT, got {self.curTok}")

        #nl
        self.parseNEWLINE()

    def parseComparison(self):
        #comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        print("COMPARISON")
        self.parseExpression()
        
        while True: 
            if self.checkToken(TokenType.EQEQ):
                print("==")
                self.emitter.emit(" == ")
                self.step()
                self.parseExpression()
                continue
            elif self.checkToken(TokenType.NOTEQ):
                print("!=")
                self.emitter.emit(" != ")
                self.step()
                self.parseExpression()
                continue
            elif self.checkToken(TokenType.GT):
                print(">")
                self.emitter.emit(" > ")
                self.step()
                self.parseExpression()
                continue
            elif self.checkToken(TokenType.GTEQ):
                print(">=") 
                self.emitter.emit(" >= ")
                self.step()
                self.parseExpression()
                continue
            elif self.checkToken(TokenType.LT):
                print("<")
                self.emitter.emit(" < ")
                self.step()
                self.parseExpression()
                continue
            elif self.checkToken(TokenType.LTEQ):
                print("<=")
                self.emitter.emit(" <= ")
                self.step()
                self.parseExpression()
                continue
            break
        
    def parseExpression(self): 
        #expression ::= term {( "-" | "+" ) term}
        print("EXPRESSION")
        self.parseTerm()
        while True: 
            if self.checkToken(TokenType.MINUS):
                print("MINUS")
                self.emitter.emit(" - ")
                self.step()
                self.parseTerm()
                continue
            elif self.checkToken(TokenType.PLUS):
                print("PLUS")
                self.emitter.emit(" + ")
                self.step()
                self.parseTerm()
                continue
            break
        
    def parseTerm(self): 
        #term ::= unary {( "/" | "*" ) unary}
        print("TERM")
        self.parseUnari()
        while True: 
            if self.checkToken(TokenType.SLASH):
                print("DIVIDE")
                self.emitter.emit(" / ")
                self.step()
                self.parseUnari()
                continue
            elif self.checkToken(TokenType.ASTERISK):
                print("MULTIPLY")
                self.emitter.emit(" * ")
                self.step()
                self.parseUnari()
                continue
            break
        
    def parseUnari(self): 
        #unary ::= ["+" | "-"] primary
        print("UNARY")
        if self.checkToken(TokenType.PLUS):
            print("POSITIVE")
            self.emitter.emit(" +")
            self.step()
        elif self.checkToken(TokenType.MINUS):
            print("NEGATIVE")
            self.emitter.emit(" -")
            self.step()
        self.parsePrimary()
        
    def parsePrimary(self):
        #primary ::= number | ident
        print("PRIMARY")
        if self.checkToken(TokenType.NUMBER):
            print("NUMBER", self.curTok.value)
            self.emitter.emit(self.curTok.value)
        elif self.checkToken(TokenType.IDENT):
            if self.curTok.value not in self.symbols:
                self.abort("Referencing variable before asignnmet" + self.curTok.value)
            print("IDENT")
            self.emitter.emit(self.curTok.value)
        else:
            self.abort("{self.curTok.value} can either be NUMBER or IDENT, not {self.curTok.type}")
        self.step()
        
    def parseNEWLINE(self): 
        #nl ::= '\n'+
        while self.checkToken(TokenType.NEWLINE):
            print("NEWLINE") 
            self.step()
