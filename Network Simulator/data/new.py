from Tkinter import*
import ttk
import Tix
from Tkconstants import *
import pygame
import random
import time
import os
import xlwt
from math import log
import coordinates,adjacent_matrix,cluster,battery,attack
#constant
RADIUS =120
SPEED=.1

#global variable
node_speed=0;
root=0
nodes=12
lamda=1
Ptx=.5
area=0
color=[0]*nodes
POSx=[0]*nodes
POSy=[0]*nodes
sybil_node_x=0
sybil_node_y=0
flag_for_attack=0
power1=[[0 for i in range(nodes)] for y in range(nodes)]
power2=[[0 for i in range(nodes)] for y in range(nodes)]
mobile_matrix=[[0 for i in range(nodes)] for y in range(nodes)]

My=[0]*nodes
header_count=[0]*15
battery_value=[1000]*nodes
clusters=[0]*15
flag=0
collectdetail=0
target=0
show_range=0
flag_for_matrix=0
flag_for_batterystatus=0
clustering=0
t=time.time()
t1=time.time()+2
timeforclustring=time.time()
direction=[time.time()]*nodes
turn=0
clustercount=0
objects=[]
def messages(a):
    global power1,power2,My,battery_value,mobile_matrix,collectdetail
    k=[0]*nodes
    if a==1:
        i=0
        minpower=RADIUS*RADIUS*4*4*(22/7.0)*(22/7.0)
        minpower=1/float(minpower)
        minpower=minpower*Ptx*lamda*lamda
        while i<nodes:
            battery_value[i]-=Ptx
            j=i+1
            power1[i][i]=0
            while j<nodes:
                power1[i][j]=0
                distance=(POSx[i]-POSx[j])**2+(POSy[i]-POSy[j])**2
                distance=distance*4*4*(22/7.0)*(22/7.0)
                if distance>0:
                    power1[i][j]=1/float(distance)
                    power1[i][j]=power1[i][j]*Ptx*lamda*lamda
                if (power1[i][j]>=minpower):
                    battery_value[j]-=(Ptx/5)
                    battery_value[i]-=(Ptx/5)
                power1[j][i]=power1[i][j]
                j+=1
            i+=1
        if flag_for_attack==1:
            i=0
            while i<7:
                j=0
                battery_value[nodes]-=Ptx/(i+1)
                while j<nodes:
                    power1[nodes+i][j]=0
                    distance=(sybil_node_x-POSx[j])**2+(sybil_node_y-POSy[j])**2
                    if distance>0:
                        distance=distance*4*4*(22/7.0)*(22/7.0)
                        power1[nodes+i][j]=1/float(distance)
                        power1[nodes+i][j]=power1[nodes+i][j]*((Ptx*2)/(2*(i+1)))*lamda*lamda
                        if power1[nodes+i][j]>=minpower:
                            battery_value[j]-=Ptx/5
                    power1[j][i+nodes]=power1[nodes+i][j]
                    j+=1
                i+=1
    if a==2:
        i=0
        minpower=RADIUS*RADIUS*4*4*(22/7.0)*(22/7.0)
        minpower=1/float(minpower)
        minpower=minpower*Ptx*lamda*lamda
        while i<nodes:
            battery_value[i]-=Ptx
            j=i+1
            power2[i][i]=0
            mobile_matrix[i][i]=0
            while j<nodes:
                power2[i][j]=0
                mobile_matrix[i][j]=0
                distance=(POSx[i]-POSx[j])**2+(POSy[i]-POSy[j])**2
                p=0
                if distance>0:
                    distance=distance*4*4*(22/7.0)*(22/7.0)
                    power2[i][j]=1/float(distance)
                    p=power2[i][j]=power2[i][j]*Ptx*lamda*lamda
                if (p>=minpower)&(power1[i][j]>=minpower):
                    k[i]+=1
                    k[j]+=1
                    battery_value[j]-=(Ptx/5)
                    battery_value[i]-=(Ptx/5)
                    mobile_matrix[i][j]=10*log((power2[i][j]/float(power1[i][j])),10)
                mobile_matrix[j][i]=mobile_matrix[i][j]
                power2[j][i]=power2[i][j]
                j+=1
            i+=1
        if flag_for_attack==1:
            i=0
            while i<7:
                j=0
                while j<nodes:
                    power2[i+nodes][j]=0
                    mobile_matrix[nodes+i][j]=0
                    distance=(sybil_node_x-POSx[j])**2+(sybil_node_y-POSy[j])**2
                    p=0
                    if distance>0:
                        distance=distance*4*4*(22/7.0)*(22/7.0)
                        power2[i+nodes][j]=1/float(distance)
                        p=power2[i+nodes][j]=power2[nodes+i][j]*((Ptx*2)/(2*(i+1)))*lamda*lamda
                    if (p>=minpower)&(power1[i+nodes][j]>=minpower):
                        k[j]+=1
                        if j==target:
                            power1[nodes+i][j]=power2[nodes+i][j]
                            mobile_matrix[nodes+i][j]=0
                        else:
                            battery_value[j]-=Ptx/5
                            mobile_matrix[nodes+i][j]=10*log((power2[nodes+i][j]/float(power1[nodes+i][j])),10)
                    mobile_matrix[j][i+nodes]=mobile_matrix[i+nodes][j]
                    power2[j][i+nodes]=power2[i+nodes][j]
                    j+=1
                i+=1
        i=0
        n=nodes
        if flag_for_attack==1:
            n=nodes+7
        while i<nodes:
            j=0
            s=0
            My[i]=100
            while j<n:
                s+=(mobile_matrix[i][j])**2
                j+=1
            if k[i]!=0:
                My[i]=s/k[i]
            k[i]=0
            i+=1
        if collectdetail==1:
            book = xlwt.Workbook(encoding="utf-8")
            sheet1 = book.add_sheet("Sheet 1")
            i=0
            sheet1.write(0,0,"NODES")
            while i<n:
                sheet1.write(0,i*2+1,str(i))
                sheet1.write(i*5+3,0,str(i))
                i+=1
            i=0
            while i<n:
                j=0
                while j<n:
                    sheet1.write(i*5+2,j*2+1,power1[i][j])
                    sheet1.write(i*5+3,j*2+1,power2[i][j])
                    sheet1.write(i*5+4,j*2+1,mobile_matrix[i][j])
                    j+=1
                sheet1.write(i*5+3,n*2+1,My[i])
                i+=1
            collectdetail=0
            book.save("detail.xls")
            print "Details Collected check detail.xls file"
