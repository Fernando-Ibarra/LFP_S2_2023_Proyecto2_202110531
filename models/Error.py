from controllers.token import (
    TokenType
)

class Error:
    
    def __init__(self, tipo: TokenType, lexema: str, row: int, column: int) -> None:
        self.tipo = tipo
        self.lexema = lexema
        self.row = row
        self.column = column
    
    def __str__(self) -> str:
        return f"Error: { self.tipo } Lexema: { self.lexema } Row: { self.row } Column: { self.column }"