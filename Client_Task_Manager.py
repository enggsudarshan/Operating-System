"""
CSC 239 Assignment - 1
Author: Sudarshan Deo
Spring 2017

This file runs on client side and is used to display server data on GUI

"""

import pickle
import sys
import socket
import time
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from threading import Timer
import sys
from tkinter import font
import os
import pwd
import os.path
import matplotlib
matplotlib.use("TkAgg")  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure 
import tkinter as tk
from tkinter import ttk
import matplotlib.animation as animation
from matplotlib import style
from operator import itemgetter
from mpl_toolkits.mplot3d import axes3d
import subprocess
import math
import heapq
import copy

##Declarations for CPU
list1={}
list2={}
list3=[]
prev_list={}

curr_list={}
prevIntr=prevContext=0

##Declarations for Memory
list4={}
list4_2={}
list5=[]
mem_util=[0]*8

##Declarations for I/O
list6={}
list7=[]
prev_disk_util={}
curr_disk_util={}

##Declarations for Network
list8={}
list9 = {}
list10 = {}
list11 = {}
list12 = []
list13 = []
list14 = []
list15 = []
list16 = []
prev_tcp_util = {}
curr_tcp_util = {}
prev_udp_util = {}
curr_udp_util = {}
prev_ip_util = {}
curr_ip_util = {}
prev_nw_speed = {}
curr_nw_speed = {}

tcp=0
udp=0
ip=0
count=0

##Declarations for Process

prev_process_list = {}
curr_temp_list=[]
curr_process_list = []
temp_list = []

#Fonts
Font = ("Times New Roman", 20, "bold","italic")
Font1 = ("Times New Roman", 16,"bold")
Font2 = ("Times New Roman", 14,"bold")
Font3= ("Times New Roman", 14)
Font4= ("Times New Roman", 11)
Font5 = ("Times New Roman", 18, "bold","italic")

#TCP Information
TCP_IP = '127.0.0.1'
TCP_PORT = 6013
BUFFER_SIZE = 4096

                                ##################################Section for CPU Graph Begins##################################

f1=Figure(figsize=(6,4), dpi=80)
#a=f.add_subplot(111,projection='3d',facecolor='lightyellow')
a=f1.add_subplot(111,facecolor='lightyellow')
#a.set_axis_bgcolor('lightyellow')
f1.suptitle('CPU Utilization', fontsize=14, fontweight='bold',color='black')
f1.subplots_adjust(top=0.85)
n=0
xlist=[]
ylist=[]
y1list=[]

def CPU_Graph_Layout(i):
    
    global n,xlist,ylist,y1list
    xlist.append(n)
    ylist.append(curr_list["cpu"][1])
    n=n+1
    if(len(xlist)==30):     #Reset the graph after 30 seconds
        xlist=xlist[20:]
        ylist=ylist[20:]
    a.clear()

    a.set_xlabel('Time(Sec)',fontweight='bold',fontsize = 12)
    a.set_ylabel('%CPU',fontweight='bold',fontsize = 12)
    a.set_ylim([0,100])
    a.plot(xlist,ylist,'r',label='CPU-Utilization')
    a.legend(loc='upper left',facecolor='lightgreen',fontsize = 12)

                                ##################################Section for CPU Graph Ends##################################


                                ##################################Section for Memory Graph Begins##################################                             
fig_memory=Figure(figsize=(8,4), dpi=80)
a1=fig_memory.add_subplot(111,facecolor='lightyellow')
fig_memory.suptitle('Memory Utilization', fontsize=14, fontweight='bold',color='black')
fig_memory.subplots_adjust(top=0.85)

n_1=0
mem_xlist=[]
mem_availlist=[]
mem_freelist=[]
mem_cachedlist=[]


def Memory_Graph_Layout(i):
    
    global n_1,mem_xlist,mem_availlist,mem_freelist,mem_cachedlist
    mem_xlist.append(n_1)
    mem_freelist.append((int(mem_util[5])/int(mem_util[4]))*100)
    mem_availlist.append((int(mem_util[6])/int(mem_util[4]))*100)
    mem_cachedlist.append((int(mem_util[7])/int(mem_util[4]))*100)
    
    n_1=n_1+1
    if(len(mem_xlist)==30):     #Reset the graph after 30 seconds
        mem_xlist=mem_xlist[10:]
        mem_freelist=mem_availlist[10:]
        mem_availlist=mem_availlist[10:]
        mem_cachedlist=mem_availlist[10:]

    a1.clear()
    a1.set_xlabel('Time(Sec)',fontweight='bold',fontsize = 12)
    a1.set_ylabel('%Mem',fontweight='bold',fontsize = 12)
    a1.set_ylim([0,100])
    a1.plot(mem_xlist,mem_freelist,'r',label='% Free Memory')
    a1.plot(mem_xlist,mem_availlist,'g',label='% Avail Memory')
    a1.plot(mem_xlist,mem_cachedlist,'b',label='% Cached Memory')
    a1.legend(loc='upper left',facecolor='lightgreen',fontsize = 12)

                                ##################################Section for Memory Graph Ends##################################


                                ##################################Section for Disk I/O Graph Begins##################################

fig_diskio=Figure(figsize=(7,4), dpi=90)
a2=fig_diskio.add_subplot(111,facecolor='lightyellow')
fig_diskio.suptitle('Disk I/O Utilization', fontsize=14, fontweight='bold',color='black')
fig_diskio.subplots_adjust(top=0.85)

n_2=0
diskio_xlist=[]
diskio_diskread=[]
diskio_diskwrite=[]
diskio_blockread=[]
diskio_blockwrite=[]