class Nodes:
    def __init__(self,node_background=0,x=0):
        self.d1=1;
        self.d2=1;
        self.node=x;
        self.node_bg=node_background;
        self.X=random.randint(0,area)
        self.Y=random.randint(0,area)

    def draw8point(self,X,Y,xc,yc):
        self.node_bg.set_at((X+xc, Y+yc),(200,200,200))
        self.node_bg.set_at((X-xc, Y+yc),(200,200,200))
        self.node_bg.set_at((X+xc, Y-yc),(200,200,200))
        self.node_bg.set_at((X-xc, Y-yc),(200,200,200))
        self.node_bg.set_at((X+yc, Y+xc),(200,200,200))
        self.node_bg.set_at((X-yc, Y+xc),(200,200,200))
        self.node_bg.set_at((X+yc, Y-xc),(200,200,200))
        self.node_bg.set_at((X-yc, Y-xc),(200,200,200))

    def Maliciousnode(self,x1,y1):
        global sybil_node_x,sybil_node_y
        x=0;
        y=RADIUS
        p=1-RADIUS
        global area
        self.X=x1-20
        self.Y=y1-20
        #calculate coordinates
        if self.X<0:
            self.X=0
        if self.Y<0:
            self.Y=0
        if self.Y>area:
            self.Y=area
        if self.X>area:
            self.X=area
        sybil_node_x=self.X
        sybil_node_y=self.Y
        #draw node no
        font=pygame.font.Font(None,22);
        textimg =font.render(str(self.node), 1,(0,0,0), (100,100,100))
        self.node_bg.blit(textimg, (self.X-7,self.Y-7))

    def draw(self,d1,d2,flag):
        x=0;
        y=RADIUS
        p=1-RADIUS
        global area
        #calculate coordinates
        if self.X<0:
            self.X=0
            self.d1=-self.d1
        if self.Y<0:
            self.Y=0
            self.d2=-self.d2
        if self.Y>area:
            self.Y=area
            self.d2=-self.d2
        if self.X>area:
            self.X=area
            self.d1=-self.d1
        if flag==1:
            self.d1=d1
            self.d2=d2
        self.X=self.X+random.randint(0,node_speed)*self.d1;
        self.Y=self.Y+random.randint(0,node_speed)*self.d2;
        POSx[self.node]=self.X;
        POSy[self.node]=self.Y;

        #draw node no
        font=pygame.font.Font(None,22);
        textimg =font.render(str(self.node), 1,color[self.node], (100,100,100))
        self.node_bg.blit(textimg, (self.X-7,self.Y-7))

        #implement circle drawing algorithm
        if (show_range==1)&(clusters[self.node]==1):
            while x<=y:
                x=x+1;
                if p<0:
                    p=p+2*x+1;
                else:
                    y=y-1;
                    p=p+2*(x-y)+1
                self.draw8point(self.X,self.Y,x,y)

