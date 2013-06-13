from Tkinter import *

def saludo():
    x = 1
    objLabel = Label(root, text='Saludos Terricolas...!')
    objLabel.grid(row=1, column=1)
    comparar(x)
def limpiar():
    x = 0
    objLabel = Label(root, text="Hola")
    objLabel.grid(row=1, column=1)
    comparar(x)
def comparar(x):
    if x==0:
        objButto = Button(root, text='Saludo', command=saludo)
        objButto.grid(row=1, column=2)
        objLabel = Label(root, text="Hola")
        objLabel.grid(row=1, column=1)
    else:
        objButto = Button(root, text='Limpiar', command=limpiar)
        objButto.grid(row=1, column=2)
        
root = Tk()
x = 0
comparar(x)
root.mainloop()