def DiskIO_Graph_Layout(i):
    
    global n_2,diskio_xlist,diskio_diskread,diskio_diskwrite,diskio_blockread,diskio_blockwrite
    diskio_xlist.append(n_2)
    diskio_diskread.append(curr_disk_util["sda"][0])
    diskio_diskwrite.append(curr_disk_util["sda"][2])
    diskio_blockread.append(curr_disk_util["sda"][1])
    diskio_blockwrite.append(curr_disk_util["sda"][3])

    n_2=n_2+1
    if(len(diskio_xlist)==30):     #Reset the graph after 30 seconds
        diskio_xlist=diskio_xlist[10:]
        diskio_diskread=diskio_diskread[10:]
        diskio_diskwrite=diskio_diskwrite[10:]
        diskio_blockread=diskio_blockread[10:]
        diskio_blockwrite=diskio_blockwrite[10:]

    a2.clear()
    a2.set_xlabel('Time(Sec)',fontweight='bold')
    a2.set_ylabel('%Disk',fontweight='bold')
    a2.set_ylim([0,1000])
    a2.plot(diskio_xlist,diskio_diskread,'r',label='Disk Read')
    a2.plot(diskio_xlist,diskio_diskwrite,'g',label='Disk Write')
    a2.plot(diskio_xlist,diskio_blockread,'b',label='Block Read')
    a2.plot(diskio_xlist,diskio_blockwrite,'m',label='Block Write')
    a2.legend(loc='upper left',facecolor='lightgreen',fontsize = 12)

                                ##################################Section for Disk I/O Graph Ends##################################

                                ##################################Section for Network TCP Graph Begins##################################

fig_network_tcp=Figure(figsize=(5,4), dpi=50)
a3=fig_network_tcp.add_subplot(111,facecolor='lightyellow')
fig_network_tcp.suptitle('TCP Packets', fontsize=14, fontweight='bold',color='black')
fig_network_tcp.subplots_adjust(top=0.85)

n_3=0
network_tcp_xlist=[]
tcp_packets_sent=[]
tcp_packets_rec=[]



def Network_TCP_Graph_Layout(i):
    
    global n_3,network_tcp_xlist,tcp_packets_sent,tcp_packets_rec
    network_tcp_xlist.append(n_3)
    tcp_packets_sent.append(curr_tcp_util[tcp][1])
    tcp_packets_rec.append(curr_tcp_util[tcp][0])

    n_3=n_3+1
    if(len(network_tcp_xlist)==30):     #Reset the graph after 30 seconds
        network_tcp_xlist=network_tcp_xlist[10:]
        tcp_packets_sent=tcp_packets_sent[10:]
        tcp_packets_rec=tcp_packets_rec[10:]

    a3.clear()
    a3.set_xlabel('Time(Sec)',fontweight='bold')
    a3.set_ylabel('Rate',fontweight='bold')
    a3.set_ylim([0,10])
    a3.plot(network_tcp_xlist,tcp_packets_sent,'r',label='TCP Packets Sent')
    a3.plot(network_tcp_xlist,tcp_packets_rec,'g',label='TCP Packets Received')

    a3.legend(loc='upper left',facecolor='lightgreen',fontsize = 12)

                                ##################################Section for Network TCP Graph Ends##################################
                                
                                ##################################Section for Network UDP Graph Begins##################################                                

fig_network_udp=Figure(figsize=(5,4), dpi=50)
a4=fig_network_udp.add_subplot(111,facecolor='lightyellow')
fig_network_udp.suptitle('UDP Packets', fontsize=14, fontweight='bold',color='black')
fig_network_udp.subplots_adjust(top=0.85)

n_4=0
network_udp_xlist=[]
udp_packets_sent=[]
udp_packets_rec=[]



def Network_UDP_Graph_Layout(i):
    
    global n_4,network_udp_xlist,udp_packets_sent,udp_packets_rec
    network_udp_xlist.append(n_4)
    udp_packets_sent.append(curr_udp_util[udp][1])
    udp_packets_rec.append(curr_udp_util[udp][0])

    n_4=n_4+1
    if(len(network_udp_xlist)==30):     #Reset the graph after 30 seconds
        network_udp_xlist=network_udp_xlist[10:]
        udp_packets_sent=udp_packets_sent[10:]
        udp_packets_rec=udp_packets_rec[10:]

    a4.clear()
    a4.set_xlabel('Time(Sec)',fontweight='bold')
    a4.set_ylabel('Rate',fontweight='bold')
    a4.set_ylim([0,10])
    a4.plot(network_udp_xlist,udp_packets_sent,'r',label='UDP Packets Sent')
    a4.plot(network_udp_xlist,udp_packets_rec,'g',label='UDP Packets Received')

    a4.legend(loc='upper left',facecolor='lightgreen',fontsize = 12)

                                ##################################Section for Network UDP Graph Ends##################################


                                ##################################GUI for CPU Begins##################################

def CPU_Graph_Design():
    global graphlabel
    graphlabel=Label(tab_for_CPU,text="CPU Data",relief=RAISED,anchor=CENTER, font=Font2)
    graphlabel.grid(row=9,column=2,rowspan=5,columnspan=int(1),sticky=(N,S,W,E))
    canvas=FigureCanvasTkAgg(f1,graphlabel)
    canvas.show()
    canvas.get_tk_widget().pack(side=RIGHT,fill=BOTH,expand=True)
    
    