def otherapp(node_background):
    global turn,t,t1,clusters,flag_for_attack,target
    global battery_value,color,timeforclustring,clustercount,My,header_count
    #get source and destination node for sending message

    if attack.flag==1:
        target=attack.nodevalue.get()
        flag_for_attack=1
        Malicious=Nodes(objects[target].node_bg,nodes)
        Malicious.Maliciousnode(POSx[target],POSy[target])
        attack.destroy()

    #send coordinates to coordinates module
    if flag==1:
        coordinates.show(POSx,POSy,nodes);

    #show battery Status
    if flag_for_batterystatus==1:
        n=nodes
        if flag_for_attack==1:
            n=nodes+1
        battery.show(battery_value,n)

    #send coordinates to adjacent_matrix module
    if flag_for_matrix==1:
        adjacent_matrix.show(POSx,POSy,nodes,RADIUS)

    # mobility based clustring
    if (t+5<time.time())&(turn==0):
        messages(1);
        t1=time.time()
        turn=1

    if (t1+2<time.time())&(turn==1):
        messages(2)
        t=time.time()
        turn=0

    if clustering==1:
        i=0
        minpower=RADIUS*RADIUS*4*4*(22/7.0)*(22/7.0)
        minpower=1/float(minpower)
        minpower=minpower*Ptx*lamda*lamda
        n=nodes
        if flag_for_attack==1:
            n=nodes+7
        g1=[' ']*n
        vote=[0]*nodes
        clusters=[0]*nodes
        while i<nodes:
            j=0
            while j<nodes:
                distance=(POSx[i]-POSx[j])**2+(POSy[i]-POSy[j])**2
                if (distance<=RADIUS*RADIUS)&(My[j]<My[i]):
                    j=100
                j+=1
            if j<100:
                j=0
                vote[i]=1
                clusters[i]=1
                color[i]=(0,255,0)
                while j<n:
                    if j<nodes:
                        distance=(POSx[i]-POSx[j])**2+(POSy[i]-POSy[j])**2
                        if (distance<=RADIUS*RADIUS):
                            g1[i]=g1[i]+','+str(j)
                            vote[j]=1
                            if i!=j:
                                color[j]=(255,255,255)
                    else:
                        distance=(sybil_node_x-POSx[i])**2+(sybil_node_y-POSy[i])**2
                        power=distance*4*4*(22/7.0)*(22/7.0)
                        if power!=0:
                            power=1/float(power)
                        else:
                            power=0
                        power=power*((Ptx*2)/(2*(j-nodes+1)))*lamda*lamda
                        if (power>=minpower):
                            g1[i]=g1[i]+','+str(j)
                    j+=1
            cluster.show(g1,n)
            i+=1
        i=0
        while i<nodes:
            if vote[i]==0:
                j=0
                vote[i]=1
                clusters[i]=1
                color[i]=(0,255,0)
                while j<n:
                    if j<nodes:
                        distance=(POSx[i]-POSx[j])**2+(POSy[i]-POSy[j])**2
                        if (distance<=RADIUS*RADIUS):
                            g1[i]=g1[i]+','+str(j)
                            vote[j]=1
                    else:
                        distance=(sybil_node_x-POSx[i])**2+(sybil_node_y-POSy[i])**2
                        power=distance*4*4*(22/7.0)*(22/7.0)
                        if power!=0:
                            power=1/float(power)
                        else:
                            power=0
                        power=power*((Ptx*2)/(2*(j-nodes+1)))*lamda*lamda
                        if (power>=minpower):
                            g1[i]=g1[i]+','+str(j)
                    j+=1
            cluster.show(g1,n)
            i+=1
        if (timeforclustring+5<time.time())&(clustercount<50):
            filename =open("clusterdetail71.txt","a")
            filename1 =open("clusterheaddetail7.txt","w")
            i=0
            filename.write("\n")
            while i<n:
                filename.write(str(i))
                filename.write("--->")
                filename.write(str(My[i]))
                filename.write("   ")
                if i<nodes:
                    filename1.write(str(i))
                    filename1.write("--->")
                    filename1.write(str(header_count[i]))
                    filename1.write("\n")
                i+=1
            i=0
            filename.write("\n")
            while i<n:
                if g1[i]!=' ':
                    header_count[i]+=1
                    filename.write(str(i))
                    filename.write("--->")
                    filename.write(g1[i])
                    filename.write("\n")
                i+=1
            filename.write("\n-----------------------------------------\n")
            filename.close
            filename1.close
            clustercount+=1
            timeforclustring=time.time()

