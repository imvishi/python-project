from Tkinter import*
import ttk
import Tix
from Tkconstants import *

cn=[0]*16
def show (g,node):
    global cn
    i=0
    while i<node:
        cn[i].set(g[i])
        i=i+1
class application(Frame):
    a=1
    def __init__(self,node,master=None):
        Frame.__init__(self,master,relief=RAISED,borderwidth=5,width=100,height=1000)
        self.pack()
        self.master=master
        self.node=node
        self.create()

    def create(self):
        global cn
        i=0
        while i<self.node:
            cn[i]=IntVar()
            i+=1
        Label(self,text="CLUSTERING AND CLUSTER HEAD ",font=("Times", 20, "bold"),bg="grey",fg="black").grid(columnspan=2)
        Label(self,text="CLUSTER HEAD",font=("Times", 20, "bold"),fg="black").grid(row=1,column=0,pady=10)
        Label(self,text="CLUSTER",font=("Times", 20, "bold"),fg="black").grid(row=1,column=1,pady=10)

        i=0;
        while (i<self.node):
            Label(self,text=str(i),font=("Times", 10, "bold"),fg="black",bg='grey',width=20).grid(row=2+i,column=0,pady=5)
            Entry(self,fg="red",textvariable=cn[i],width=40).grid(row=2+i,column=1,pady=5)
            i=i+1
        self.master.update()

def main(root1,node):
    global cn
    cn=[0]*node
    app = application(node,master=root1)
    app.master.title("cluster")

if __name__ == '__main__': main()
