from tkinter import *
from tkinter import filedialog, messagebox
import os

from controllers.lexer import Lexer
from controllers.parser import Parser
from controllers.graph import make_graph

class MenuView():
    menuView = Tk()
    # constructor
    def __init__(self) -> None:
        self.menuView.title("Menu Principal")
        self.menuView.geometry("1150x740")
        self.menuView.config(bg="#93E1D8")
        self.menuView.iconbitmap(os.path.abspath("assets/usac_logo.ico"))
        self.menuView.resizable(0,0)
        self.originalPath = ""
        self.viewUI()
        self.menuView.mainloop()
    # create the UI of the menu view
    def viewUI(self):
        titleFont = ("Arial", 30, "bold")
        # Title
        Label(
            self.menuView,
            text="BizData Analyzer",
            font=titleFont,
            bg="#93E1D8",
            fg="black"
        ).grid(
            row=0,
            column=0,
            columnspan=10,
            ipadx=200,
            pady=10
        )
        # Buton 1 - Open a file
        Button(
            self.menuView,
            text="Abrir",
            width=10,
            command=self.openFile,
        ).grid(
            row=1,
            column=0,
        )
        # Buton 2 - Start to analyze the file
        Button(
            self.menuView,
            text="Analizar",
            width=10,
            command=self.analyzeFile,
        ).grid(
            row=1,
            column=1,
        )
        # Buton 3 - Start to analyze the file
        Button(
            self.menuView,
            text="Reporte de Errores",
            width=15,
            command=self.generateErrors,
        ).grid(
            row=1,
            column=2,
        )
        # Buton 3 - Start to analyze the file
        Button(
            self.menuView,
            text="Árbol de derivación",
            width=15,
            command=self.generateGraphviz,
        ).grid(
            row=1,
            column=3,
        )
        # Buton 3 - Get out of the program
        Button(
            self.menuView,
            text="Salir",
            width=10,
            command=self.menuView.quit,
        ).grid(
            row=1,
            column=4,
        )
        self.editor = Text(self.menuView, width=100, height=37, bg="#DDFFF7", fg="black", font=("Arial", 10))
        self.editor.grid(row=2, column=0, columnspan=5, padx=15, ipadx=15, ipady=10)
        # block the console
        self.console = Text(self.menuView, width=50, height=37, bg="black", fg="#96E2D9", state="disabled", font=("Arial", 10))
        self.console.grid(row=2, column=6, columnspan=5, padx=5, ipadx=5, ipady=10)
    # set text to the console
    def setConsole(self, textIn):
        self.console.config(state="normal")
        self.console.insert(END, textIn)
        self.console.config(state="disabled")    
    # set text to the editor
    def setEditor(self, text):
        self.editor.delete("1.0", END)
        self.editor.insert(END, text)
    # get text from the editor
    def getEditor(self):
        return str(self.editor.get("1.0", END))   
    # open a file and put it on the editor
    def openFile(self):
        try:
            fileSearch = filedialog.askopenfilename(
                initialdir="./",
                title="Abrir Archivo",
                filetypes=(
                    ("bizdata files", "*.bizdata"),
                    ("all files", "*.*")
                )
            )
            
            filepath = os.path.abspath(fileSearch)
            self.originalPath = filepath
            
            with open(filepath, "r") as file:
                text = file.read()
                self.setEditor(text)
                
            self.setConsole("Archivo cargado correctamente: " + filepath + "\n")
        except:
            messagebox.showinfo(title="Aviso", message="Ocurrio un error al abrir el archivo")
    def analyzeFile(self):
        try:
            jsonString = self.getEditor()
            if jsonString == "":
                messagebox.showinfo(title="Aviso", message="No hay texto para analizar")
            else:
                lex = Lexer(jsonString)
                lex.analyze()
                self.setConsole("Archivo analizado correctamente\n")
                
                tokens, tokensToParser = lex.getTokens()
                for token in tokens:
                    self.setConsole(str(token) + "\n")
                
                parser = Parser(tokensToParser)
                try:
                    parser.parse()
                except:
                    print("Error: No se pudo analizar el archivo")
        except:
            messagebox.showinfo(title="Aviso", message="Ocurrio un error al analizar el archivo")   
    def generateErrors(self):
        pass   
    def generateGraphviz(self):
        try:
            make_graph()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self.setConsole("Archivo de reporte generado correctamente: " + dir_path.replace("\\view", '') + "\graphs.gv" + "\n")
        
        except:
            messagebox.showinfo(title="Aviso", message="Ocurrio un error al generar el árbol de derivación")