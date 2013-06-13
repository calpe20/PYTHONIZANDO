#!/usr/bin/python
from Tkinter import *
root = Tk()
label1 = Label(root, text='Calculadora')
label1.grid(row=0,column=0)
for r in range(1,3):
    for c in range(4):
        exp= Label(root, text='R%s/C%s'%(r,c),borderwidth=1 ).grid(row=r,column=c)
root.mainloop()
