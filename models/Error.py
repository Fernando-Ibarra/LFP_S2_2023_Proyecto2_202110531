errorsList = []

class Error:
    
    def __init__(self, tipo: str, lexema: str, row: int, column: int) -> None:
        self.tipo = tipo
        self.lexema = lexema
        self.row = row
        self.column = column
    
    def __str__(self) -> str:
        return f"Error: { self.tipo } Lexema: { self.lexema } Row: { self.row } Column: { self.column }"