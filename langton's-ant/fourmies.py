from tkinter import *
from random import choice


class Interface(Frame):

    def __init__(self,fenetre,**kwargs):
        self.fenetre=fenetre
        Frame.__init__(self,self.fenetre,**kwargs)
        self.pack(fill=BOTH)
        self.fenetre.title('Les fourmies de Langton')
        self.fenetre.bind('<Configure>',self.taille)
        
        self.fra=Frame(self,bd=4,relief=GROOVE)
        self.fra.pack(side=BOTTOM)

        Scale(self.fra,length=100,orient=HORIZONTAL,showvalue=0,from_=1,to=100,command=self.vitesse,
              label='-       Vitesse       +').grid(row=0,column=0)
        Button(self.fra,text='Start',width=8,command=self.start).grid(row=0,column=1,padx=5)
        Button(self.fra,text='Pause',width=8,command=self.pause).grid(row=0,column=2)
        Button(self.fra,text='Reset',width=8,command=self.reset).grid(row=0,column=3,padx=5)
        Button(self.fra,text='Fourmie+',width=8,command=self.addFourmie).grid(row=0,column=4)
        Button(self.fra,text='Quitter',width=8,command=self.fenetre.destroy).grid(row=0,column=5,padx=5)

        self.mouvement=Label(self.fra,text='Nombre de mouvement : 0')
        self.mouvement.grid(row=1,column=0,columnspan=3)
        self.nbrFourmie=Label(self.fra,text='Nombre de fourmie : 0')
        self.nbrFourmie.grid(row=1,column=3,columnspan=3)
        self.fra.pack(pady=5)

        self.height=self.width=0
        self.cadre=Canvas(self,height=self.height,width=self.width,bg='white',bd=2,relief=SUNKEN)
        self.cadre.pack(side=TOP)
        self.cadre.bind('<Button-1>',self.addFourmie)

        self.flag=0
        self.v=100
        self.nbrMouv=0
        self.fourmie=[]

    def taille(self,event):
        self.height=self.fenetre.winfo_height()-self.fra.winfo_height()-5
        self.width=self.fenetre.winfo_width()-5
        self.cadre.configure(height=self.height,width=self.width)

    def start(self):
        if not self.flag and self.fourmie:
            self.flag=1
            self.animation()

    def pause(self):
        if self.flag:
            self.flag=0

    def reset(self):
        del(self.fourmie[:])
        self.cadre.delete(ALL)
        self.flag=0
        self.nbrMouv=0
        self.nbrFourmie.configure(text='Nombre de fourmie : 0')
        self.mouvement.configure(text='Nombre de mouvement : 0')

    def vitesse(self,event):
        self.v=101-int(event)

    def addFourmie(self,event=0):
        if event:
            pX=event.x//5
            pY=event.y//5
        else:
            pX=self.width//10
            pY=self.height//10
        self.fourmie.append(Fourmie(self.cadre,pX,pY,
                                     choice(['red','blue','green','yellow','brown','orange','purple','pink','black','grey'])))
        self.nbrFourmie.configure(text='Nombre de fourmie : {}'.format(len(self.fourmie)))

    def animation(self):
        for fourmie in self.fourmie:
            pX=fourmie.getX()
            pY=fourmie.getY()
            objets=self.cadre.find_enclosed(pX*5,pY*5,(pX+1)*5,(pY+1)*5)
            sur_une_case=False
            for objet in objets:
                if self.cadre.type(objet)=='rectangle':
                    sur_une_case=True
                    case=objet
                    break
            if not sur_une_case:
                case=self.cadre.create_rectangle(pX*5,pY*5,(pX+1)*5,(pY+1)*5,
                                                  width=0,fill='white',tags='white')
            fourmie.orientation(case)
            fourmie.bouge()
        self.nbrMouv+=1
        self.mouvement.configure(text='Nombre de mouvement : {}'.format(self.nbrMouv))
        if self.flag:
            self.fenetre.after(self.v,self.animation)


class Fourmie():

    def __init__(self,cadre,posX,posY,couleur):
        self.cadre=cadre
        self.posX=posX
        self.posY=posY
        self.dx=0
        self.dy=1
        self.couleur=couleur
        self.fourmie=cadre.create_oval(posX*5,posY*5,(posX+1)*5,(posY+1)*5,fill=couleur,tags='h')

    def getX(self):
        return self.posX

    def getY(self):
        return self.posY

    def bouge(self):
        self.posX+=self.dx
        self.posY+=self.dy
        self.cadre.coords(self.fourmie,self.posX*5,self.posY*5,(self.posX+1)*5,(self.posY+1)*5)
        self.cadre.lift(self.fourmie)

    def orientation(self,case):
        tagF=self.cadre.gettags(self.fourmie)[0]
        tagC=self.cadre.gettags(case)[0]
        if tagF=='h':
            if tagC=='white':
                self.dx=1; self.dy=0
                self.cadre.itemconfigure(self.fourmie,tags='d')
                self.cadre.itemconfigure(case,tags=self.couleur,fill=self.couleur)
            else:
                self.dx=-1; self.dy=0
                self.cadre.itemconfigure(self.fourmie,tags='g')
                self.cadre.itemconfigure(case,tags='white',fill='white')
        elif tagF=='b':
            if tagC=='white':
                self.dx=-1; self.dy=0
                self.cadre.itemconfigure(self.fourmie,tags='g')
                self.cadre.itemconfigure(case,tags=self.couleur,fill=self.couleur)
            else:
                self.dx=1; self.dy=0
                self.cadre.itemconfigure(self.fourmie,tags='d')
                self.cadre.itemconfigure(case,tags='white',fill='white')
        elif tagF=='d':
            if tagC=='white':
                self.dx=0; self.dy=-1
                self.cadre.itemconfigure(self.fourmie,tags='b')
                self.cadre.itemconfigure(case,tags=self.couleur,fill=self.couleur)
            else:
                self.dx=0; self.dy=1
                self.cadre.itemconfigure(self.fourmie,tags='h')
                self.cadre.itemconfigure(case,tags='white',fill='white')
        elif tagF=='g':
            if tagC=='white':
                self.dx=0; self.dy=1
                self.cadre.itemconfigure(self.fourmie,tags='h')
                self.cadre.itemconfigure(case,tags=self.couleur,fill=self.couleur)
            else:
                self.dx=0; self.dy=-1
                self.cadre.itemconfigure(self.fourmie,tags='b')
                self.cadre.itemconfigure(case,tags='white',fill='white')



if __name__=='__main__':
    f=Tk()
    interface=Interface(f)
    f.geometry('500x500')
    f.mainloop()