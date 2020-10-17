from tkinter import *
from PIL import Image, ImageTk
import pygame 
from tkinter import messagebox
from tkinter import filedialog

class ReproductorMusical:

    def __init__(self, master):
        self.master = master
        master.title("Reproductor Musical")
        master.geometry("550x225")
        
        self.cancion=IntVar()
        self.cancion.set(1)
        self.estado=StringVar()
        self.estado.set("Detenido")
        self.filename=StringVar()
        self.filename.set("archivo")
        self.Lista_canciones=[]
        
        #Inicializando pygame mixer 
        pygame.mixer.init()
        
        #Imagen del reproductor
        self.caratula=ImageTk.PhotoImage(Image.open('Canciones/caratula.jpg'))
        self.my_label=Label(image=self.caratula)
        self.my_label.grid(row=0,column=0)

        #Creacion de frames para elementos
        self.frame1=Frame(master)
        self.frame1.grid(row=0,column=1)
        self.frame2=Frame(master)
        self.frame2.grid(row=0,column=2)
        
        #Creando Listbox
        self.listaCanciones=Listbox(self.frame2,bd=4,height=7)
        self.listaCanciones.grid(row=1,column=1)
        
        
        #Creando Scrollbar para listbox
        self.scroll=Scrollbar(self.frame2,orient=VERTICAL)
        self.scroll.grid(row=1,column=2,sticky=S+N)

        #Creacion de Status bar
        self.status=Label(master,text="Satus: Reproductor detenido",bd=1,relief=SUNKEN,anchor=E)
        self.status.grid(row=1,column=0,columnspan=4,sticky=W+E)

        #Definiendo que pasa cuando se presionan los botones
        self.boton_reproducir=Button(self.frame1,text="Reproducir",padx=30,pady=9,bd=5,command=self.ReproducirCancion)
        self.boton_detener=Button(self.frame1,text="Detener",padx=38,pady=9,bd=5,command=self.DetenerCancion)
        self.boton_pausar=Button(self.frame1,text="Pausar/Reanudar",padx=13,pady=9,bd=5,command=self.PausarReanudar)
        self.boton_salir=Button(self.frame1,text="Salir del reproductor",padx=5,pady=9,bd=5, command=root.quit)
        self.agregar=Button(self.frame2,text="Agregar Cancion",padx=14,pady=2,bd=5,command=self.AgregarCancion)
        self.eliminar=Button(self.frame2,text="Eliminar Cancion",padx=14,pady=2,bd=5,command=self.EliminarCancion)

        #Ubicando los botones en la pantalla
        self.boton_reproducir.grid(row=0,column=1)
        self.boton_detener.grid(row=1,column=1)
        self.boton_pausar.grid(row=2,column=1)
        self.boton_salir.grid(row=3,column=1)
        self.agregar.grid(row=0,column=1)
        self.eliminar.grid(row=2,column=1)
        
        #Configuracion de scrollbar
        self.listaCanciones.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.listaCanciones.yview)
        
    def AgregarCancion(self):
        self.filename=filedialog.askopenfilename(initialdir="Canciones/",title="select a file",filetypes=(("ogg files","*.ogg"),("mp3 files","*.mp3"),("mp4 files","*.mp4"),("all files","*.*")))
        self.cancion =pygame.mixer.Sound(self.filename)
        self.Lista_canciones.append(self.cancion)
        self.listaCanciones.insert(self.listaCanciones.size()+1,"Cancion "+str(self.listaCanciones.size()+1))
        self.listaCanciones.select_set(0)
       

    def EliminarCancion(self):
        if self.listaCanciones.size()>0:
            self.cancion=self.Lista_canciones[(self.listaCanciones.curselection())[0]]
            self.Lista_canciones.remove(self.cancion)
            self.listaCanciones.delete(self.listaCanciones.curselection())
            self.listaCanciones.select_set(0)

    def ReproducirCancion(self):
        if self.listaCanciones.size()>0:
            if self.estado.get()=="Detenido":           
                self.Lista_canciones[(self.listaCanciones.curselection())[0]].play()
                self.estado.set("Reproduciendo")
                self.StatusBar()
            else:
                pygame.mixer.stop()
                self.Lista_canciones[(self.listaCanciones.curselection())[0]].play()
                self.estado.set("Reproduciendo")
                self.StatusBar()
            
    def DetenerCancion(self):
        pygame.mixer.stop()
        self.estado.set("Detenido")
        self.StatusBar()

    def PausarReanudar(self):
        if self.estado.get()=="Reproduciendo":
            pygame.mixer.pause()
            self.estado.set("En pausa")
            self.StatusBar()
        else:
            if self.estado.get()=="En pausa":
                pygame.mixer.unpause()
                self.estado.set("Reproduciendo")
                self.StatusBar()
    
    #Funcion creada para actualizar el status en la barra inferior cada vez que se presiona un boton
    def StatusBar(self):
        status=Label(text="Satus:  "+ self.estado.get(),bd=1,relief=SUNKEN,anchor=E)
        status.grid(row=1,column=0,columnspan=4,sticky=W+E)

root= Tk()
Mi_Reproductor= ReproductorMusical(root)
root.mainloop()