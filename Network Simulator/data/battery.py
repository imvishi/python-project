from Tkinter import*
import ttk
import Tix
from Tkconstants import *
app=0
def show (v1,node):
    global app
    i=0
    while i<node:
        app.v[i].set(v1[i])
        i+=1
class application(Frame):
    a=1
    def __init__(self,node,master=None):
        Frame.__init__(self,master,relief=RAISED,borderwidth=5,width=100,height=1000)
        self.pack()
        self.master=master
        self.node=node
        self.v=[0]*node
        self.create()

    def create(self):
        i=0
        while i<self.node:
            i=i+1
            self.v[i-1]=IntVar()
        Label(self,text="BATTERY STATUS",font=("Times", 20, "bold"),bg="grey",fg="black").grid(row=0,column=1)
        Label(self,text="NODES",font=("Times", 20, "bold"),fg="black").grid(row=1,column=0,pady=10)
        Label(self,text="BATTERY",font=("Times", 20, "bold"),fg="black").grid(row=1,column=1,pady=10)
        Label(self,text="In mAh",font=("Times", 20, "bold"),fg="black").grid(row=1,column=2,pady=10)
        i=0;
        while (i<self.node):
            Label(self,text=str(i),font=("Times", 10, "bold"),fg="black",bg='grey',width=10).grid(row=2+i,column=0,pady=5)
            ttk.Progressbar(self, orient="horizontal", mode="determinate",length=200,maximum=1000,variable=self.v[i]).grid(row=2+i,column=1,pady=5)
            Entry(self,fg="red",textvariable=self.v[i]).grid(row=2+i,column=2,pady=5)
            i=i+1
        self.master.update()

def main(root1,nodes):
    global app
    app = application(nodes,master=root1)
    app.master.title("battery status")
if __name__ == '__main__': main()
