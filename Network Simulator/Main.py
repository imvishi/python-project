from Tkinter import*
import ttk
import Tix
import data.new
from Tkconstants import *
nodes=0
area=0
Ptx=.5
Freq=1
speed=20;
root=Tk()
def fun():
    global nodes,area,Ptx,Freq
    data.new.main(root,int(nodes.get()),int(area.get()),int(Ptx.get()),int(Freq.get()),int(speed.get()))
class application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master,relief=RAISED,borderwidth=5,width=100,height=1000)
        self.pack()
        self.master=master
        self.create()

    def create(self):
        global nodes,area,Ptx,Freq,speed
        nodes=IntVar()
        area=IntVar()
        Ptx=IntVar()
        Freq=IntVar()
        speed=IntVar()

        nodes.set(10)
        area.set(600)
        Ptx.set(500)
        Freq.set(900)
        speed.set(20)
        Label(self,text="SIMULATION PARAMETERS",font=("Times", 20, "bold"),bg="grey",fg="black").grid(row=0,column=1)

        Label(self,text="No of Nodes",font=("Times", 20, "bold"),fg="black").grid(row=1,column=1,pady=10)
        Entry(self,fg="green",textvariable=nodes).grid(row=2,column=1,pady=10)

        Label(self,text="Simulation Area_Side",font=("Times", 20, "bold"),fg="black").grid(row=3,column=1,pady=10)
        Entry(self,fg="green",textvariable=area).grid(row=4,column=1,pady=10)

        Label(self,text="Transmission Power(in mW)",font=("Times", 20, "bold"),fg="black").grid(row=5,column=1,pady=10)
        Entry(self,fg="green",textvariable=Ptx).grid(row=6,column=1,pady=10)

        Label(self,text="Transmission Frequency(in Mhz)",font=("Times", 20, "bold"),fg="black").grid(row=7,column=1,pady=10)
        Entry(self,fg="green",textvariable=Freq).grid(row=8,column=1,pady=10)

        Label(self,text="Speed variation",font=("Times", 20, "bold"),fg="black").grid(row=9,column=1,pady=10)
        Entry(self,fg="green",textvariable=speed).grid(row=10,column=1,pady=10)
        
        self.button=Button(self,text="SUBMIT",command=fun).grid(row=11,column=1,pady=10)
        self.master.update()
def main():
    app = application(master=root)
    app.master.title("Network simulation")
    app.mainloop()
    app.master.maxsize(50,50)
    root.destroy()
if __name__ == '__main__': main()
