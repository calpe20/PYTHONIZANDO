from Tkinter import *
import tkMessageBox
import cx_Oracle
vta = Tk()
vta.geometry('800x500+100+100')
vta.title(' => CUOTA DE ALBUM')
contenedor1 = Frame(vta, width=50, relief=SUNKEN, borderwidth=1)
contenedor1.pack(side= LEFT)
contenedor2 = Frame(vta).grid(row=2, column=1)
codigo = StringVar()
imgsalir = vta.PhotoImage(file="imagenes/exit.gif")
def mostrarDatos(n):
	conexion = cx_Oracle.connect('ventas/ventas@prod')
	cursor = conexion.cursor()
	cursor.execute("SELECT * FROM CLIENTES where cli_idclie='"+n+"'")
	for i in cursor:
		lblcodigo = Label(contenedor2,text=i[5]).grid(row=0, column=0)
		
def salir():
	vta.quit
	
def buscar():
	_codigo=codigo.get()
	if len(_codigo)< 6 or len(_codigo) > 6:
		tkMessageBox.showerror('Error', 'Tiene que ser 6 caracteres')
	else:
		mostrarDatos(_codigo)
def controlesConsulta():
	label1 = Label(contenedor1, font='{MS Sans Serif} 9 bold', text='CODIGO : ').grid(row=1, column=0)
	_codigo = Entry(contenedor1, font='{MS Sans Serif} 10 bold', width=6, textvariable=codigo,justify=CENTER).grid(row=1, column=1)
	btnSalir = Button(contenedor1, font='{MS Sans Serif} 9 bold', image=imgsalir, command=salir).grid(row=1, column=2)
	btnlimpiar = Button(contenedor1, font='{MS Sans Serif} 9 bold', text='x', command=vta.quit).grid(row=1, column=3)
	

controlesConsulta()
vta.mainloop()
