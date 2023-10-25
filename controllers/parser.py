from controllers.token import (
    Token,
    TokenType
)
from controllers.graph import dot
from models.Error import Error, errorsList

correlativeC = 1
correlativeR = 1
correlativeF = 1

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.listaClaves = []
        self.listaRegistros = []
        self.results = []
        self.params = ""
        
    def recovery(self, tokenType: str):
        while self.tokens[0].token_type != TokenType.EOF:
            if self.tokens[0].token_type == tokenType:
                break
            else:
                self.tokens.pop(0)
        
    def parse(self):
        dot.node(f'I0', '<inicio>', fillcolor='gold', style='filled', shape='circle', fontcolor='black')
        self.inicio()

    # <inicio> ::= <claves> <registros> <funciones>        
    def inicio(self):
        dot.node(f'C0', '<claves>', fillcolor='gold3', style='filled', shape='circle', fontcolor='black')
        dot.edge('I0', 'C0')
        self.claves()
        dot.node(f'R0', '<registros>', fillcolor='gold4', style='filled', shape='circle', fontcolor='white')
        dot.edge('I0', 'R0')
        self.registros()
        dot.node(f'F0', '<funciones>', fillcolor='goldenrod', style='filled', shape='circle', fontcolor='black')
        dot.edge('I0', 'F0')
        self.funciones()

    # <claves> ::= KEY EQUAL LBRACKET KEYWORD <otra_clave> RBRACKET
    def claves(self):
        global correlativeC
        dot.node(f'C{ correlativeC }', f'Clave {correlativeC}', fillcolor='aquamarine1', style='filled', shape='circle', fontcolor='black')
        dot.edge('C0', f'C{ correlativeC }')
        base = correlativeC
        correlativeC += 1
        if self.tokens[0].token_type == TokenType.KEY:
            nodeTkn = self.tokens.pop(0)
            dot.node(f'C{ correlativeC }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
            dot.edge(f'C{ base }', f'C{ correlativeC }')
            correlativeC += 1
            if self.tokens[0].token_type == TokenType.EQUAL:
                nodeTkn = self.tokens.pop(0)
                dot.node(f'C{ correlativeC }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
                dot.edge(f'C{ base }', f'C{ correlativeC }')
                correlativeC += 1
                if self.tokens[0].token_type == TokenType.LBRACKET:
                    nodeTkn = self.tokens.pop(0)
                    dot.node(f'C{ correlativeC }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
                    dot.edge(f'C{ base }', f'C{ correlativeC }')
                    correlativeC += 1
                    if self.tokens[0].token_type == TokenType.KEYWORD:
                        clave = self.tokens.pop(0)
                        dot.node(f'C{ correlativeC }', f'{ clave.literal }', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
                        dot.edge(f'C{ base }', f'C{ correlativeC }')
                        correlativeC += 1
                        self.listaClaves.append(clave.literal)
                        dot.node(f'C{ correlativeC }', '<otraClave>', fillcolor='aquamarine3', style='filled', shape='circle', fontcolor='black')
                        dot.edge(f'C{ base }', f'C{ correlativeC }')
                        basetoNode = correlativeC
                        correlativeC += 1
                        self.otraClave(basetoNode)
                        if self.tokens[0].token_type == TokenType.RBRACKET:
                            nodeTkn = self.tokens.pop(0)
                            dot.node(f'C{ correlativeC }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
                            dot.edge(f'C{ base }', f'C{ correlativeC }')
                            correlativeC += 1
                        else:
                            error: Error = Error("Sintáctico", f"Se esperaba un corchete derecho de cierre", self.tokens[0].row, self.tokens[0].column)
                            errorsList.append(error)
                            self.recovery(TokenType.RBRACKET)
                            print("Error: Se esperaba un corchete derecho de cierre")
                else:
                    error: Error = Error("Sintáctico", f"Se esperaba un corchete izquierdo de apertura", self.tokens[0].row, self.tokens[0].column)
                    errorsList.append(error)
                    self.recovery(TokenType.LBRACKET)
                    print("Error: Se esperaba un corchete izquierdo de apertura")
            else:
                error: Error = Error("Sintáctico", "Se esperaba un =", self.tokens[0].row, self.tokens[0].column)
                errorsList.append(error)
                self.recovery(TokenType.EQUAL)
                print("Error: Se esperaba un signo igual")
        else:
            error: Error = Error("Sintáctico", "Se esperaba una KEY - claves", self.tokens[0].row, self.tokens[0].column)
            errorsList.append(error)
            self.recovery(TokenType.KEY)
            print("Error: Se esperaba una KEY - claves")
        
    # <otra_clave> ::= COMMA KEYWORD <otra_clave | ε
    def otraClave(self, baseNode):
        global correlativeC
        if self.tokens[0].token_type == TokenType.COMMA:
            nodeTkn = self.tokens.pop(0)
            dot.node(f'C{ correlativeC }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
            dot.edge(f'C{ baseNode }', f'C{ correlativeC }')
            correlativeC += 1
            if self.tokens[0].token_type == TokenType.KEYWORD:
                clave = self.tokens.pop(0)
                dot.node(f'C{ correlativeC }', f'{ clave.token_type }\n{clave.literal}', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
                dot.edge(f'C{ baseNode }', f'C{ correlativeC }')
                baseNodePrev = correlativeC
                correlativeC += 1
                self.listaClaves.append(clave.literal)
                dot.node(f'C{ correlativeC }', '<otraClave>', fillcolor='aquamarine3', style='filled', shape='circle', fontcolor='black')
                dot.edge(f'C{ baseNodePrev }', f'C{ correlativeC }')
                basetoNode = correlativeC
                correlativeC += 1
                self.otraClave(basetoNode)
            else:
                error: Error = Error("Sintáctico", f"Se esperaba una KEYWORD", self.tokens[0].row, self.tokens[0].column)
                errorsList.append(error)
                self.recovery(TokenType.KEYWORD)
                print("Error: Se esperaba una KEYWORD")
        else:
            dot.node(f'C{ correlativeC }', 'ε', fillcolor='aquamarine2', style='filled', shape='circle', fontcolor='black')
            dot.edge(f'C{ baseNode }', f'C{ correlativeC }')
            correlativeC += 1
            pass
        
    # <registros> ::= KEY EQUAL LBRACKET <registro> <otroRegistro> RBRACKET
    def registros(self):
        global correlativeR
        dot.node(f'R{ correlativeR }', f'Registro {correlativeR}', fillcolor='dodgerblue', style='filled', shape='circle', fontcolor='white')
        dot.edge('R0', f'R{ correlativeR }')
        base = correlativeR
        correlativeR += 1
        if self.tokens[0].token_type == TokenType.KEY:
            nodeTkn = self.tokens.pop(0)
            dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'R{ base }', f'R{ correlativeR }')
            correlativeR += 1
            if self.tokens[0].token_type == TokenType.EQUAL:
                nodeTkn = self.tokens.pop(0)
                dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
                dot.edge(f'R{ base }', f'R{ correlativeR }')
                correlativeR += 1
                if self.tokens[0].token_type == TokenType.LBRACKET:
                    nodeTkn = self.tokens.pop(0)
                    dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
                    dot.edge(f'R{ base }', f'R{ correlativeR }')
                    correlativeR += 1
                    dot.node(f'R{ correlativeR }', 'lista_registro', fillcolor='dodgerblue4', style='filled', shape='circle', fontcolor='white')
                    dot.edge(f'R{ base }', f'R{ correlativeR }')
                    baseNode = correlativeR
                    correlativeR += 1
                    self.registro(baseNode)
                    self.otroRegistro(baseNode)
                    if self.tokens[0].token_type == TokenType.RBRACKET:
                        nodeTkn = self.tokens.pop(0)
                        dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
                        dot.edge(f'R{ base }', f'R{ correlativeR }')
                        correlativeR += 1
                    else:
                        error: Error = Error("Sintáctico", f"Se esperaba un corchete derecho de cierre", self.tokens[0].row, self.tokens[0].column)
                        errorsList.append(error)
                        self.recovery(TokenType.RBRACKET)
                        print("Error: Se esperaba un corchete derecho de cierre")
                else:
                    error: Error = Error("Sintáctico", f"Se esperaba un corchete izquierdo de apertura", self.tokens[0].row, self.tokens[0].column)
                    errorsList.append(error)
                    self.recovery(TokenType.LBRACKET)
                    print("Error: Se esperaba un corchete izquierdo de apertura")
            else:
                error: Error = Error("Sintáctico", f"Se esperaba un =", self.tokens[0].row, self.tokens[0].column)
                errorsList.append(error)
                self.recovery(TokenType.EQUAL)
                print("Error: Se esperaba un signo igual")
        else:
            error: Error = Error("Sintáctico", f"Se esperaba una KEY - registros", self.tokens[0].row, self.tokens[0].column)
            errorsList.append(error)
            self.recovery(TokenType.KEY)
            print("Error: Se esperaba una KEY - registros")
    
    # <registro> ::= LBRACE <valor> <otroValor> RBRACE
    def registro(self, baseNode):
        global correlativeR
        dot.node(f'R{ correlativeR }', 'registro_item', fillcolor='dodgerblue2', style='filled', shape='circle', fontcolor='white')
        dot.edge(f'R{ baseNode }', f'R{ correlativeR }')
        base = correlativeR
        correlativeR += 1
        if self.tokens[0].token_type == TokenType.LBRACE:
            nodeTkn = self.tokens.pop(0)
            dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'R{ base }', f'R{ correlativeR }')
            correlativeR += 1
            res = self.valor()
            dot.node(f'R{ correlativeR }', f'{ res.token_type }\n{res.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'R{ base }', f'R{ correlativeR }')
            correlativeR += 1
            if res is not None:
                registro = []
                registro.append(res.literal)
                self.otroValor(registro, base)
                if self.tokens[0].token_type == TokenType.RBRACE:
                    nodeTkn = self.tokens.pop(0)
                    dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white')
                    dot.edge(f'R{ base }', f'R{ correlativeR }')
                    correlativeR += 1
                    self.listaRegistros.append(registro)
                else:
                    error: Error = Error("Sintáctico", f"Se esperaba un corchete derecho de cierre", self.tokens[0].row, self.tokens[0].column)
                    errorsList.append(error)
                    self.recovery(TokenType.RBRACE)
                    print("Error: Se esperaba un corchete derecho de cierre") 
        else:
            error: Error = Error("Sintáctico", f"Se esperaba un corchete izquierdo de apertura", self.tokens[0].row, self.tokens[0].column)
            errorsList.append(error)
            self.recovery(TokenType.LBRACE)
            print("Error: Se esperaba un corchete izquierdo de apertura")
    
    # <valor> ::= KEYWORD | INTEGER | FLOAT
    def valor(self):
        global correlativeR
        if self.tokens[0].token_type == TokenType.KEYWORD or self.tokens[0].token_type == TokenType.INTEGER or self.tokens[0].token_type == TokenType.FLOAT:
            res = self.tokens.pop(0)
            return res
        else:
            error: Error = Error("Sintáctico", f"No se esperaba un { self.tokens[0].literal }", self.tokens[0].row, self.tokens[0].column)
            errorsList.append(error)
            self.recovery(TokenType.LBRACE)
            print("Error: Se esperaba una KEYWORD, INTEGER o FLOAT")
            return None
    
    # <otroValor> ::= COMMA <valor> <otroValor> | ε
    def otroValor(self, registro, baseNodeOtroVal):
        global correlativeR
        if self.tokens[0].token_type == TokenType.COMMA:
            nodeTkn = self.tokens.pop(0)
            dot.node(f'R{ correlativeR }', f'{ nodeTkn.token_type }\n{nodeTkn.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white',)
            dot.edge(f'R{ baseNodeOtroVal }', f'R{ correlativeR }')
            correlativeR += 1
            res = self.valor()
            dot.node(f'R{ correlativeR }', f'{ res.token_type }\n{res.literal}', fillcolor='dodgerblue3', style='filled', shape='circle', fontcolor='white', )
            dot.edge(f'R{ baseNodeOtroVal }', f'R{ correlativeR }')
            baseNodeValToTroVal = correlativeR
            correlativeR += 1
            if res is not None:
                registro.append(res.literal)
                dot.node(f'R{ correlativeR }', '<otroValor>', fillcolor='dodgerblue4', style='filled', shape='circle', fontcolor='white', )
                dot.edge(f'R{ baseNodeValToTroVal }', f'R{ correlativeR }')
                baseNode2 = correlativeR
                correlativeR += 1
                self.otroValor(registro, baseNode2)
        else:
            dot.node(f'R{ correlativeR }', 'ε', fillcolor='dodgerblue1', style='filled', shape='circle', fontcolor='black', )
            dot.edge(f'R{ baseNodeOtroVal }', f'R{ correlativeR }')
            correlativeR += 1
            pass
    
    # <otroRegistro> ::= <registro> <otroRegistro> | ε
    def otroRegistro(self, baseNode):
        global correlativeR
        if self.tokens[0].token_type == TokenType.LBRACE:
            self.registro(baseNode)
            self.otroRegistro(baseNode)
        else:
            dot.node(f'R{ correlativeR }', 'ε', fillcolor='dodgerblue1', style='filled', shape='circle', fontcolor='black')
            dot.edge(f'R{ baseNode }', f'R{ correlativeR }')
            correlativeR += 1
            pass
    
    # <funciones> ::= <funcion> <otraFuncion>
    def funciones(self):
        self.funcion()
        self.otraFuncion()
    
    # <funcion> ::= KEY LPAREN <parametros> RPAREN SEMICOLON
    def funcion(self):
        global correlativeF
        dot.node(f'F{ correlativeF }', f'Función', fillcolor='firebrick', style='filled', shape='circle', fontcolor='white')
        dot.edge('F0', f'F{ correlativeF }')
        base = correlativeF
        correlativeF += 1
        if self.tokens[0].token_type == TokenType.KEY:
            tipo = self.tokens.pop(0)
            dot.node(f'F{ correlativeF }', f'{ tipo.token_type }\n{ tipo.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'F{ base }', f'F{ correlativeF }')
            correlativeF += 1
            if self.tokens[0].token_type == TokenType.LPAREN:
                nodeTkn = self.tokens.pop(0)
                dot.node(f'F{ correlativeF }', f'{ nodeTkn.token_type }\n{ nodeTkn.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
                dot.edge(f'F{ base }', f'F{ correlativeF }')
                correlativeF += 1
                dot.node(f'F{ correlativeF }', f'<lista_parametro>', fillcolor='firebrick3', style='filled', shape='circle', fontcolor='white')
                dot.edge(f'F{ base }', f'F{ correlativeF }')
                baseListParam = correlativeF
                correlativeF += 1
                parametros = self.parametros(baseListParam)
                if self.tokens[0].token_type == TokenType.RPAREN:
                    nodeTkn = self.tokens.pop(0)
                    dot.node(f'F{ correlativeF }', f'{ nodeTkn.token_type }\n{ nodeTkn.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
                    dot.edge(f'F{ base }', f'F{ correlativeF }')
                    correlativeF += 1
                    if self.tokens[0].token_type == TokenType.SEMICOLON:
                        nodeTkn = self.tokens.pop(0)
                        dot.node(f'F{ correlativeF }', f'{ nodeTkn.token_type }\n{ nodeTkn.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
                        dot.edge(f'F{ base }', f'F{ correlativeF }')
                        correlativeF += 1
                        self.operarFuncion(tipo, parametros)
                    else:
                        error: Error = Error("Sintáctico", f"Se esperaba un { self.tokens[0].literal }", self.tokens[0].row, self.tokens[0].column)
                        errorsList.append(error)
                        self.recovery(TokenType.SEMICOLON)
                        print("Error: Se esperaba un punto y coma")
                else:
                    error: Error = Error("Sintáctico", f"Se esperaba un { self.tokens[0].literal }", self.tokens[0].row, self.tokens[0].column)
                    errorsList.append(error)
                    self.recovery(TokenType.RPAREN)
                    print("Error: Se esperaba un parentesis derecho de cierre")
            else:
                error: Error = Error("Sintáctico", f"Se esperaba un { self.tokens[0].literal }", self.tokens[0].row, self.tokens[0].column)
                errorsList.append(error)
                self.recovery(TokenType.LPAREN)
                print("Error: Se esperaba un parentesis izquierdo de apertura")
        else:
            error: Error = Error("Sintáctico", f"Se esperaba un { self.tokens[0].literal }", self.tokens[0].row, self.tokens[0].column)
            errorsList.append(error)
            self.recovery(TokenType.KEY)
            print("Error: Se esperaba una KEY")
    
    # <parametros> ::= <valor> <otroParametro> | ε
    def parametros(self, base):
        global correlativeF
        parametros = []
        if self.tokens[0].token_type != TokenType.RPAREN:
            valor = self.valor()
            dot.node(f'F{ correlativeF }', f'{ valor.token_type }\n{ valor.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'F{ base }', f'F{ correlativeF }')
            correlativeF += 1
            if valor is not None:
                parametros = [valor]
                dot.node(f'F{ correlativeF }', f'<otroParametro>', fillcolor='firebrick3', style='filled', shape='circle', fontcolor='white')
                dot.edge(f'F{ base }', f'F{ correlativeF }')
                baseOtherParam = correlativeF
                correlativeF += 1
                self.otroParametro(parametros, baseOtherParam)
        else:
            dot.node(f'F{ correlativeF }', 'ε', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'F{ base }', f'F{ correlativeF }')
            correlativeF += 1
            pass
        return parametros

    # <otroParametro> ::= COMMA <valor> <otroParametro> | ε
    def otroParametro(self, parametros, base):
        global correlativeF
        if self.tokens[0].token_type == TokenType.COMMA:
            nodeTkn = self.tokens.pop(0)
            dot.node(f'F{ correlativeF }', f'{ nodeTkn.token_type }\n{ nodeTkn.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'F{ base }', f'F{ correlativeF }')
            correlativeF += 1
            valor = self.valor()
            dot.node(f'F{ correlativeF }', f'{ valor.token_type }\n{ valor.literal }', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'F{ base }', f'F{ correlativeF }')
            baseOtherParam = correlativeF
            correlativeF += 1
            if valor is not None:
                parametros.append(valor)
                self.otroParametro(parametros, baseOtherParam)
        else:
            dot.node(f'F{ correlativeF }', 'ε', fillcolor='firebrick1', style='filled', shape='circle', fontcolor='white')
            dot.edge(f'F{ base }', f'F{ correlativeF }')
            correlativeF += 1
            pass
        
    # <otraFuncion> ::= <funcion> <otraFuncion> | ε
    def otraFuncion(self):
        if self.tokens[0].token_type != TokenType.EOF:
            self.funcion()
            self.otraFuncion()
        else:
            print("Fin del archivo")
            
    def operarFuncion(self, tipo, parametros):
        if tipo.literal == 'imprimir':
            if len(parametros) == 1:
                self.params = self.params + parametros[0].literal.replace('"', '')
                self.params.replace('\n', '').replace('\t', '')
                self.results.append(f"imprimir({ parametros[0].literal });")
                self.results.append(f"{ self.params }")
            else:
                print("Error: La funcion imprimir solo recibe un parametro")
        elif tipo.literal == 'imprimirln':
            if len(parametros) == 1:
                param = parametros[0].literal.replace('"', '')
                self.results.append(f"imprimirln({ parametros[0].literal });")
                self.results.append(f"{ param }")
            else:
                print("Error: La funcion imprimirln solo recibe un parametro")
        elif tipo.literal == 'conteo':
            if len(parametros) == 0:
                self.results.append("conteo();")
                self.results.append(f">>> { len(self.listaRegistros) }")
            else:
                print("Error: La funcion conteo no recibe parametros")
        elif tipo.literal == 'promedio':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.results.append(f"promedio({ parametros[0].literal });")
                    self.promedio(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion promedio debe ser una clave")
            else:
                print("Error: La funcion promedio solo recibe un parametro")
        elif tipo.literal == 'contarsi':
            if len(parametros) == 2:
                if parametros[0].token_type == TokenType.KEYWORD and (parametros[1].token_type == TokenType.INTEGER or parametros[1].token_type == TokenType.FLOAT):
                    self.results.append(f"contarsi({ parametros[0].literal }, { parametros[1].literal });")
                    self.contarsi(parametros[0].literal, parametros[1].literal)
                else:
                    print("Error: Los parametros de la funcion contarsi deben ser una clave y un valor")
        elif tipo.literal == 'datos':
            if len(parametros) == 0:
                self.results.append("datos();")
                self.datos()
            else:
                print("Error: La funcion datos no recibe parametros")
        elif tipo.literal == 'sumar':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.results.append(f"sumar({ parametros[0].literal });")
                    self.sumar(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion sumar debe ser una clave")
            else:
                print("Error: La funcion sumar solo recibe un parametro")
        elif tipo.literal == 'max':
            if len(parametros) == 1:
                self.results.append(f"max({ parametros[0].literal });")
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.max(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion max debe ser una clave")
            else:
                print("Error: La funcion max solo recibe un parametro")
        elif tipo.literal == 'min':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.results.append(f"min({ parametros[0].literal });")
                    self.min(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion min debe ser una clave")
            else:
                print("Error: La funcion min solo recibe un parametro")
        elif tipo.literal == 'exportarReporte':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.results.append(f"exportarReporte({ parametros[0].literal });")
                    param = parametros[0].literal.replace('"', '')
                    self.results.append(param)
                else:
                    print("Error: El parametro de la funcion exportarReporte debe ser una clave")
        # TODO: exportarReporte
        
    def promedio(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        
        if encontrado:
            suma = 0
            promedio = 0
            for registro in self.listaRegistros:
                suma += float(registro[posicion])
            if len(self.listaRegistros) > 0:
                promedio = suma / len(self.listaRegistros)
            self.results.append(f">>> { promedio }")
    
    def contarsi(self, campo, valor):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        
        if encontrado:
            contador = 0
            for registro in self.listaRegistros:
                if registro[posicion] == valor:
                    contador += 1
            self.results.append(f">>> { contador }")
    
    def datos(self):
        keys = ">>> "
        for claves in self.listaClaves:
            keys = keys + '  ' + claves.replace('"', '')
        self.results.append(f"{ keys }")
        
        for registro in self.listaRegistros:
            value = ">>> "
            for valor in registro:
                if '"' in valor:
                    valor = valor.replace('"', '')
                    value = value + '  ' + valor.replace('"', '')
                else: 
                    value = value + '  ' + valor
            self.results.append(f"{ value }")

    def sumar(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        
        if encontrado:
            suma = 0
            for registro in self.listaRegistros:
                suma += float(registro[posicion])
            self.results.append(f">>> { suma }")
    
    def max(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        
        if encontrado:
            valores = []
            for registro in self.listaRegistros:
                valores.append(float(registro[posicion]))
            maximo = max(valores)
            self.results.append(f">>> { maximo }")
    
    def min(self, campo):
        encontrado = False
        posicion = -1
        for c in self.listaClaves:
            posicion += 1
            if c == campo:
                encontrado = True
                break
        
        if encontrado:
            valores = []
            for registro in self.listaRegistros:
                valores.append(float(registro[posicion]))
            minimo = min(valores)
            self.results.append(f">>> { minimo }")
    
    def getListaClaves(self) -> []:
        return self.listaClaves
    
    def getListaRegistros(self) -> []:
        return self.listaRegistros
    
    def getResults(self) -> []:
        return self.results