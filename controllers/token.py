from enum import (
    auto,
    Enum,
    unique
)

from typing import NamedTuple

@unique
class TokenType(Enum):
    # Special tokens    
    ILLEGAL = auto()
    EOF = auto()
    
    # keywords, key and numbers
    KEY = auto() # Registro
    KEYWORD = auto() # "ejemplo"
    INTEGER = auto() # 123
    FLOAT = auto()
    
    # Simbols
    COMMA = auto() # ,
    COLON = auto() # :
    LBRACKET = auto() # [
    LBRACE = auto() # {
    LPAREN = auto() # (
    RBRACKET = auto() # ]
    RBRACE = auto() # }
    RPAREN = auto() # )
    EQUAL = auto()  # =
    SEMICOLON = auto() # ;
    
    # Coments
    LINE_COMMENT = auto()
    BLOCK_COMMENT = auto()
    

class Token(NamedTuple):
    token_type: TokenType
    literal: str
    row: int
    column: int
    
    def __str__(self) -> str:
        return f"Type: { self.token_type }, Literal: { self.literal }"
    
    def getLiteral(self) -> str:
        return self.literal
    
    def getType(self) -> TokenType:
        return self.token_type