def CPU_Design():
    with open('data.pickle', 'rb') as pickle_in:
        f = pickle.load(pickle_in)  
        
    for line in f:
        if 'vendor_id' in line.split():
            lcpuinfo1=line.split()
            vendor=lcpuinfo1[2]
        if 'model_name' in line.split():
            lcpuinfo2=line.split()
            model=lcpuinfo2[2]  
        if 'No_of_cores' in line.split():
            lcpuinfo3=line.split()
            cores=lcpuinfo3[2]
            break
    #print(vendor)
    #print(model)
    #print(cores)
    Label(tab_for_CPU,text="CPU Statistics",relief=RAISED,anchor=CENTER, font=Font).grid(row=0,column=0,rowspan=1,columnspan=15,sticky=(N,S,W,E))

    list1=["CPU's","CPU Utilization", "CPU % in User Mode", "CPU% in Kernel Mode","Min CPU Utilization", "Max CPU Utilization","Avg CPU Utilization"]
    c=0
    r=1
    for item in list1:
        Label(tab_for_CPU,text=item,relief=RAISED,anchor=W, font=Font1).grid(row=r,column=c,sticky=(N,S,W,E))
        r=r+1

    c=1
    r=1
    i=0
    for item in range(7*(int(cores)+1)):
        list3.append(Label(tab_for_CPU,text=item,anchor=CENTER,font=Font2, relief=SUNKEN))
        list3[i].grid(row=r,column=c,sticky=(S,N,E,W))  
        if(r==7):
            r=0
            c=c+1
        r=r+1
        i=i+1
        
    Label(tab_for_CPU,text="CPU Information",relief=RAISED,anchor=CENTER, font=Font).grid(row=8,column=0,rowspan=1,columnspan=2,sticky=(N,S,W,E))
    
    r=9
    c=0
    list2=["CPU Vendor","Model Name","CPU Cores","Interrupts/sec","Context Switches/sec"]
    for item in list2:
        Label(tab_for_CPU,text=item,relief=RAISED,anchor=W,font=Font1).grid(row=r,column=0,sticky=(N,S,W,E))
        r=r+1
        
    Label(tab_for_CPU,text=vendor,relief=RAISED,anchor=CENTER, font=Font2).grid(row=9,column=1,sticky=(N,S,W,E))
    Label(tab_for_CPU,text=model,relief=RAISED,anchor=CENTER, font=Font2).grid(row=10,column=1,sticky=(N,S,W,E))
    Label(tab_for_CPU,text=cores,relief=RAISED,anchor=CENTER, font=Font2).grid(row=11,column=1,sticky=(N,S,W,E))
    
    global label_context,label_interrupt
    label_interrupt = Label(tab_for_CPU,text="",relief=RAISED,anchor=CENTER, font=Font2)
    label_interrupt.grid(row=12,column=1,sticky=(N,S,W,E))
    label_context = Label(tab_for_CPU,text="",relief=RAISED,anchor=CENTER, font=Font2)
    label_context.grid(row=13,column=1,sticky=(N,S,W,E))
    
    Label(tab_for_CPU,text="CPU Graph",relief=RAISED,anchor=CENTER, font=Font).grid(row=8,column=2,rowspan=1,columnspan=int(cores),sticky=(N,S,W,E))
    
                                ##################################GUI for CPU Ends##################################

                                ##################################CPU Calculations Begins##################################

def CPU_Calculations(): 
    with open('data.pickle', 'rb') as pickle_in:
        f = pickle.load(pickle_in)  
    
    for line in f:
        global prevIntr,prevContext
        if "cpu" in line:
            cpu=line.split()[0]
            #print(cpu)
            if cpu in prev_list:
                curr_cpu_list = line.split()
                prevUser = int(prev_list[cpu][1])
                prevSys = int(prev_list[cpu][3])
                prevIdle = int(prev_list[cpu][4])
                
                currUser = int(curr_cpu_list[1])
                currSys = int(curr_cpu_list[3])
                currIdle = int(curr_cpu_list[4])
                
                delta = (currUser - prevUser) + (currSys - prevSys)
                
                TotalTime = delta + (currIdle - prevIdle)
                
                CPUUtilization = (delta*100)/TotalTime
    
                curr_list[cpu][0] = curr_cpu_list[0].upper()
                curr_list[cpu][1] = round(CPUUtilization,3)  ##Overall CPU Utilization
                curr_list[cpu][2] = round((((currUser-prevUser)/TotalTime)*100),3)  ##User Mode  in %  
                curr_list[cpu][3] = round((((currSys-prevSys)/TotalTime)*100),3)  ##System Mode in %  
                
                
                if(curr_list[cpu][1]< curr_list[cpu][4]):  #Min CPU Util
                    curr_list[cpu][4]=curr_list[cpu][1]

                if(curr_list[cpu][1]>curr_list[cpu][5]):   # Max CPU Util
                    curr_list[cpu][5]=curr_list[cpu][1]
     
                ##Avg CPU Util Calculation
                curr_list[cpu][6]=round((curr_list[cpu][6]+CPUUtilization)/2,3)            
                
       
                prev_list[cpu][0] = curr_list[cpu][0]
                prev_list[cpu][1] = prevUser
                prev_list[cpu][3] = prevSys
                prev_list[cpu][4] = prevIdle

            else:
                tmplist=line.split()
                prev_list[cpu] = []
                prev_list[cpu].append(0)
                prev_list[cpu].append(tmplist[1])
                prev_list[cpu].append(0)
                prev_list[cpu].append(tmplist[3])
                prev_list[cpu].append(tmplist[4])
                prev_list[cpu].append(0)
                prev_list[cpu].append(0)
                curr_list[cpu]=[]
                curr_list[cpu]=[0,0,0,0,100,0,0]
              
    i=0
    with open('data.pickle', 'rb') as pickle_in:
        f = pickle.load(pickle_in) 
    
    for line in f:
        if "cpu" in line:
            cpu = line.split()[0]
            if cpu in curr_list:
                for item in curr_list[cpu]:
                    list3[i].configure(text=item)
                    i=i+1  
                    
        if "intr" in line:
            listIntr=line.split()
            currIntr=int(listIntr[1])
            TotalIntr=round((currIntr-prevIntr)/3)
            prevIntr=currIntr
            label_interrupt.configure(text=TotalIntr)       
                   
        if "ctxt" in line:
            listContext=line.split()
            currContext=int(listContext[1])
            TotalContext=round((currContext-prevContext)/3)
            prevContext=currContext
            label_context.configure(text=TotalContext)
  
    t=Timer(3,CPU_Calculations)
    t.start()

                                ##################################CPU Calculations End##################################
                                
                                ##################################GUI for Memory Begins##################################
