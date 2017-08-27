from Tkinter import*
import ttk
import Tix
from Tkconstants import *
nodevalue=0
flag=0
root=0
def fun():
    global nodevalue
    global flag
    flag=1
def destroy():
    global root
    root.destroy()
class application(Frame):
    a=1
    def __init__(self,master=None):
        Frame.__init__(self,master,relief=RAISED,borderwidth=5,width=100,height=1000)
        self.pack()
        self.master=master
        self.create()

    def create(self):
        global nodevalue
        nodevalue=IntVar()
        Label(self,text="ENTER TARGET NODES",font=("Times", 20, "bold"),bg="grey",fg="black").grid(row=0,column=1)
        Entry(self,fg="green",textvariable=nodevalue).grid(row=1,column=1)
        Button(self,text="SUBMIT",command=fun).grid(row=3,column=1)
        self.master.update()

def main(root1):
    global root
    root=root1
    app = application(master=root)
    app.master.title("Attack")

if __name__ == '__main__': main()
