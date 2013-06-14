from Tkinter import *
import tkMessageBox
obj = Tk()
obj.geometry('400x400')
saludo =  Label(obj, text='Saludos').grid(row=0, column=0)
boton = Button(obj, text='Hola', command=saludo).grid(row=0, column=1)
c = Canvas(obj, height = 360, width=360)
coor = 10,10,360,360
arc = c.create_arc(coor, start=0, extent=359.999, fill='yellow')
arc = c.create_arc(coor, start=0, extent=15, fill='red')
arc = c.create_arc(coor, start=0, extent=-35, fill='blue')
c.grid(row=1)
def saludar():
   tkMessageBox.showinfo('Hola','Hola')
obj.mainloop()