def Memory_Design():

     
    Label(tab_for_Memory,text="Memory Utilization",relief=RAISED,anchor=CENTER, font=Font).grid(row=0,column=0,rowspan=1,columnspan=8,sticky=(N,S,W,E))    
    
    
    list4=["Memory Util","Min Mem Util", "Max Mem Util", "Avg Mem Util"]
    r=1
    c=0
    for item in list4:
        Label(tab_for_Memory,text=item,relief=RAISED,anchor=CENTER, font=Font1).grid(row=r,column=c,rowspan=1,columnspan=1,sticky=(N,S,W,E))
        c=c+1
          
    list4_2=["Total Memory","Free Memory","Available Memory","Cached Memory"]
    c=0
    r=3
    for item in list4_2:
        Label(tab_for_Memory,text=item,relief=RAISED,anchor=CENTER, font=Font1).grid(row=r,column=c,sticky=(N,S,W,E))
        c=c+1
    
    r=2
    c=0
    i=0
    for item in range(8):
        list5.append(Label(tab_for_Memory,text=item,anchor=CENTER,font=Font2, relief=SUNKEN))
        list5[i].grid(row=r,column=c,sticky=(S,N,E,W))  
        if(c==3):
            c=-1
            r=r+2
        c=c+1
        i=i+1
    Label(tab_for_Memory,text="Memory Graph",relief=RAISED,anchor=CENTER, font=Font).grid(row=5,column=0,rowspan=1,columnspan=8,sticky=(N,S,W,E))         
    memorylabel=Label(tab_for_Memory,text="Memory Data",relief=RAISED,anchor=CENTER, font=Font2)
    memorylabel.grid(row=6,column=0,rowspan=5,columnspan=int(4),sticky=(N,S,W,E))
    
    canvas=FigureCanvasTkAgg(fig_memory,memorylabel)    
    canvas.show()    
    canvas.get_tk_widget().pack(side=RIGHT,fill=BOTH,expand=True)

                                ##################################GUI for Memory Ends##################################


                                ##################################Memory Calculations Begin##################################

def Memory_Calculations():
    global list5
    with open('data.pickle2', 'rb') as pickle_in:
        f = pickle.load(pickle_in)  
        
    for line in f:
        if 'MemTotal' in line:
            mem_util[4]=line.split()[1] 
        if 'MemFree' in line:
            mem_util[5]=line.split()[1]
        if 'MemAvailable' in line:
            mem_util[6]=line.split()[1]
        if 'Cached' in line:
            mem_util[7]=line.split()[1]
            break

    MemUtilization=(int(mem_util[4])-int(mem_util[5]))*100/int(mem_util[4])
    mem_util[0]=round(MemUtilization,2)
        
    if (mem_util[0]< mem_util[1]):
        mem_util[1]=mem_util[0]

    if (mem_util[0]>mem_util[2]):
        mem_util[2]=mem_util[0]
        
    AvgMemUtilization= (int(mem_util[3])+int(mem_util[0]))/2
    mem_util[3]=round(AvgMemUtilization,2)
    
    for i in range(8):
        list5[i].configure(text=mem_util[i])

    t = Timer(3,Memory_Calculations)
    t.start()

                                ##################################Memory Calculations End##################################
                                

                                ##################################GUI for Disk I/O Begin##################################
def IO_Design():
    
    Label(tab_for_DiskIO,text="I/O Utilization",relief=RAISED,anchor=CENTER, font=Font).grid(row=0,column=0,rowspan=1,columnspan=10,sticky=(N,S,W,E)) 
    list6=["Disk Reads","Blocks Read","Disk Writes","Blocks Written", "Avg Disk Reads", "Avg Blocks Read","Avg Disk Writes","Avg Blocks Written","Avg Response Time","% Utilization"]
    c=0
    r=1
    for item in list6:
        Label(tab_for_DiskIO,text=item,relief=RAISED,anchor=CENTER, font=Font1).grid(row=r,column=c,sticky=(N,S,W,E))
        c=c+1
        if(c==5):
            c=0
            r=r+2
    
    r=2
    c=0
    i=0
    for item in range(10):
        list7.append(Label(tab_for_DiskIO,text=item,anchor=CENTER,font=Font2, relief=SUNKEN))
        list7[i].grid(row=r,column=c,sticky=(S,N,E,W))  
        if(c==4):
            c=-1
            r=r+2
        c=c+1
        i=i+1
    
    Label(tab_for_DiskIO,text="Disk Graph",relief=RAISED,anchor=CENTER, font=Font).grid(row=5,column=0,rowspan=1,columnspan=8,sticky=(N,S,W,E))     
         
    diskiolabel=Label(tab_for_DiskIO,text="DiskIO Data",relief=RAISED,anchor=CENTER, font=Font2)
    diskiolabel.grid(row=6,column=0,rowspan=5,columnspan=int(4),sticky=(N,S,W,E))
    canvas=FigureCanvasTkAgg(fig_diskio,diskiolabel)
    canvas.show()
    canvas.get_tk_widget().pack(side=RIGHT,fill=BOTH,expand=True)

                                ##################################GUI for Disk I/O End##################################


                                ##################################Disk I/O Calculations Begin##################################
