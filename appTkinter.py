from Tkinter import *
import tkMessageBox
import sqlite3
root = Tk()
root.geometry('800x600')
root.title('Esperando')
def conectar():
    con = sqlite3.connect('dbase.db')
    cursor = connection.cursor()
    
def alerta():
    tkMessageBox.showwarning("HOla", "Saludando")
def cabecera():
    btnMsg = Button(root, text='Hola', command=donothing)
    btnMsg.grid(row=0,column=0)
def donothing():
    filewin = Toplevel(root)
    lblSaludo = Label(filewin, text='ID')
    lblSaludo.grid(row=2, column=0)
    lblSaludo = Label(filewin, text='NOMBRES')
    lblSaludo.grid(row=2, column=1)
    lblSaludo = Label(filewin, text='APELLIDOS')
    lblSaludo.grid(row=2, column=2)
    lblSaludo = Label(filewin, text='EDAD')
    lblSaludo.grid(row=2, column=3)
    lblSaludo = Label(filewin, text='SEXO')
    lblSaludo.grid(row=2, column=4)
    filewin.title('Saludoando')
cabecera()
root.mainloop()
