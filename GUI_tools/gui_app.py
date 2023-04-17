import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("Auto Jira")
        #setting window size
        width=600
        height=494
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GButton_289=tk.Button(root)
        GButton_289["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_289["font"] = ft
        GButton_289["fg"] = "#000000"
        GButton_289["justify"] = "center"
        GButton_289["text"] = "Browse"
        GButton_289["relief"] = "flat"
        GButton_289.place(x=40,y=30,width=70,height=25)
        GButton_289["command"] = self.GButton_289_command

        GLabel_147=tk.Label(root)
        GLabel_147["bg"] = "#f2eeee"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_147["font"] = ft
        GLabel_147["fg"] = "#333333"
        GLabel_147["justify"] = "center"
        GLabel_147["text"] = "label"
        GLabel_147.place(x=30,y=90,width=70,height=25)

        GListBox_842=tk.Listbox(root)
        GListBox_842["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_842["font"] = ft
        GListBox_842["fg"] = "#333333"
        GListBox_842["justify"] = "center"
        GListBox_842.place(x=150,y=80,width=410,height=391)

        GMessage_865=tk.Message(root)
        ft = tkFont.Font(family='Times',size=10)
        GMessage_865["font"] = ft
        GMessage_865["fg"] = "#333333"
        GMessage_865["justify"] = "center"
        GMessage_865["text"] = ""
        GMessage_865["relief"] = "flat"
        GMessage_865.place(x=140,y=30,width=433,height=30)

    def GButton_289_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
