from tkinter import *
from tkinter import filedialog, messagebox
import os

from controllers.lexer import Lexer

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
        
        # Menu Buttons
        mb = Menubutton(self.menuView, text="Archivo")
        mb.grid(row=1, column=0)
        mb.menu = Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="Abrir", command=self.openFile) 
        mb.menu.add_command(label="Guardar", command=self.saveFile)
        mb.menu.add_command(label="Guardar como", command=self.saveAsFile)
        mb.menu.add_command(label="Salir", command=self.menuView.quit) 
        
        # Buton 1 - Start to analyze the file
        Button(
            self.menuView,
            text="Analizar",
            width=10,
            command=self.analyzeFile,
        ).grid(
            row=1,
            column=1,
        )
        
        # Button 2 - Generate the errors
        Button(
            self.menuView,
            text="Errores", 
            width=10,
            command=self.generateErrors
        ).grid(
            row=1,
            column=2,
        )
        
        # Button 3 - Generate the report Graphviz
        Button(
            self.menuView,
            text="Reporte", 
            width=10,
            command=self.generateGraphviz
        ).grid(
            row=1,
            column=3,
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
    
    # save the file in the original path
    def saveFile(self):
        try:
            file = open(self.originalPath, "w",  encoding="utf-8", errors='ignore')
            file.write(self.getEditor())
            file.close()
            messagebox.showinfo(title="Aviso", message="Archivo guardado")
            self.setConsole("Archivo guardado correctamente: " + self.originalPath +"\n")
        except:
            messagebox.showinfo(title="Aviso", message="Ocurrio un error al guardar el archivo")
    
    # save the file in a new path
    def saveAsFile(self):
        try:
            fileSearch = filedialog.asksaveasfilename(
                initialdir="./",
                title="Save File",
                filetypes=(
                    ("Text Files", "*.txt"),
                    ("JSON Files", "*.json"),
                    ("All Files", "*.*")
                )
            )

            filepath = os.path.abspath(fileSearch)

            if os.path.exists(filepath):
                self.saveFile()
            else:
                self.originalPath = filepath
                # open the file and put it on the editor
                file = open(self.originalPath, "w",  encoding="utf-8", errors='ignore')
                file.write(self.getEditor())
                file.close()
                messagebox.showinfo(title="Aviso", message="Archivo creado y guardado")
                self.setConsole("Archivo creado correctamente: " + filepath + "\n") 
        except:
            messagebox.showinfo(title="Aviso", message="Ocurrio un error al guardar el archivo")
            
    def analyzeFile(self):
        try:
            jsonString = self.getEditor()
            if jsonString == "":
                messagebox.showinfo(title="Aviso", message="No hay texto para analizar")
            else:
                lex = Lexer(jsonString)
                lex.analyze()
                self.setConsole("Archivo analizado correctamente\n")
                
                tokens = lex.getTokens()
                for token in tokens:
                    self.setConsole(str(token) + "\n")
            pass
        except:
            messagebox.showinfo(title="Aviso", message="Ocurrio un error al analizar el archivo")
    
    def generateErrors(self):
        pass
    
    def generateGraphviz(self):
        pass