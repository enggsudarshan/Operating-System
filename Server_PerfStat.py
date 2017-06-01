"""
CSC 239 Assignment - 1
Author: Sudarshan Deo
Spring 2017

This file runs on server side. It fetches data from different virtual paths of OS and sends data to client via socket
"""
import pickle
import socket
from threading import Thread
from socketserver import ThreadingMixIn
import time
from threading import Timer
import os
import pwd
import os.path
import subprocess

                                ##################################Function to Fetch Data for client##################################
def Get_Data_For_Client():
    list1 = []
    list2 = []
    list3 = []
                                ##################################CPU Part Begins##################################
    with open('data.pickle', 'wb') as f1:	##This pickle stores data for CPU

        filename='/proc/cpuinfo'
        f = open(filename,'r')
        for line in f:
            if 'vendor_id' in line:
                lcpuinfo1=line.split()
                vendor=lcpuinfo1[2]
                vendor.encode()
                str1 = "vendor_id" + "\t" +  ":" +  "\t" +  vendor + "\n"
                list1.append(str1)

            if 'model name' in line:
                lcpuinfo2=line.split()
                model=lcpuinfo2[3]+lcpuinfo2[4]+lcpuinfo2[5]
                str2 = "model_name"  + "\t" + ":" +  "\t" + model + "\n"
                list1.append(str2)

            if 'cpu cores' in line:
                lcpuinfo3=line.split()
                cores=lcpuinfo3[3]
                str3 = "No_of_cores"  +  "\t" + ":" + "\t" +  cores + "\n"
                list1.append(str3)

        filename='/proc/stat'
    
        f=open(filename,"r")
        for line in f:
            if "cpu" in line:
                str1 = ""
                curr_cpu_list = line.split()
                
                currcpu = curr_cpu_list[0]
                currUser = int(curr_cpu_list[1])
                currSys = int(curr_cpu_list[3])
                currIdle = int(curr_cpu_list[4])


                str1 = str1 + str(currcpu) + "\t"
                str1 = str1 + str(currUser) + "\t"
                str1 = str1 + str(100) + "\t"
                str1 = str1 + str(currSys) + "\t"
                str1 = str1 + str(currIdle) + "\t"
            
                list1.append(str1)

            if "intr" in line:
                list1.append("intr" + "\t" + str(line.split()[1]) + "\n")
            if "ctxt" in line:
                list1.append("ctxt" + "\t" + str(line.split()[1]) + "\n")
     
        pickle.dump(list1,f1,pickle.HIGHEST_PROTOCOL)
        f1.close()
                                ##################################CPU Part Ends##################################        
								
                                ##################################Memory Part Begins##################################								
    with open('data.pickle2', 'wb') as f2:		##This pickle stores data for Memory, DiskIO and Network 
        filename='/proc/meminfo'
        f=open(filename,"r")
        for line in f: 
            str1 = "" 
            if 'MemTotal' in line:
                str1 = str1 + "MemTotal:" + "\t" + str(line.split()[1]) + "\t" + "kB" + "\n"
                list2.append(str1)
            if 'MemFree' in line:
                str1 = str1 + "MemFree:" + "\t" + str(line.split()[1]) + "\t" + "kB" + "\n"
                list2.append(str1)
            if 'MemAvailable' in line:
                str1 = str1 + "MemAvailable:" + "\t" + str(line.split()[1]) + "\t" + "kB" + "\n" 
                list2.append(str1)
            if 'Cached' in line:
                str1 = str1 + "Cached:" + "\t" + str(line.split()[1]) + "\t" + "kB" + "\n"
                list2.append(str1)
                break        
                                ##################################Memory Part Ends##################################

                                ##################################DiskIO Part Begins##################################								
        filename='/proc/diskstats'
        f=open(filename,"r")
        for line in f:
            str1 = ""    
            if 'sda' in line:
                if 'sda' in line.split():
                    str1 = str(line.split()[0])  + "\t" + str(line.split()[1])  +  "\t" + str(line.split()[2])  + "\t" + str(line.split()[3])  +  "\t"  
                    str1 = str1 + str(line.split()[4])  + "\t" + str(line.split()[5])  +  "\t" + str(line.split()[6])  + "\t" + str(line.split()[7])  +  "\t"  
                    str1 = str1 + str(line.split()[8])  + "\t" +  str(line.split()[9]) +  "\t" + str(line.split()[10]) + "\t" + str(line.split()[11]) +  "\t"  
                    str1 = str1 + str(line.split()[12]) + "\t" + str(line.split()[13]) +  "\n" 
            
                    list2.append(str1)
					
                                ##################################DiskIO Part Ends##################################  

                                ##################################Network Part Begins##################################								
        filename='/proc/net/snmp'
        f=open(filename,"r")        
        for line in f:
            str1 = ""
            if(line.split()[0] == "Tcp:" and line.split()[1].isnumeric()):		##TCP
                str1 = str1 + str(line.split()[0])  + "\t" + str(line.split()[1])  +  "\t" + str(line.split()[2])  + "\t" + str(line.split()[3])  +  "\t"   
                str1 = str1 + str(line.split()[4])  + "\t" + str(line.split()[5])  +  "\t" + str(line.split()[6])  + "\t" + str(line.split()[7])  +  "\t"  
                str1 = str1 + str(line.split()[8])  + "\t" +  str(line.split()[9]) +  "\t" + str(line.split()[10]) + "\t" + str(line.split()[11]) +  "\t"  + "\n"
            
                list2.append(str1)
            
            if(line.split()[0] == "Udp:" and line.split()[1].isnumeric()):		##UDP
                str1 = str1 + str(line.split()[0])  + "\t" + str(line.split()[1])  +  "\t" + str(line.split()[2])  + "\t" + str(line.split()[3])  +  "\t"
                str1 = str1 + str(line.split()[4]) + "\n"
            
                list2.append(str1)
        
            if(line.split()[0] == "Ip:" and line.split()[1].isnumeric()):		##IP
                str1 = str1 + str(line.split()[0])  + "\t" + str(line.split()[1])  +  "\t" + str(line.split()[2])  + "\t" + str(line.split()[3])  +  "\t"
                str1 = str1 + str(line.split()[4])  + "\t" + str(line.split()[5])  +  "\t" + str(line.split()[6])  + "\t" + str(line.split()[7])  +  "\t"
                str1 = str1 + str(line.split()[8])  + "\t" +  str(line.split()[9]) +  "\t" + str(line.split()[10]) + "\t"  + "\n"
            
                list2.append(str1)
      
        filename='/proc/net/dev'												##Ethernet
        f=open(filename,"r")        
        for line in f:
            str1 = ""
            if("eth0:" in line.split()):
                str1 = str1 + str(line.split()[0])  + "\t" + str(line.split()[1])  +  "\t" + str(line.split()[2])  + "\t" + str(line.split()[3])  +  "\t"
                str1 = str1 + str(line.split()[4])  + "\t" + str(line.split()[5])  +  "\t" + str(line.split()[6])  + "\t" + str(line.split()[7])  +  "\t" 
                str1 = str1 + str(line.split()[8])  + "\t" +  str(line.split()[9]) +  "\t" + "\n"
            
                list2.append(str1)
                                  
        pickle.dump(list2,f2,pickle.HIGHEST_PROTOCOL)    
        f2.close()
                                ##################################Network Part Ends##################################
								
                                ##################################Process Part Begins##################################								
    with open('data.pickle3', 'wb') as f3:   	##This pickle stores data for Individual Processes
        for pid in os.listdir(path='/proc'):
            str2 = ""
            if(pid.isnumeric()):    
                pid_stat = os.path.join("/proc",pid,"stat")
                pid_status = os.path.join("/proc",pid,"status")
                f = open(pid_stat,"r")
                for line in f:
                    str2 = str2 + "Process:" + "\t" + pid + "\t" + str(line.split()[17]) + "\t" + str(line.split()[18]) + "\t" + str(line.split()[22])
                    str2 = str2 + "\t" + str(line.split()[23]) + "\t" + str(line.split()[2]) + "\t" + str(line.split()[13]) + "\t" + str(line.split()[14]) + "\t" + "\t"
                    
                f = open(pid_status,"r")
                for line1 in f:
                    if "Name:" in line1:
                        str2 = str2 + str(line1.split()[1]) + "\t" + "\t" + "\t"
                    if "Uid:" in line1:
                        str2 = str2 + pwd.getpwuid(int(line1.split()[1])).pw_name + "\n"  
                list3.append(str2)
        pickle.dump(list3,f3,pickle.HIGHEST_PROTOCOL)
        f3.close()
                                ##################################Process Part Ends##################################
    t=Timer(3,Get_Data_For_Client)
    t.start()    

                                ##################################Socket Begins##################################