class Application(Frame):
    def __init__(self,master=None):
        self.master=master;
    def create(self):

        embed=Frame(self.master,width=area,height=area)
        embed.pack()

        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        self.master.update()

        pygame.init()
        screen=pygame.display.set_mode((area,area))#,pygame.FULLSCREEN)

        #surface for nodes
        node_background=pygame.Surface((area,area))
        node_background.fill((100,100,100))
        screen.blit(node_background,(0,0))
        pygame.display.flip()
        x=500

        #create nodes
        global local_flag,objects
        for x in range (nodes):
            o=Nodes(node_background,x)
            objects.append(o)

        global direction
        while 1:
            node_background.fill((100,100,100))
            i=0
            for o in objects:
                if direction[i]<time.time():
                    o.draw(random.choice([-1,1]),random.choice([-1,1]),1)
                    direction[i]=time.time()+random.randint(3,5)
                else:
                    o.draw(0,0,0)
                i+=1
            otherapp(node_background)
            screen.blit(node_background,(0,0))
            pygame.display.flip()
            time.sleep(SPEED)

            self.master.update()


def coord():
    global flag,flag_for_matrix,clustering,flag_for_batterystatus
    root1=Toplevel(root)
    coordinates.main(root1,nodes)
    flag=1
    flag_for_matrix=0
    flag_for_batterystatus=0
    clustering=0

def transmission_area():
    global show_range
    show_range=(show_range+1)%2

def clust():
    global flag,flag_for_matrix,clustering,flag_for_batterystatus
    root1=Toplevel(root)
    adjacent_matrix.main(root1,nodes)
    flag=0
    flag_for_matrix=1
    flag_for_batterystatus=0
    clustering=0

def clustering():
    global clustering,flag,flag_for_matrix,flag_for_batterystatus
    root1=Toplevel(root)
    n=nodes
    if flag_for_attack==1:
        n=nodes+7
    cluster.main(root1,n)
    clustering=1
    flag=0
    flag_for_matrix=0
    flag_for_batterystatus=0

def Batterystatus():
    global clustering,flag,flag_for_matrix,flag_for_batterystatus,flag_for_attack
    root1=Toplevel(root)
    n=nodes
    if flag_for_attack==1:
        n=nodes+1
    battery.main(root1,n)
    clustering=0
    flag_for_batterystatus=1
    flag=0
    flag_for_matrix=0

def Attack():
    global clustering,flag,flag_for_matrix,flag_for_batterystatus
    root1=Toplevel(root)
    attack.main(root1)
    clustering=0
    flag_for_batterystatus=0
    flag=0
    flag_for_matrix=0

def Collect():
    global collectdetail
    collectdetail=1
def initi(r,node,ar,ptx,Freq,speed):
    global node_speed,root,nodes,direction,POSx,POSy,power1,power2,mobile_matrix,My,battery_value,area,RADIUS,lamda,Ptx,color,clusters
    nodes=node
    node_speed=speed
    root=Tk()
    area=ar
    lamda=float(300/float(Freq))
    Ptx=ptx/1000.0
    RADIUS=area/5
    RADIUS=200
    POSx=[0]*nodes
    POSy=[0]*nodes
    clusters=[0]*nodes
    direction=[time.time()]*nodes
    color=[(255,255,255)]*(nodes+7)
    power1=[[0 for i in range(nodes+7)] for y in range(nodes+7)]
    power2=[[0 for i in range(nodes+7)] for y in range(nodes+7)]
    mobile_matrix=[[0 for i in range(nodes+7)] for y in range(nodes+7)]

    My=[100]*(nodes+7)
    i=0
    while i<3:
        My[nodes+i]=100
        i+=1
    battery_value=[1000]*(nodes+1)

def main(r,node,area,Ptx,Freq,speed):
    r.destroy()
    initi(r,node,area,Ptx,Freq,speed)
    app=Application(master=root)
    app.master.title("simulation")

    menubar=Menu(root)
    filemenu=Menu(menubar)
    filemenu.add_command(label="Coordinate",command=coord)
    filemenu.add_separator()
    filemenu.add_command(label="ADJACENT_MATRIX",command=clust)
    filemenu.add_separator()
    filemenu.add_command(label="Start Clustring",command=clustering)
    filemenu.add_separator()
    filemenu.add_command(label="Battery Status",command=Batterystatus)
    filemenu.add_separator()
    filemenu.add_command(label="Start Attack",command=Attack)
    filemenu.add_separator()
    filemenu.add_command(label="Collect detail",command=Collect)
    filemenu.add_separator()
    filemenu.add_command(label="Exit",command=root.destroy)

    filemenu2=Menu(menubar)
    filemenu2.add_command(label="Transmission_area",command=transmission_area)



    menubar.add_cascade(label="FILE",menu=filemenu)
    menubar.add_cascade(label="EDIT",menu=filemenu2)
    root.config(menu=menubar)
    app.create()
    app.mainloop()
    root.destroy()
if __name__ == '__main__':
     main()
