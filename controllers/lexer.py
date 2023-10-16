from controllers.token import (
    Token,
    TokenType
)

from models.Error import Error

tokens = []
tokensToParser = []

class Lexer:

    def __init__(self, source: str) -> None:
        self.source: str = source

    # State 1 - Key        
    def key_analyzer(self, character: str) -> bool:
        if character.isalpha():
            return True
        else:
            return False

    # State 2 - KeyWord
    def keyword_start_analyzer(self, character: str) -> bool:
        if character == '"':
            return True
        else:
            return False
        
    # State 3 - Number with negative or positive sign
    def number_sign_analyzer(self, character: str) -> bool:
        if character == "+" or character == "-":
            return True
        else:
            return False
    
    # State 4 - Number
    def number_analyzer(self, character: str) -> bool:
        if character.isdigit():
            return True
        else:
            return False
        
    # state 5 - Line Comment begin
    def line_comment_begin_analyzer(self, character: str) -> bool:
        if character == "#":
            return True
        else:
            return False
    
    # state 5 - Line Comment end
    def line_comment_end_analyzer(self, character: str) -> bool:
        if character != "\n" or character != "\r":
            return True
        else:
            return False
        
    # state 6 - Block Comment begin
    def block_comment_begin_analyzer(self, character: str) -> bool:
        if character == "'":
            return True
        else:
            return False
    
    # state 7 - KeyWord text
    def keyword_text_analyzer(self, character: str) -> bool:
        if character.isalpha():
            if character == '"':
                return False
            else:
                return True
        elif character.isdigit():
            return True
        if character != '"' or character != "\n" or character != "\r" or character != "\t":
            return True         
        else:
            return False
    
    # state 8 - KeyWord end
    def keyword_end_analyzer(self, character: str) -> bool:
        if character == '"':
            return True
        else:
            return False
    
    # state 9 - point in number
    def number_point_analyzer(self, character: str) -> bool:
        if character == ".":
            return True
        else:
            return False
    
    # state 10 - decimal number
    def decimal_number_analyzer(self, character: str) -> bool:
        if character.isdigit():
            return True
        else:
            return False
        
    # state 11 - Block Comment continue
    def block_comment_continue_analyzer(self, character: str) -> bool:
        if character == "'":
            return True
        else:
            return False
    
    # state 12 -  Block Comment content
    def block_comment_content_analyzer(self, character: str) -> bool:
        if character != "'":
            return True
        else:
            return False
    
    # All simbols
    def simbol_analyzer(self, character: str) -> bool:
        if character == "," or character == ":" or character == "[" or character == "]" or character == "{" or character == "}" or character == "(" or character == ")" or character == "=" or character == ";":
            return True
        else:
            return False
        
    def analyze(self):
        row = 1
        column = 1
        
        state = 0
        prev_state = 0
        lexeme = ""
        
        for character in self.source:
            if state == 0:
                if self.key_analyzer(character):
                    state = 1
                    lexeme += character
                    prev_state = 0
                elif self.keyword_start_analyzer(character):
                    state = 2
                    lexeme += character
                    prev_state = 0
                elif self.number_sign_analyzer(character):
                    state = 3
                    lexeme += character
                    prev_state = 0
                elif self.number_analyzer(character):
                    state = 4
                    lexeme += character
                    prev_state = 0
                elif self.line_comment_begin_analyzer(character):
                    state = 5
                    lexeme += character
                    prev_state = 0
                elif self.block_comment_begin_analyzer(character):
                    state = 6
                    lexeme += character
                    prev_state = 0
                elif self.simbol_analyzer(character):
                    state = 8
                    lexeme += character
                    prev_state = 0
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                    state = 0
                    lexeme = ""
                    prev_state = 0
            elif state == 1:
                if self.key_analyzer(character):
                    state = 1
                    lexeme += character
                    prev_state = 1
                else:
                    token: Token = Token(TokenType.KEY, lexeme)
                    tokens.append(token)
                    tokensToParser.append(token)
                    state = 0
                    prev_state = 0
                    lexeme = ""
                    if self.key_analyzer(character):
                        state = 1
                        lexeme += character
                        prev_state = 0
                    elif self.keyword_start_analyzer(character):
                        state = 2
                        lexeme += character
                        prev_state = 0
                    elif self.number_sign_analyzer(character):
                        state = 3
                        lexeme += character
                        prev_state = 0
                    elif self.number_analyzer(character):
                        state = 4
                        lexeme += character
                        prev_state = 0
                    elif self.line_comment_begin_analyzer(character):
                        state = 5
                        lexeme += character
                        prev_state = 0
                    elif self.block_comment_begin_analyzer(character):
                        state = 6
                        lexeme += character
                        prev_state = 0
                    elif self.simbol_analyzer(character):
                        state = 8
                        lexeme += character
                        prev_state = 0
                    else:
                        if character == "\n" or character == "\r" or character == "\t" or character == " ":
                            pass
                        else:
                            token: Token = Token(TokenType.ILLEGAL, character)
                            tokens.append(token)
                            tokensToParser.append(token)
                        state = 0
                        lexeme = ""
                        prev_state = 0
            elif state == 2:
                if self.keyword_text_analyzer(character):
                    state = 7
                    lexeme += character
                    prev_state = 2
                else:
                    if character == "\n" or character == "\r" or character == "\t":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            elif state == 3:
                if self.number_analyzer(character):
                    state = 4
                    lexeme += character
                    prev_state = 3
                else:
                    if character == "\n" or character == "\r" or character == "\t":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            elif state == 4:
                if self.number_point_analyzer(character):
                    state = 9
                    lexeme += character
                    prev_state = 4
                elif self.number_analyzer(character):
                    state = 4
                    lexeme += character
                    prev_state = 4
                else:
                    token: Token = Token(TokenType.INTEGER, lexeme)
                    tokens.append(token)
                    tokensToParser.append(token)
                    state = 0
                    prev_state = 0
                    lexeme = ""
                    if self.key_analyzer(character):
                        state = 1
                        lexeme += character
                        prev_state = 0
                    elif self.keyword_start_analyzer(character):
                        state = 2
                        lexeme += character
                        prev_state = 0
                    elif self.number_sign_analyzer(character):
                        state = 3
                        lexeme += character
                        prev_state = 0
                    elif self.number_analyzer(character):
                        state = 4
                        lexeme += character
                        prev_state = 0
                    elif self.line_comment_begin_analyzer(character):
                        state = 5
                        lexeme += character
                        prev_state = 0
                    elif self.block_comment_begin_analyzer(character):
                        state = 6
                        lexeme += character
                        prev_state = 0
                    elif self.simbol_analyzer(character):
                        state = 8
                        lexeme += character
                        prev_state = 0
                    else:
                        if character == "\n" or character == "\r" or character == "\t" or character == " ":
                            pass
                        else:
                            token: Token = Token(TokenType.ILLEGAL, character)
                            tokens.append(token)
                            tokensToParser.append(token)
                        state = 0
                        lexeme = ""
                        prev_state = 0
            elif state == 5:
                if character == "\n" or character == "\r":
                    token: Token = Token(TokenType.LINE_COMMENT, lexeme)
                    tokens.append(token)
                    lexeme = ""
                    state = 0
                    prev_state = 0
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                elif self.line_comment_end_analyzer(character):
                    state = 5
                    lexeme += character
                    prev_state = 5
            elif state == 6:
                if self.block_comment_continue_analyzer(character):
                    state = 11
                    lexeme += character
                    prev_state = 6
                else:
                    token: Token = Token(TokenType.ILLEGAL, character)
                    tokens.append(token)
                    tokensToParser.append(token)
                    lexeme = ""
                    state = 0
                    prev_state = 0  
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)    
            elif state == 7:
                if self.keyword_end_analyzer(character):
                    state = 8
                    lexeme += character
                    prev_state = 7
                elif self.keyword_text_analyzer(character):
                    state = 7
                    lexeme += character
                    prev_state = 7
                else:
                    token: Token = Token(TokenType.ILLEGAL, character)
                    tokens.append(token)
                    tokensToParser.append(token)
                    lexeme = ""
                    state = 0
                    prev_state = 0
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
            elif state == 8:
                if prev_state == 7:
                    token: Token = Token(TokenType.KEYWORD, lexeme)
                    tokens.append(token)
                    tokensToParser.append(token)
                elif prev_state == 14:
                    token: Token = Token(TokenType.BLOCK_COMMENT, lexeme)
                    tokens.append(token)
                elif prev_state == 0:
                    if lexeme == ",":
                        token: Token = Token(TokenType.COMMA, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == ":":
                        token: Token = Token(TokenType.COLON, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == "[":
                        token: Token = Token(TokenType.LBRACKET, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == "{":
                        token: Token = Token(TokenType.LBRACE, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == "(":
                        token: Token = Token(TokenType.LPAREN, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == "]":
                        token: Token = Token(TokenType.RBRACKET, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == "}":
                        token: Token = Token(TokenType.RBRACE, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == ")":
                        token: Token = Token(TokenType.RPAREN, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == "=":
                        token: Token = Token(TokenType.EQUAL, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                    elif lexeme == ";":
                        token: Token = Token(TokenType.SEMICOLON, lexeme)
                        tokens.append(token)
                        tokensToParser.append(token)
                lexeme = ""
                if self.key_analyzer(character):
                    state = 1
                    lexeme += character
                    prev_state = 0
                elif self.keyword_start_analyzer(character):
                    state = 2
                    lexeme += character
                    prev_state = 0
                elif self.number_sign_analyzer(character):
                    state = 3
                    lexeme += character
                    prev_state = 0
                elif self.number_analyzer(character):
                    state = 4
                    lexeme += character
                    prev_state = 0
                elif self.line_comment_begin_analyzer(character):
                    state = 5
                    lexeme += character
                    prev_state = 0
                elif self.block_comment_begin_analyzer(character):
                    state = 6
                    lexeme += character
                    prev_state = 0
                elif self.simbol_analyzer(character):
                    state = 8
                    lexeme += character
                    prev_state = 0
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                    state = 0
                    lexeme = ""
                    prev_state = 0
            elif state == 9:
                if self.decimal_number_analyzer(character):
                    state = 10
                    lexeme += character
                    prev_state = 9
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            elif state == 10:
                if self.decimal_number_analyzer(character):
                    state = 10
                    lexeme += character
                    prev_state = 10
                else:
                    token: Token = Token(TokenType.FLOAT, lexeme)
                    tokens.append(token)
                    tokensToParser.append(token)
                    state = 0
                    prev_state = 0
                    lexeme = ""
                    if self.key_analyzer(character):
                        state = 1
                        lexeme += character
                        prev_state = 0
                    elif self.keyword_start_analyzer(character):
                        state = 2
                        lexeme += character
                        prev_state = 0
                    elif self.number_sign_analyzer(character):
                        state = 3
                        lexeme += character
                        prev_state = 0
                    elif self.number_analyzer(character):
                        state = 4
                        lexeme += character
                        prev_state = 0
                    elif self.line_comment_begin_analyzer(character):
                        state = 5
                        lexeme += character
                        prev_state = 0
                    elif self.block_comment_begin_analyzer(character):
                        state = 6
                        lexeme += character
                        prev_state = 0
                    elif self.simbol_analyzer(character):
                        state = 8
                        lexeme += character
                        prev_state = 0
                    else:
                        if character == "\n" or character == "\r" or character == "\t" or character == " ":
                            pass
                        else:
                            token: Token = Token(TokenType.ILLEGAL, character)
                            tokens.append(token)
                            tokensToParser.append(token)
                        state = 0
                        lexeme = ""
                        prev_state = 0
            elif state == 11:
                if self.block_comment_continue_analyzer(character):
                    state = 12
                    lexeme += character
                    prev_state = 11
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            elif state == 12:
                if self.block_comment_content_analyzer(character):
                    state = 12
                    lexeme += character
                    prev_state = 12
                elif self.block_comment_begin_analyzer(character):
                    state = 13
                    lexeme += character
                    prev_state = 12
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            elif state == 13:
                if self.block_comment_continue_analyzer(character):
                    state = 14
                    lexeme += character
                    prev_state = 13
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            elif state == 14:
                if self.block_comment_continue_analyzer(character):
                    state = 8
                    lexeme += character
                    prev_state = 14
                else:
                    if character == "\n" or character == "\r" or character == "\t" or character == " ":
                        pass
                    else:
                        token: Token = Token(TokenType.ILLEGAL, character)
                        tokens.append(token)
                        tokensToParser.append(token)
                        lexeme = ""
                        state = 0
                        prev_state = 0
            else:
                if character == "\n" or character == "\r" or character == "\t" or character == " ":
                    pass
                else:
                    token: Token = Token(TokenType.ILLEGAL, character)
                    tokens.append(token)
                    tokensToParser.append(token)
                    lexeme = ""
                    state = 0
                    prev_state = 0
            # break line
            if character == "\n" or character == "\r":
                row += 1
                continue          
            # tab
            if  character == "\t":
                column += 4
                continue
            # space
            if character == " ":
                column += 1
                continue
            # column
            column += 1
        token: Token = Token(TokenType.EOF, "EOF")
        tokens.append(token)
        tokensToParser.append(token)

    def getTokens(self) -> list:
        return tokens, tokensToParser