def IO_Calculations():
    global list7
    with open('data.pickle2', 'rb') as pickle_in:
        f = pickle.load(pickle_in)  
        
    for line in f:
        if 'sda' in line:
            sda=line.split()[2]
            break;
    if sda in prev_disk_util:
                
        disk_time_interval = 3
        curr_disk_read =  int(line.split()[3])
        curr_blocks_read = round(int(line.split()[5])*512)
        curr_disk_write = int(line.split()[7])
        curr_blocks_write = round(int(line.split()[9])*512)
                
        curr_avg_response_time = int(line.split()[12]) 
                
        prev_disk_read = int(prev_disk_util[sda][0])
        prev_block_read = int(prev_disk_util[sda][1])
        prev_disk_write = int(prev_disk_util[sda][2])
        prev_block_write = int(prev_disk_util[sda][3])
                
        prev_avg_response_time = int(prev_disk_util[sda][8])
                
        curr_disk_util[sda][0] = round((curr_disk_read - prev_disk_read)/disk_time_interval,2)
        curr_disk_util[sda][1] = round((curr_blocks_read - prev_block_read)/(1024*disk_time_interval),2)
        curr_disk_util[sda][2] = round((curr_disk_write - prev_disk_write)/disk_time_interval,2)
        curr_disk_util[sda][3] = round((curr_blocks_write - prev_block_write)/(1024*disk_time_interval),2)
                
        curr_disk_util[sda][4] = round((curr_disk_util[sda][0] + curr_disk_util[sda][4])/2,2)
        curr_disk_util[sda][5] = round((curr_disk_util[sda][1] + curr_disk_util[sda][5])/2,2)
        curr_disk_util[sda][6] = round((curr_disk_util[sda][2] + curr_disk_util[sda][6])/2,2)
        curr_disk_util[sda][7] = round((curr_disk_util[sda][3] + curr_disk_util[sda][7])/2,2)
                
        curr_disk_util[sda][8] = round((curr_avg_response_time - prev_avg_response_time)/disk_time_interval,2)
                
        curr_disk_util[sda][9] = round((((curr_disk_util[sda][0] + curr_disk_util[sda][2]) * curr_disk_util[sda][8])/1000)*100,2)
                
        prev_disk_util[sda][0] = curr_disk_read
        prev_disk_util[sda][1] = curr_blocks_read
        prev_disk_util[sda][2] = curr_disk_write
        prev_disk_util[sda][3] = curr_blocks_write
        prev_disk_util[sda][8] = curr_avg_response_time                
                
    else:
        tmplist=line.split()
                
        prev_disk_util[sda] = []
        prev_disk_util[sda].append(int(tmplist[3]))
        prev_disk_util[sda].append(round(int(tmplist[5])*512))
        prev_disk_util[sda].append(int(tmplist[7]))
        prev_disk_util[sda].append(round(int(tmplist[9])*512))
        prev_disk_util[sda].append(int(0))
        prev_disk_util[sda].append(int(0))
        prev_disk_util[sda].append(int(0))
        prev_disk_util[sda].append(int(0))
        prev_disk_util[sda].append(int(tmplist[12]))
        prev_disk_util[sda].append(int(0))
        curr_disk_util[sda]=[]
        curr_disk_util[sda]=[0,0,0,0,0,0,0,0,0,0]
                
    i=0
    for item in curr_disk_util[sda]:
        list7[i].configure(text=item)
        i=i+1
    
    t=Timer(3,IO_Calculations)
    t.start()              
    
                                ##################################Disk I/O Calculations End##################################
                            
                                ##################################GUI for Network Begin##################################
def Network_Deign():
    Label(tab_for_Network, text="NETWORK STATISTIC'S", relief=RAISED,anchor=CENTER, font=Font).grid(row=0,column=0,rowspan=1,columnspan=10,sticky=(N,S,W,E))

    r=1
    c=0
    list8 = ["TCP","Rate","Min","Max","Avg"]
    for item in list8:
        Label(tab_for_Network,text=item,relief=RAISED,anchor=CENTER,font=Font5).grid(row=r,column=c,sticky=(N,S,W,E))
        c=c+1
        
    i=0
    r=2
    c=1
    for item in range(8):
        list12.append(Label(tab_for_Network,text=item,anchor=CENTER,font=Font2, relief=SUNKEN))
        list12[i].grid(row=r,column=c,sticky=(S,N,E,W))  
        if(r==3):
            r=1
            c=c+1
        r=r+1    
        i=i+1
    Label(tab_for_Network, text="Packets Received", relief=RAISED,anchor=W, font=Font1).grid(row=2,column=0,rowspan=1,columnspan=1,sticky=(N,S,W,E))

    Label(tab_for_Network, text="Packets Sent", relief=RAISED,anchor=W, font=Font1).grid(row=3,column=0,rowspan=1,columnspan=1,sticky=(N,S,W,E))

    r=1
    c=5
        
    list9 = ["IP","Rate","Min","Max","Avg"]
    for item in list9:
        Label(tab_for_Network,text=item,relief=RAISED,anchor=CENTER,font=Font5).grid(row=r,column=c,sticky=(N,S,W,E))
        c=c+1

    i=0
    r=2
    c=6
    for item in range(8):
        list13.append(Label(tab_for_Network,text=item,anchor=CENTER,font=Font2, relief=SUNKEN))
        list13[i].grid(row=r,column=c,sticky=(S,N,E,W))  
        if(r==3):
            r=1
            c=c+1
        r=r+1
        i=i+1

    Label(tab_for_Network, text="Packets Received", relief=RAISED,anchor=W, font=Font1).grid(row=2,column=5,rowspan=1,columnspan=1,sticky=(N,S,W,E))
    Label(tab_for_Network, text="Packets Sent", relief=RAISED,anchor=W, font=Font1).grid(row=3,column=5,rowspan=1,columnspan=1,sticky=(N,S,W,E))           
    Label(tab_for_Network, text="TCP Information", relief=RAISED,anchor=CENTER, font=Font5).grid(row=4,column=0,rowspan=1,columnspan=2,sticky=(N,S,W,E))
    Label(tab_for_Network, text="Network Speed", relief=RAISED,anchor=CENTER, font=Font5).grid(row=4,column=2,rowspan=1,columnspan=3,sticky=(N,S,W,E))    
    Label(tab_for_Network, text="Active", relief=RAISED,anchor=W, font=Font1).grid(row=5,column=0,rowspan=1,columnspan=1,sticky=(N,S,W,E))

    global label_active,label_established
    
    label_active = Label(tab_for_Network, text="", relief=RAISED,anchor=CENTER, font=Font2)
    label_active.grid(row=5,column=1,rowspan=1,columnspan=1,sticky=(N,S,W,E))
    
    Label(tab_for_Network, text="Established", relief=RAISED,anchor=W, font=Font1).grid(row=6,column=0,rowspan=1,columnspan=1,sticky=(N,S,W,E))

    label_established = Label(tab_for_Network, text="", relief=RAISED,anchor=CENTER, font=Font2)
    label_established.grid(row=6,column=1,rowspan=1,columnspan=1,sticky=(N,S,W,E))

    global label_received,label_sent
                
    Label(tab_for_Network, text="Kb Received/s", relief=RAISED,anchor=W, font=Font1).grid(row=5,column=2,rowspan=1,columnspan=2,sticky=(N,S,W,E))

    label_received = Label(tab_for_Network, text="", relief=RAISED,anchor=CENTER, font=Font2)
    label_received.grid(row=5,column=4,rowspan=1,columnspan=1,sticky=(N,S,W,E))
        
    Label(tab_for_Network, text="Kb Sent/s", relief=RAISED,anchor=W, font=Font1).grid(row=6,column=2,rowspan=1,columnspan=2,sticky=(N,S,W,E))

    label_sent = Label(tab_for_Network, text="", relief=RAISED,anchor=CENTER, font=Font2)
    label_sent.grid(row=6,column=4,rowspan=1,columnspan=1,sticky=(N,S,W,E))
        
    r=4
    c=5    
    
    list10 = ["UDP","Rate","Max","Min","Avg"]
    for item in list10:
        Label(tab_for_Network,text=item,relief=RAISED,anchor=CENTER,font=Font5).grid(row=r,column=c,sticky=(N,S,W,E))
        c=c+1    
        
    i=0
    r=5
    c=6
    for item in range(8):
        list14.append(Label(tab_for_Network,text=item,anchor=CENTER,font=Font2, relief=SUNKEN))
        list14[i].grid(row=r,column=c,sticky=(S,N,E,W))  
        if(r==6):
            r=4
            c=c+1
        r=r+1
        i=i+1

    Label(tab_for_Network, text="Packets Received", relief=RAISED,anchor=W, font=Font1).grid(row=5,column=5,rowspan=1,columnspan=1,sticky=(N,S,W,E))
    Label(tab_for_Network, text="Packets Sent", relief=RAISED,anchor=W, font=Font1).grid(row=6,column=5,rowspan=1,columnspan=1,sticky=(N,S,W,E))
    
    networklabel_tcp=Label(tab_for_Network,text="TCP Data",relief=RAISED,anchor=CENTER, font=Font2)
    networklabel_tcp.grid(row=8,column=0,rowspan=6,columnspan=int(5),sticky=(N,S,W,E))
    canvas=FigureCanvasTkAgg(fig_network_tcp,networklabel_tcp)    
    canvas.show()    
    canvas.get_tk_widget().pack(side=RIGHT,fill=BOTH,expand=True)

    networklabel_udp=Label(tab_for_Network,text="UDP Data",relief=RAISED,anchor=CENTER, font=Font2)
    networklabel_udp.grid(row=8,column=5,rowspan=6,columnspan=int(5),sticky=(N,S,W,E))    
    canvas=FigureCanvasTkAgg(fig_network_udp,networklabel_udp)    
    canvas.show()    
    canvas.get_tk_widget().pack(side=RIGHT,fill=BOTH,expand=True) 

                                ##################################GUI for Network Ends##################################

                                ##################################Network Calculations Begin##################################
