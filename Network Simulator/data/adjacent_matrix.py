from Tkinter import*
import ttk
import Tix
from Tkconstants import *

cn=[[0 for i in range(16)] for y in range(16)]
def show (POSx,POSy,nodes,Radius):
    global cn
    i=0
    while i<nodes:
        j=i
        while j<nodes:
            cn[i][j].set(0)
            cn[j][i].set(0)
            if abs(POSx[i]-POSx[j])<=Radius:
                if abs(POSy[i]-POSy[j])<=Radius:
                    cn[i][j].set(1)
                    cn[j][i].set(1)
            j+=1
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
        global cn
        i=0
        while i<self.node:
            j=0
            while j<self.node:
                cn[i][j]=IntVar()
                j+=1
            i+=1
        self.Label1=Label(self,text="ADJACENT MATRIX",font=("Times", 20, "bold"),bg="grey",fg="black").grid(columnspan=16)
        i=0
        while i<self.node+1:
            j=0
            while j<self.node+1:
                if (i==0)&(j==0):
                    do_nothing=0
                elif i==0:
                    self.Label2=Label(self,text=str(j),font=("Times", 10, "bold"),fg="black",width=0).grid(row=1,column=j+1,pady=8,ipadx=20,sticky=W+E)
                elif j==0:
                    self.Label3=Label(self,text=str(i),font=("Times", 10, "bold"),fg="black",width=0).grid(row=i+2,column=0,pady=8,padx=40)
                else:
                    self.enter=Entry(self,fg="black",textvariable=cn[i-1][j-1],width=10).grid(row=i+2,column=j+1,pady=8,sticky = W)
                j+=1
            i+=1
        self.master.update()

def main(root1,node):
    global cn
    cn=[[0 for i in range(node)] for y in range(node)]
    app = application(node,master=root1)
    app.master.title("Adjacent_Matrix")
    #app.mainloop()
    #app.master.maxsize(50,50)
    #root.destroy()
if __name__ == '__main__': main()
