from distutils.cmd import Command
import tkinter as tk
from tkinter import BOTTOM, filedialog
from tkinter import font
import os

#CREATING MENU BAR
class Menubar():
    def __init__(self, parent):
        font = ("ubuntu", 8) #INITIAL FONT

        menubar = tk.Menu(parent.app, font=font)

        parent.app.config(menu=menubar)

        #FILE MENU
        filemenu = tk.Menu(menubar, font=font, tearoff=0)
        
        filemenu.add_command(label="New file", command=parent.newfile, accelerator="Ctrl+N")
        filemenu.add_command(label="Open file", command=parent.openfile, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", command=parent.savefile, accelerator="Ctrl+S")
        filemenu.add_command(label="Save as", command=parent.savefileas, accelerator="Ctrl+Shift+S")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=parent.app.destroy)

        menubar.add_cascade(label="File", menu=filemenu)
        #END FILE MENU
        
        #SETTINGS MENU
        sett = tk.Menu(menubar, font=font, tearoff=0)
        
        sett.add_command(label="Settings", command=parent.settings)
        
        menubar.add_cascade(label="Tools", menu=sett)
        #END SETTINGS MENU

#BOTTOM BAR
class Downbar:
    def __init__(self, parent):
        font = ("ubuntu", 8)

        self.dwbar = tk.StringVar()

        self.dwbar.set("TextEdit - Riccardo Vescio")

        label = tk.Label(parent.textarea, textvariable=self.dwbar, fg="black", bg="lightgrey", anchor='sw', font=font)
        label.pack(side=BOTTOM, fill=tk.BOTH)

    #UPDATING BOTTOM BAR
    def updatedwbar(self, *args):
        self.dwbar.set("TextEdit - Riccardo Vescio")
    #END UPDATING BOTTOM BAR
    
    #UPDATING BOTTOM BAR
    def update(self, aux):
        self.dwbar.set(aux)
    #END UPDATING BOTTOM BAR