def Network_Calculations():
    global tcp,udp,ip
    with open('data.pickle2', 'rb') as pickle_in:
        f = pickle.load(pickle_in)  
        
    for line in f:
        if "Tcp:" in line :
            tcp = line.split()[0].lower()
            label_active.configure(text = line.split()[5])
            label_established.configure(text = line.split()[9])
            if (tcp in prev_tcp_util):
            
                tcp_value = line.split()
                prev_tcp_rec = int(prev_tcp_util[tcp][0])
                prev_tcp_sent = int(prev_tcp_util[tcp][1])
        
                curr_tcp_rec = int(tcp_value[10])
                curr_tcp_sent = int(tcp_value[11])
        
                tcp_received_rate = round((curr_tcp_rec - prev_tcp_rec)/3,2)
                tcp_sent_rate = round((curr_tcp_sent - prev_tcp_sent)/3,2)
        
                curr_tcp_util[tcp][0] = tcp_received_rate
                curr_tcp_util[tcp][1] = tcp_sent_rate
        
                if(tcp_received_rate < curr_tcp_util[tcp][2]):
                    curr_tcp_util[tcp][2]=tcp_received_rate

                if(tcp_sent_rate < curr_tcp_util[tcp][3]):
                    curr_tcp_util[tcp][3]=tcp_sent_rate    

                if(tcp_received_rate > curr_tcp_util[tcp][4]):
                    curr_tcp_util[tcp][4]=tcp_received_rate

                if(tcp_sent_rate > curr_tcp_util[tcp][5]):
                    curr_tcp_util[tcp][5]=tcp_sent_rate

                    curr_tcp_util[tcp][6]= round((curr_tcp_util[tcp][6]+ tcp_received_rate )/2,2)
                    curr_tcp_util[tcp][7]= round((curr_tcp_util[tcp][7]+ tcp_sent_rate )/2,2)
        
                prev_tcp_util[tcp][0] = curr_tcp_rec
                prev_tcp_util[tcp][1] = curr_tcp_sent
                   
                i=0
                for item in curr_tcp_util[tcp]:
                    list12[i].configure(text=item)
                    i=i+1

            else:
                tmplist1 = line.split()
                prev_tcp_util[tcp] = []
                prev_tcp_util[tcp].append(int(tmplist1[10]))
                prev_tcp_util[tcp].append(int(tmplist1[11]))
                curr_tcp_util[tcp] = []
                curr_tcp_util[tcp] = [0,0,0,0,0,0,0,0]
        if "Udp:" in line :
            udp = line.split()[0].lower()
            if (udp in prev_udp_util):   
                
                upd_values = line.split()
            
                prev_udp_rec = int(prev_udp_util[udp][0])
                prev_udp_sent = int(prev_udp_util[udp][1])
        
                curr_udp_rec = int(upd_values[1])
                curr_udp_sent = int(upd_values[4])
            
                udp_received_rate = round((curr_udp_rec - prev_udp_rec)/3,2)
                udp_sent_rate = round((curr_udp_sent - prev_udp_sent)/3,2)
        
                curr_udp_util[udp][0] = udp_received_rate
                curr_udp_util[udp][1] = udp_sent_rate
        
                if(udp_received_rate < curr_udp_util[udp][2]):
                    curr_udp_util[udp][2]=udp_received_rate

                if(udp_sent_rate < curr_udp_util[udp][3]):
                    curr_udp_util[udp][3]=udp_sent_rate    

                if(udp_received_rate > curr_udp_util[udp][4]):
                    curr_udp_util[udp][4]=udp_received_rate

                if(udp_sent_rate > curr_udp_util[udp][5]):
                    curr_udp_util[udp][5]=udp_sent_rate

                    curr_udp_util[udp][6]= round((curr_udp_util[udp][6]+ udp_received_rate )/2,2)
                    curr_udp_util[udp][7]= round((curr_udp_util[udp][7]+ udp_sent_rate )/2,2)
        
                prev_udp_util[udp][0] = curr_udp_rec
                prev_udp_util[udp][1] = curr_udp_sent
            
                j=0
    
                for item in curr_udp_util[udp]:
                    list14[j].configure(text=item)
                    j=j+1
            
            else:
                tmplist2 = line.split()
                prev_udp_util[udp] = []
                prev_udp_util[udp].append(int(tmplist2[1]))
                prev_udp_util[udp].append(int(tmplist2[4]))
                curr_udp_util[udp] = []
                curr_udp_util[udp] = [0,0,0,0,0,0,0,0]

        if "Ip:" in line:
            ip = line.split()[0].lower()
            if (ip in prev_ip_util): 
                ip_values = line.split()
                   
                prev_ip_rec = int(prev_ip_util[ip][0])
                prev_ip_sent = int(prev_ip_util[ip][1])
        
                curr_ip_rec = int(ip_values[3])
                curr_ip_sent = int(ip_values[10])
            
                ip_received_rate = round((curr_ip_rec - prev_ip_rec)/3,2)
                ip_sent_rate = round((curr_ip_sent - prev_ip_sent)/3,2)
        
                curr_ip_util[ip][0] = ip_received_rate
                curr_ip_util[ip][1] = ip_sent_rate
        
                if(ip_received_rate < curr_ip_util[ip][2]):
                    curr_ip_util[ip][2]=ip_received_rate

                if(ip_sent_rate < curr_ip_util[ip][3]):
                    curr_ip_util[ip][3]=ip_sent_rate    

                if(ip_received_rate > curr_ip_util[ip][4]):
                    curr_ip_util[ip][4]=ip_received_rate

                if(ip_sent_rate > curr_ip_util[ip][5]):
                    curr_ip_util[ip][5]=ip_sent_rate

                    curr_ip_util[ip][6]= round((curr_ip_util[ip][6]+ ip_received_rate )/2,2)
                    curr_ip_util[ip][7]= round((curr_ip_util[ip][7]+ ip_sent_rate )/2,2)
        
                prev_ip_util[ip][0] = curr_ip_rec
                prev_ip_util[ip][1] = curr_ip_sent
                j=0
    
                for item in curr_ip_util[ip]:
                    list13[j].configure(text=item)
                    j=j+1
            
            else:
                tmplist3 = line.split()
                prev_ip_util[ip] = []
                prev_ip_util[ip].append(int(tmplist3[3]))
                prev_ip_util[ip].append(int(tmplist3[10]))
                curr_ip_util[ip] = []
                curr_ip_util[ip] = [0,0,0,0,0,0,0,0]

        if "eth0:" in line:
            eth = line.split()[0]
            if(eth in curr_nw_speed):
                eth_list = line.split()
                prev_nw_speed_rec = int(prev_nw_speed[eth][0])
                prev_nw_speed_sent = int(prev_nw_speed[eth][1])
                
                curr_nw_speed_rec = int(eth_list[1])
                curr_nw_speed_sent = int(eth_list[9])
                
                kb_rec_per_sec = round((((curr_nw_speed_rec - prev_nw_speed_rec)/3)/1024),2)
                kb_sent_per_sec = round((((curr_nw_speed_sent - prev_nw_speed_sent)/3)/1024),2)
                
                curr_nw_speed[eth][0] = kb_rec_per_sec
                curr_nw_speed[eth][1] = kb_sent_per_sec                
                
                prev_nw_speed[eth][0] = curr_nw_speed_rec
                prev_nw_speed[eth][1] = curr_nw_speed_sent

                label_received.configure(text = curr_nw_speed[eth][0])
                label_sent.configure(text = curr_nw_speed[eth][1])
                
            else:
                
                tmplist4 = line.split()
                prev_nw_speed[eth] = []
                prev_nw_speed[eth].append(int(tmplist4[1]))
                prev_nw_speed[eth].append(int(tmplist4[9]))
                curr_nw_speed[eth] = []
                curr_nw_speed[eth] = [0,0]
         
    t=Timer(3,Network_Calculations)
    t.start()
        
                                ##################################Network Calculations Ends##################################
                                

                                ##################################Process Calculations Begin##################################
