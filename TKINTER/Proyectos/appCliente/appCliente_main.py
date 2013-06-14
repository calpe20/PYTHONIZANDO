#	Project Name	:	Visual Python IDE for 2.6#	Date	        :	13-12-2009#	Author		    :	macrocoders team#	Contact		    :	macrocoders@gmail.com#	Web			    :	http://visualpython.org#	Python Ver.     :	2.6# -*- coding: utf-8 -*-from Tkinter import * from tkMessageBox import *from AppClientefunciones import *
def saludar():
	tkMessageBox.showinfo('Hola','Hola')# -- Do not change. You may experience problems with the design file. #form1=Tk()form1.title('Saludos')form1.resizable(width=FALSE, height=FALSE)form1.geometry('800x600+100+100')
# -- Do not change. You may experience problems with the design file. ## -- Do not change. You may experience problems with the design file. -- #
label1=Label(text='CODIGO : ', font = '{MS Sans Serif} 11 bold').grid(row=1, column=1)# -- Do not change. You may experience problems with the design file. -- #

textBox1=Entry(font = '{MS Sans Serif} 11 bold', width = 10, justify=CENTER).grid(row = 1, column = 2)
# -- Do not change. You may experience problems with the design file. -- #
button1=Button(text='BUSCAR', font = '{MS Sans Serif} 9 bold', command=saludar).grid(row=1, column=4)
#button1.place(relx=0.5, rely=0.01, relwidth=0.1, relheight=0.05)

# -- Do not change. You may experience problems with the design file. -- #
label2=Label(text='')
label2.place(relx=0., rely=0., relwidth=0., relheight=0.)
#--FRAME
marco1 = Frame(form1, bd=1, relief="groove")
marco1.place(relx=0.005, rely=0.05, relwidth=0.99, relheight=0.9)
#scrollbar = Scrollbar(form1)
#scrollbar.pack(side=RIGHT, fill= Y)
label3=Label(marco1,text='label3').grid(row=1, column=1)
label3=Label(marco1,text='label3').grid(row=1, column=2)
label3=Label(marco1,text='label3').grid(row=1, column=3)
label3=Label(marco1,text='label3').grid(row=1, column=4)
#------------

form1.mainloop()