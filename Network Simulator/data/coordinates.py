from Tkinter import*
import ttk
import Tix
from Tkconstants import *

cn1=[0]*16
cn2=[0]*16
cn3=[0]*16

def show (POSx,POSy,nodes):
    global cn1,cn2,cn3
    i=0
    while i<nodes:
        cn1[i].set(i+1)
        cn2[i].set(POSx[i])
        cn3[i].set(POSy[i])
        i=i+1
class application(Frame):
    a=1
    def __init__(self,nodes,master=None):
        Frame.__init__(self,master,relief=RAISED,borderwidth=5,width=100,height=1000)
        self.pack()
        self.master=master
        self.node=nodes
        self.create()

    def create(self):
        global cn1,cn2,cn3
        i=0
        while i<self.node:
            cn1[i]=IntVar()
            cn2[i]=IntVar()
            cn3[i]=IntVar()
            i=i+1
        self.Label1=Label(self,text="NODES COORDINATES",font=("Times", 20, "bold"),bg="grey",fg="black").grid(row=0,column=1)
        self.Label2=Label(self,text="NODES",font=("Times", 20, "bold"),fg="black").grid(row=1,column=0,pady=10)
        self.Label3=Label(self,text="X AXIS",font=("Times", 20, "bold"),fg="black").grid(row=1,column=1,pady=10)
        self.Label4=Label(self,text="Y AXIS",font=("Times", 20, "bold"),fg="black").grid(row=1,column=2,pady=10)

        i=0;
        while (i<self.node):
            self.enter1 = Entry(self,fg="green",textvariable=cn1[i]).grid(row=2+i,column=0,pady=5)
            self.enter2 = Entry(self,fg="red",textvariable=cn2[i]).grid(row=2+i,column=1,pady=5)
            self.enter3 = Entry(self,fg="green",textvariable=cn3[i]).grid(row=2+i,column=2,pady=5)
            i=i+1
        self.master.update()

def main(root1,nodes):
    print nodes
    global cn1,cn2,cn3
    cn1=[0]*nodes
    cn2=[0]*nodes
    cn3=[0]*nodes

    app = application(nodes,master=root1)
    app.master.title("Coordinates")

if __name__ == '__main__': main()