def Process_Calculations():
    global prev_process_list,curr_process_list,count
    with open('data.pickle3', 'rb') as pickle_in:
        f = pickle.load(pickle_in) 
        
    VmSize = ((math.pow(2,64)-1)/1024)

    for line in f:
        if "Process:" in line:
            pid = line.split()[1]
            if pid in prev_process_list:
                curr_temp_list = [0,0,0,0,0,0,0,0,0,0,0,0,0]
                templist = line.split()

                curr_temp_list[0] = pid                                                             ##PID
                curr_temp_list[2] = templist[2]                                                     ##PRIORITY
                curr_temp_list[3] = templist[3]                                                     ##NICE
                curr_temp_list[4] = round((int(templist[4]))/1024,2)                                ##Virtual Memory in Kb
                curr_temp_list[5] = round(((curr_temp_list[4]/int(VmSize))*100),6)                     ##VM % 
                curr_temp_list[6] = round((int(templist[5])*4096/1024),2)                           ##Rss. Each Page is 4KB. Represented in KB
                
                #curr_temp_list[7] = round((int(curr_temp_list[6])*100/(int(100000))),2)                ##Rss %
                
                curr_temp_list[7] = round((int(curr_temp_list[6])*100/(int(mem_util[4]))),2)
                    
                curr_temp_list[8] = templist[6]                                                     ##State
                curr_temp_list[9] = round((int(templist[7]) - int(prev_process_list[pid][0]))/3,2)  ##User Time
                curr_temp_list[10] = round((int(templist[8]) - int(prev_process_list[pid][1]))/3,2) ##System Time 
                curr_temp_list[11] = round((curr_temp_list[9] + curr_temp_list[10])/3,2)            ##Total Time

                curr_temp_list[1] =  templist[9]                                                    ##Username
                curr_temp_list[12] = templist[10]                                                    ##Command
                
                curr_process_list.append(curr_temp_list)
                
                prev_process_list[pid][0] = int(templist[7])
                prev_process_list[pid][1] = int(templist[8])
            else:
                prev_process_list[pid] = []
                prev_process_list[pid].append(line.split()[7])                                         ##Previous Utime
                prev_process_list[pid].append(line.split()[8])                                         ##Previous Stime
 
    heapq.nlargest(len(curr_process_list), curr_process_list,key=lambda curr_process_list: curr_process_list[11])    ##Sorting list using heap queue
   
    temp_list = copy.copy(heapq.nlargest(int(variable.get()), curr_process_list,key=lambda curr_process_list: curr_process_list[11]))    

    global deleteitemsrun
    
    for i in tree.get_children():           ##Clear the Treeview after every run
        tree.delete(i)
        
    for item in temp_list:
        tree.insert("",'end',values=item) 

    if curr_process_list:
        curr_process_list.clear()
        curr_temp_list.clear()
        temp_list.clear()
       
    t=Timer(3,Process_Calculations)
    t.start()          

                                ##################################Process Calculations Ends##################################


                                ##################################GUI for Process Begins##################################