TCP_IP = socket.gethostbyaddr("127.0.0.1")[0]	##Localhost
TCP_PORT = 6013
BUFFER_SIZE = 4096

print ('TCP_IP=',TCP_IP)
print ('TCP_PORT=',TCP_PORT)

                                ##################################Thread-1 for CPU Data##################################
class ClientThread1(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print ("New thread started for "+ip+":"+str(port))

    def run(self):
        filename='data.pickle'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                break

                                ##################################Thread-1 for CPU Data End##################################

                                ##################################Thread-2 for Memory, DiskIO, Network Data##################								
class ClientThread2(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print ("New thread started for "+ip+":"+str(port))

    def run(self):
        filename='data.pickle2'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                break

                                ##################################Thread-2 for Memory, DiskIO, Network Data Ends##################

                                ##################################Thread-3 for Process Data#######################################								
class ClientThread3(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print ("New thread started for "+ip+":"+str(port))

    def run(self):
        filename='data.pickle3'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                break

                                ##################################Thread-3 for Process Data Ends#######################################	
								
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []



while True:
    tcpsock.listen(1)
    Get_Data_For_Client()
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread1(ip,port,conn)
    newthread.start()
    threads.append(newthread)   
    
    newthread2 = ClientThread2(ip,port,conn)
    newthread2.start()
    threads.append(newthread2) 
    
    newthread3 = ClientThread3(ip,port,conn)
    newthread3.start()
    threads.append(newthread3)        
    
for t in threads:
    t.join()