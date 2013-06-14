# -*- coding: cp1252 -*-
# -*- coding: utf-8 -*-
 
#Importamos las funciones necesarias
 
from Tkinter import *
from random import randrange
 
#Esta es la funcion mas complicada y sirve para mover la vibora
def desplazamiento():
    global a,b,z,y,lu,lv,puntaje,vibora,j,m
    c=len(vibora)
    c=c-1
    #Cada cuadro contiene las coordenadas de precedentes en la lista (vibora)
    while c!=0 :
        lu[c]=lu[c-1]
        lv[c]=lv[c-1]
        c+=-1
    #Podemos cambiar las coordenadas del primer cuadrado
    lu[0] += a
    lv[0] += b
    c=0
    #Aplicamos las nuevas cordenadas a los cuadrados correspondientes
    while c!=len(vibora):
        can.coords(vibora[c],lu[c],lv[c],lu[c]+10,lv[c]+10)
        c+=1
    c=1
    #Si las coordnadas de la cabeza son iguales a las de otro cuadrado del cuerpo
    #el juego se detiene
    while c!=len(vibora):
        if lu[c]==lu[0] and lv[c]==lv[0]:
            j=1
            puntaje = 'Perdiste con ' + str(puntaje*10) + ' puntos'
            puntajes.set(puntaje)
            break
        c+=1
    #Si la vibora llega a un borde, aparece por el opuesto
    #El valor 'd' se usa para prevenir un error al querer pasar de un lado al otro del canvas
    d=1
    if lu[0]==200:
        lu[0],d=10,0
    if lu[0]==0 and d==1:
        lu[0]=200
    if lv[0]==200:
        lv[0],d=10,0
    if lv[0]==0 and d==1:
        lv[0]=200
        d=0
    #Si la cabeza come un circulo, aparece otro en un punto al azar y se aumenta el puntaje
    if z-7<=lu[0]<=z+7 and y-7<=lv[0]<=y+7:
        puntaje+=1
        puntajes.set(str(puntaje*10))
        criatura()
    if j!=1 and m!=1:
        fen.after(100,desplazamiento)
 
#Esta función crea un círculo de coordenadas múltiplo de 10 para evitar que el círculo sea cortado parcialemente por la vibora
 
def criatura():
    global z,y,n,lu,lv,vibora,a,b
    z=randrange(2,18)
    y=randrange(2,18)
    z = z*10
    y = y*10
    can.coords(circulo,z,y,z+5,y+5)
    #Cada vez que come, se agrega un cuadrado que la hace crecer
    viboras = can.create_rectangle(300,300,310,310,fill='green')
    vibora.append(viboras)
    lu.append(lu[n]+12+a)
    lv.append(lv[n]+12+b)
    n+=1
 
#Estas cuatro funciones permiten el movimiento en cuatro direcciones de la vibora
#Por los sucecivos cambios de direccion del primer cuadrado el valor se graba en b
#La variable s hace quelavibora no se acelere como loca cuando se
#modifica la direccion con o cuando se vuelve a presionar arriba/abajo/izquierda/derecha
 
def izquierda(event):
    global a,b,s
    a=-10
    b=0
    if s==0:
        s=1
        desplazamiento()
 
def derecha(event):
    global a,b,s
    a=10
    b=0
    if s==0:
        s=1
        desplazamiento()
 
def arriba(event):
    global a,b,s
    a=0
    b=-10
    if s==0:
        s=1
        desplazamiento()
 
def abajo(event):
    global a,b,s
    a=0
    b=10
    if s==0:
        s=1
        desplazamiento()
 
#Esta funcion se utiliza para detener la vibora
 
def pausa(event):
    global j,a,b,m,enpausa
    t=0
    if a==b:
        t=1
    if j!=1:
        #Mostrar o borrar el texto 'PAUSA'
        #Y detiene la vibora
        if m!=1:
            m=1
            can.coords(enpausa,100,100)
        else:
            m=0
            can.coords(enpausa,300,300)
            if t!=1:
                desplazamiento()
 
#Esta función restablece todos los valores y vuelve a crear la vibora base y la primera comida
 
def empezar(event):
    global z,y,lu,lv,puntaje,vibora,j,m,s,n,a,b,circulo
    if j!=0:
        print 'El suicidio esta penado!'
    can.delete(ALL)
    s=puntaje=j=m=a=b=0
    z=y=50
    lu,lv,vibora = [100,112],[100,112],[]
    n=1
    cabeza = can.create_rectangle(100,100,110,110,fill='dark green')
    cuadrados = can.create_rectangle(112,100,122,110,fill='green')
    circulo = can.create_oval(z,y,z+5,y+5,fill='red')
    vibora.append(cabeza)
    vibora.append(cuadrados)
    puntajes.set('0')
 
#Definimos los valores iniciales
 
s=puntaje=j=m=t=a=b=0
z=y=50
lu,lv,vibora = [100,112],[100,112],[]
n=1
 
print ' '*30 + "Te moves con las flechas del teclado"
print ' '*30 + "P para poner o sacar la pausa"
print ' '*30 + "Enter para comenzar. No te suicides!"
 
#Se crea un canvas todo gris
 
fen = Tk()
can = Canvas(fen,width = 200, height = 200 , bg = 'gray')
can.grid(row=1,column=0,columnspan=3)
 
enpausa=can.create_text(300,300,text="PAUSA")
 
#Se crea la base de la vibora y la primera comida
 
cabeza = can.create_rectangle(100,100,110,110,fill='dark green')
cuadrados = can.create_rectangle(112,100,122,110,fill='green')
circulo = can.create_oval(z,y,z+5,y+5,fill='red')
 
vibora.append(cabeza)
vibora.append(cuadrados)
 
#Creamos los controles del teclado
 
can.bind_all('<Up>', arriba)
can.bind_all('<Down>', abajo)
can.bind_all('<Left>', izquierda)
can.bind_all('<Right>', derecha)
can.bind_all('<Return>',empezar)
can.bind_all('p',pausa)
 
#La pantalla del puntaje
 
Label(fen, text='Puntaje: ').grid(row=0,column=0)
 
puntajes = StringVar()
Puntaje = Entry(fen, textvariable=puntajes)
Puntaje.grid(row=0,column=1)
puntajes.set('0')
 
fen.mainloop()