#TEXT AREA AND SCROLL BAR
class Text:
    #GRAPHICAL SETTINGS
    def __init__(self, app):
        app.title("Untitled - TextEdit")

        app.geometry("1000x550")

        font = ("ubuntu", 9)

        self.app = app

        self.textarea = tk.Text(app, font=font, foreground="white", background="grey10", insertbackground="white")
        self.scroll = tk.Scrollbar(app, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = Menubar(self)
        
        self.dwbar = Downbar(self)

        self.shortcut()
    #END GRAPHICAL SETTINGS

    #SETTING WINDOW TITLE NAME
    def settitle(self, name = None):
        if name:
            self.app.title(name + " - TextEdit")
        else:
            self.app.title("Untitled - TextEdit")
    #END SETTING WINDOW TITLE NAME

    #NEW FILE
    def newfile(self, *args):
        self.textarea.delete(1.0, tk.END)

        self.filename = None

        self.settitle()
        
        self.dwbar.update("TextEdit - Riccardo Vescio")
    #END NEW FILE FUNCTION

    #OPENING FILE
    def openfile(self, *args):
        self.filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Every file", "*.*"),
                                                                                       ("Text file", "*.txt"),
                                                                                       ("Python script", "*.py"),
                                                                                       ("Java file", "*.java"),
                                                                                       ("HTML file", "*.html"),
                                                                                       ("CCS file", "*.css"),
                                                                                       ("Markdown Text", "*.md"),
                                                                                       ("JavaScript file", "*.js")
                                                                                       ])

        if self.filename:
            self.textarea.delete(1.0, tk.END)

            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            
            self.settitle(self.filename)
    #END OPENING FILE FUNCTION

    #SAVING FILE
    def savefile(self, *args):
        if self.filename:
            try:
                aux = self.textarea.get(1.0, tk.END)

                with open(self.filename, "w") as f:
                    f.write(aux)
            
                os.remove(self.tmpname)

                self.dwbar.update("Your file have been saved")
            except Exception as e:
                print(e)
        else:
            self.savefileas()
    #END SAVING FILE FUNCTION

    #SAVING AS
    def savefileas(self, *args):
        try:
            newfile = filedialog.asksaveasfilename(initialfile="SenzaTitolo.txt", defaultextension=".txt", filetypes=[("Every file", "*.*"),
                                                                                                                      ("Text file", "*.txt"),
                                                                                                                      ("Python script", "*.py"),
                                                                                                                      ("Java file", "*.java"),
                                                                                                                      ("HTML file", "*.html"),
                                                                                                                      ("CCS file", "*.css"),
                                                                                                                      ("Markdown Text", "*.md"),
                                                                                                                      ("JavaScript file", "*.js")
                                                                                                                      ])
            
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/~temp.txt')
            
            os.remove(desktop)
            
            with open(newfile, "w") as f:
                aux = self.textarea.get(1.0, tk.END)

                f.write(aux)

            self.filename = newfile

            self.settitle(self.filename)

            self.dwbar.update("Your file have been saved")
        except Exception as e:
            print(e)
    #END SAVING AS FUNCTION
            
    #TEMPORARY FILE FUNCTION
    def savetmp(self, *args):        
        try:            
            aux = str(self.filename)
            
            i = len(aux) - 1
            
            trovato = False
            
            while trovato == False:
                if aux[i] == "/":
                    trovato = True
                    
                    self.tmpname = aux[0 : (i + 1)] + "~" + aux[(i + 1) : (len(aux))]
                    
                i -= 1
                            
            with open(self.tmpname, "w") as f:
                text = self.textarea.get(1.0, tk.END)

                f.write(text)
            
        except AttributeError:            
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/~temp.txt')
            
            with open(desktop, "w") as f:
                text = self.textarea.get(1.0, tk.END)
                
                f.write(text)
        
        except IndexError:            
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/~temp.txt')
                        
            with open(desktop, "w") as f:
                text = self.textarea.get(1.0, tk.END)
                
                f.write(text)
                
        self.dwbar.update("Your file have been saved in a temporary file")
    #END TEMPORARY FILE FUNCTION

    #SHORTCUTS MANAGMENT FUNCTION
    def shortcut(self):
        self.textarea.bind('<Control-n>', self.newfile)
        self.textarea.bind('<Control-o>', self.openfile)
        self.textarea.bind('<Control-s>', self.savefile)
        self.textarea.bind('<Control-S>', self.savefileas)
        self.textarea.bind('<Key>', self.dwbar.updatedwbar)
        self.textarea.bind('<Key>', self.savetmp)
    #END SHORTCUTS MANAGMENT FUNCTION

    #SETTINGS PAGE
    def settings(self):
        #CHANGING THEME FUNCTIONS
        def wht(self):
            self.textarea.config(foreground="black", background="white", insertbackground="black")

        def blk(self):
            self.textarea.config(foreground="white", background="grey10", insertbackground="white")

        def drkb(self):
            self.textarea.config(foreground="white", background="#000022", insertbackground="white")

        def drkg(self):
            self.textarea.config(foreground="white", background="#002200", insertbackground="white")

        def matrix(self):
            self.textarea.config(foreground="green3", background="grey6", insertbackground="green3")
        #END CHANGING THEME FUNCTIONS
            
        #CHANGING FONT FUNCTION
        def setfont(self, font):
            font = (font)
            self.textarea.config(font=font)
        #END CHANGING FONT FUNCTION

        #CHANGING FONT DIMENSION FUNCTION
        def setdimf(self, dim):
            font = ("ubuntu", dim)
            self.textarea.config(font=font)
        #END CHANGING FONT DIMENSION FUNCTION

        #CREATING TOPLEVEL
        setting = tk.Toplevel()
        
        setting.title("Impostazioni")
        
        setting.geometry("250x470")
        #END CREATING TOPLEVEL
        
        #FUNCTION FOR CHANGE SETTINGS
        def getselecteditem():
            aux = ""
            aux2 = ""
            aux3 = ""

            for i in stili.curselection():
                aux = stili.get(i)

            if aux == "Whiteboard":
                wht(self)
            elif aux == "Blackboard":
                blk(self)
            elif aux == "Dark blue":
                drkb(self)
            elif aux == "Dark green":
                drkg(self)
            elif aux == "Matrix":
                matrix(self)

            for i in dimf.curselection():
                aux2 = dimf.get(i)

            
            if aux2 != "":
                setdimf(self, aux2)
                
            for i in font.curselection():
                aux3 = font.get(i)
                
            if aux3 != "":
                setfont(self, aux3)
        #END FUNCTION FOR CHANGE SETTINGS

        #LIST WITH AVAILABLE THEMES
        label = tk.Label(setting, text="Choose theme:")
        label.pack()
        
        stili = tk.Listbox(setting, height=5, width=13)
                
        stili.insert(1, "Whiteboard")
        stili.insert(2, "Blackboard")
        stili.insert(3, "Dark blue")
        stili.insert(4, "Dark green")
        stili.insert(5, "Matrix")

        stili.pack()
        #END OF LIST
                
        #LIST WITH FONT DIMENSIONS
        label = tk.Label(setting, text="Choose font:")
        label.pack()
        
        font = tk.Listbox(setting, height=6, width=13)
                
        font.insert(1, "ubuntu")
        font.insert(2, "Courier")
        font.insert(3, "Arial")
        font.insert(4, "Terminal")
        font.insert(5, "System")
        font.insert(7, "Consolas")

        font.pack()
        #END LIST

        #LIST WITH FONT DIMENSIONS
        label = tk.Label(setting, text="Choose font dimension:")
        label.pack()
        
        dimf = tk.Listbox(setting, height=10, width=13)
                
        dimf.insert(6, "6")
        dimf.insert(7, "7")
        dimf.insert(8, "8")
        dimf.insert(10, "10")
        dimf.insert(11, "11")
        dimf.insert(12, "12")
        dimf.insert(14, "14")
        dimf.insert(16, "16")
        dimf.insert(18, "18")
        dimf.insert(20, "20")

        dimf.pack()
        #END LIST

        #SAVING BUTTOM
        save = tk.Button(setting, text="Save setting", width=18, command=getselecteditem)
        save.pack()
        #END BUTTON
    #END SETTINGS PAGE

#PROGRAM FUNCTIONS
if __name__ == "__main__":
    app = tk.Tk()
    tx = Text(app)
    app.mainloop()