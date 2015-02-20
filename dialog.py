import tkinter.simpledialog
from tkinter import *

class MyDialog(tkinter.simpledialog.Dialog):

    def body(self, master):

        Label(master, text="Pokemon Name:").grid(row=0)
        Label(master, text="Error Description:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        with open('log.txt',mode='a') as f:
            f.write('Name: '+first+'\t')
            f.write('Problem: '+second+'\n')
            