def Process_Design():
    global tree,variable
    
    process_label=Label(tab_for_Process)
    process_label.grid(column=0, row=0, sticky=(N, S, E, W))
    tab_for_Process.columnconfigure(0, weight=1)
    tab_for_Process.rowconfigure(0,weight=1)
    
    Label(process_label,text="Please select No. of Processes",relief=RAISED,anchor=CENTER, font=Font2).grid(row=0,column=0,sticky=(N,S,W,E))
    variable = StringVar(tab_for_Process)
    variable.set("0") # default value
    choices = ['0','10', '20', '50', '100']
    w = OptionMenu(process_label, variable, *choices)
    w.grid(row = 0, column =1)
    btn_process=Button(process_label,text="Search",command=Process_Calculations)
    btn_process.grid(column=2, row=0, sticky=(N, S, E, W))
    
    tree = Treeview(tab_for_Process,height=25,show='headings',columns=('pid','user','pr','ni','virt','virtper','res','resper','s','ucpu','scpu','cpu','command'))

    tree.column('pid', width=70, anchor='center')
    tree.column('user', width=100, anchor='center')
    tree.column('pr', width=50, anchor='center')
    tree.column('ni', width=50, anchor='center')
    tree.column('virt', width=100, anchor='center')
    tree.column('virtper', width=100, anchor='center')
    tree.column('res', width=70, anchor='center')
    tree.column('resper', width=70, anchor='center')
    tree.column('s', width=20, anchor='center')
    tree.column('ucpu', width=60, anchor='center')
    tree.column('scpu', width=60, anchor='center')
    tree.column('cpu', width=60, anchor='center')
    tree.column('command', width=100, anchor='center')

    tree.heading('pid',text='PID')
    tree.heading('user', text='USER')
    tree.heading('pr', text='PRI')
    tree.heading('ni', text='NICE')
    tree.heading('virt',text='VIRT')
    tree.heading('virtper',text='%VIRT')
    tree.heading('res', text='RES')
    tree.heading('resper', text='%RES')
    tree.heading('s', text='S')
    tree.heading('ucpu',text='%USER')
    tree.heading('scpu',text='%SYS')
    tree.heading('cpu', text='%CPU')
    tree.heading('command', text='COMMAND') 
       
    tree.grid(row=1,column=0,sticky=S+N+E+W)
    s = Scrollbar(tab_for_Process, orient=VERTICAL, command=tree.yview)
    s.grid(column=1, row=1, sticky=(N,S))
    tree['yscrollcommand'] = s.set

    tree.columnconfigure(0, weight=1)
    tree.rowconfigure(0,weight=1)

    ttk.Style().configure("Treeview", background="black", 
    foreground="white", fieldbackground="light grey",font=Font4)
    


                                ##################################GUI for Process Ends##################################


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

root = Tk()

root.title("Task Manager")
root.configure(background='white')

note1 = Notebook(root)
Sizegrip(root).grid(column=999, row=999, sticky=(S,E))
note1.grid(column=0, row=0, sticky=(N, S, E, W))

st = Style()
st.configure('My.TFrame', font=Font1)

##Creating Frame for individual model
tab_for_CPU = Frame(note1)
note1.add(tab_for_CPU,text="CPU")  

tab_for_Memory = Frame(note1)
note1.add(tab_for_Memory,text="Memory")

tab_for_DiskIO = Frame(note1)
note1.add(tab_for_DiskIO,text="Disk I/O")  

tab_for_Network = Frame(note1)
note1.add(tab_for_Network,text="Network")

tab_for_Process = Frame(note1)
note1.add(tab_for_Process,text="Process")  


CPU_Design()                ##CPU GUI
CPU_Calculations()            ##CPU Calculations

Memory_Design()                ##Memory GUI
Memory_Calculations()        ##Memory Calculations

IO_Design()                    ##DiskIO GUI
IO_Calculations()            ##DiskIO Calculations

Network_Deign()                ##NETWORK GUI
Network_Calculations()        ##NETWORK Calculations

Process_Design()            ##Process Statistics

CPU_Graph_Design()            ##CPU Grahical Interphase

cpu_animation=animation.FuncAnimation(f1,CPU_Graph_Layout,interval=2000)
memory_animation=animation.FuncAnimation(fig_memory,Memory_Graph_Layout,interval=2000)
diskio_animation=animation.FuncAnimation(fig_diskio,DiskIO_Graph_Layout,interval=2000)
network_tcp_animation=animation.FuncAnimation(fig_network_tcp,Network_TCP_Graph_Layout,interval=2000)
network_udp_animation=animation.FuncAnimation(fig_network_udp,Network_UDP_Graph_Layout,interval=2000)

root.mainloop()
s.close()