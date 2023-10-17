from controllers.token import (
    Token,
    TokenType
)
from controllers.graph import dot

correlativeC = 1
correlativeR = 1
correlativeF = 1

class Parser():
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.listaClaves = []
        self.listaRegistros = []
        
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
                            print("Error: Se esperaba un corchete derecho de cierre")
                else:
                    print("Error: Se esperaba un corchete izquierdo de apertura")
            else:
                print("Error: Se esperaba un signo igual")
        else:
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
                        print("Error: Se esperaba un corchete derecho de cierre")
                else:
                    print("Error: Se esperaba un corchete izquierdo de apertura")
            else:
                print("Error: Se esperaba un signo igual")
        else:
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
                    print("Error: Se esperaba un corchete derecho de cierre") 
        else:
            print("Error: Se esperaba un corchete izquierdo de apertura")
    
    # <valor> ::= KEYWORD | INTEGER | FLOAT
    def valor(self):
        global correlativeR
        if self.tokens[0].token_type == TokenType.KEYWORD or self.tokens[0].token_type == TokenType.INTEGER or self.tokens[0].token_type == TokenType.FLOAT:
            res = self.tokens.pop(0)
            return res
        else:
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
            # self.tokens.pop(0)
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
        dot.node(f'F{ correlativeF }', f'Función {correlativeF}', fillcolor='firebrick', style='filled', shape='circle', fontcolor='white')
        dot.edge('F0', f'F{ correlativeF }')
        correlativeF += 1
        if self.tokens[0].token_type == TokenType.KEY:
            tipo = self.tokens.pop(0)
            if self.tokens[0].token_type == TokenType.LPAREN:
                self.tokens.pop(0)
                parametros = self.parametros()
                if self.tokens[0].token_type == TokenType.RPAREN:
                    self.tokens.pop(0)
                    if self.tokens[0].token_type == TokenType.SEMICOLON:
                        self.tokens.pop(0)
                        self.operarFuncion(tipo, parametros)
                    else:
                        print("Error: Se esperaba un punto y coma")
                else:
                    print("Error: Se esperaba un parentesis derecho de cierre")
            else:
                print("Error: Se esperaba un parentesis izquierdo de apertura")
        else:
            print("Error: Se esperaba una KEY")
    
    # <parametros> ::= <valor> <otroParametro> | ε
    def parametros(self):
        parametros = []
        if self.tokens[0].token_type != TokenType.RPAREN:
            valor = self.valor()
            if valor is not None:
                parametros = [valor]
                self.otroParametro(parametros)
        return parametros

    # <otroParametro> ::= COMMA <valor> <otroParametro> | ε
    def otroParametro(self, parametros):
        if self.tokens[0].token_type == TokenType.COMMA:
            self.tokens.pop(0)
            valor = self.valor()
            if valor is not None:
                parametros.append(valor)
                self.otroParametro(parametros)
        else:
            # epsilon is accepted
            pass
        
    # <otraFuncion> ::= <funcion> <otraFuncion> | ε
    def otraFuncion(self):
        if self.tokens[0].token_type != TokenType.EOF:
            self.funcion()
            self.otraFuncion()
        else:
            print("Fin del archivo")
            
    def operarFuncion(self, tipo, parametros):
        if tipo.literal == 'imprimirln':
            if len(parametros) == 1:
                print(parametros[0].literal)
            else:
                print("Error: La funcion imprimir solo recibe un parametro")
        elif tipo.literal == 'conteo':
            if len(parametros) == 0:
                print(len(self.listaRegistros))
            else:
                print("Error: La funcion conteo no recibe parametros")
        elif tipo.literal == 'promedio':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.promedio(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion promedio debe ser una clave")
            else:
                print("Error: La funcion promedio solo recibe un parametro")
        elif tipo.literal == 'contarsi':
            if len(parametros) == 2:
                if parametros[0].token_type == TokenType.KEYWORD and parametros[1].token_type == TokenType.INTEGER:
                    self.contarsi(parametros[0].literal, parametros[1].literal)
                else:
                    print("Error: Los parametros de la funcion contarsi deben ser una clave y un valor")
        elif tipo.literal == 'datos':
            if len(parametros) == 0:
                self.datos()
            else:
                print("Error: La funcion datos no recibe parametros")
        elif tipo.literal == 'sumar':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.sumar(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion sumar debe ser una clave")
            else:
                print("Error: La funcion sumar solo recibe un parametro")
        elif tipo.literal == 'max':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.max(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion max debe ser una clave")
            else:
                print("Error: La funcion max solo recibe un parametro")
        elif tipo.literal == 'min':
            if len(parametros) == 1:
                if parametros[0].token_type == TokenType.KEYWORD:
                    self.min(parametros[0].literal)
                else:
                    print("Error: El parametro de la funcion min debe ser una clave")
            else:
                print("Error: La funcion min solo recibe un parametro")
        
        # TODO: exportarReporte, imprimirln e imprimir
        
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
            print(f"promedio: { promedio }")
    
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
            print(f"contarsi: {contador}")
    
    def datos(self):
        # show all data
        for claves in self.listaClaves:
            print(claves.replace('"', ''), end="\t")
        
        for registro in self.listaRegistros:
            print()
            for valor in registro:
                print(valor, end="\t")
        print()

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
        
            print(f"sumar: {suma}")
    
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
            print(f"max: {maximo}")
    
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
            print(f"min: {minimo}")
    
    def getListaClaves(self):
        return print(self.listaClaves)
    
    def getListaRegistros(self):
        return print(self.listaRegistros)