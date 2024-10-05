from compiler.lexer import * 
from enum import Enum
class TokenType(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1 ##
    IDENT = 2 ##
    STRING = 3 ##
    #---------------Key Words---------------# 
        #RANGE FROM 100 to 200
    IF = 100
    THEN = 101
    ELSE = 102 #TODO
    ELSIF = 103 #TODO
    ENDIF = 104 
    DO = 105
    LOOP = 106 #TODO
    FOR = 107 #TODO
    NEXT = 108 #TODO
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    PRINT = 112
    LABEL = 113
    GOTO = 114
    LET = 115
    INPUT = 116
    #---------------Operators---------------#
    EQ = 44
    PLUS = 15
    PLUSEQ = 200
    MINUS = 16
    MINUSEQ = 201
    ASTERISK = 17
    ASTERISKEQ = 50
    SLASH = 18
    SLASHEQ = 51
        #not done!
    LSHIFT = 24
    RSHIFT = 25
    NOT = 26
    AND = 27
    OR = 28
    XOR = 29
    MOD = 30
        #not done!
    #----------COMPARE------------#
        #RANGE FROM 200 TO 300
    EQEQ = 201
    LT = 202
    GT = 203
    LTEQ = 204
    GTEQ = 205
    NOTEQ = 206
    
class Token:
    def __init__(self, value, type: TokenType):
        self.value = value
        self.type = type
    def __str__(self):
        return f'{self.type}'
        
    @staticmethod
    def isKeyword(value: str):
        for type in TokenType:
            if type.value >= 100 and type.name == value and type.value <= 200:
            #if type.name == value:
                return type
        return None
