#!/usr/bin/python

import fileinput
import time ,os
import datetime
import socket

MAXZEIT=3  # 3 sek
zeitpunkt=0
zeitpunktlast=0
zeitpunktstart=-1

class HostLog:
    def __init__(self, ipaddress, bytecount):
        self.ipaddress = ipaddress
        self.hostname = socket.getfqdn(ipaddress)
        self.bytecount = bytecount
    
    def add(self, bytecount):
        self.bytecount = self.bytecount + bytecount
    
    def __str__(self):
        if(self.bytecount<1024):
            bc = "%8d  B"%(self.bytecount)
        elif(self.bytecount>1024 and self.bytecount<1024*1024):
            bc = "%8d kB"%(self.bytecount/1024)
        elif(self.bytecount>1024*1024 and self.bytecount<1024*1024*1024):
            bc = "%8d MB"%(self.bytecount/1024/1024)
        elif(self.bytecount>1024*1024*1024):
            bc = "%8d GB"%(self.bytecount/1024/1024/1024)
        return  "%16s %35s %s"%(self.ipaddress, self.hostname, bc)

class HostsList:
    def __init__(self):
        self.hosts=[]
    
    def has(self, ipaddress):
        for h in self.hosts:
            if h.ipaddress == ipaddress:
                return True
        return False
    
    def get(self, ipaddress):
        for h in self.hosts:
            if h.ipaddress == ipaddress:
                return h
        return nill

    def add(self, ipaddress, bytecount):
        if not self.has(ipaddress):
            self.hosts.append(HostLog(ipaddress, bytecount))
        else:
            self.get(ipaddress).add(bytecount)
    
    def sort(self):
        self.hosts = sorted(self.hosts, key=lambda h: -h.bytecount)
    
    def display(self):
        os.system('clear')
        # print first all who ist > 500MB
        print "%16s %35s %8s    %8s    %8s    %8s    %8s    %8s   %8s   %8s   %8s   "%("IP-Address", "Hostname", "Gesammt", "1m", "2m", "3m", "4m","5m","6m","7m","8m")
        for h in self.hosts:
                print h
        print "\n\nGestartet am: ", datetime.datetime.fromtimestamp(zeitpunktstart).strftime('%Y-%m-%d %H:%M'),
        print "  laueft: %d min"%((zeitpunkt-zeitpunktstart)/60)
        print "\nZeit: ", datetime.datetime.fromtimestamp(zeitpunkt).strftime('%Y-%m-%d %H:%M') 

host_list = HostsList()

for line in fileinput.input():
        line = " ".join(line.split())
        lines = line.split(" ")
        bytecnt = int(lines[4])
        ip = lines[2]
        zeitpunkt=int(lines[0].split(".")[0])
        if(zeitpunktstart==-1):
            zeitpunktstart=zeitpunkt
        
        host_list.add(ip, bytecnt)
        
        if((zeitpunkt-zeitpunktlast)>MAXZEIT):
            host_list.sort()
            host_list.display()
            zeitpunktlast=zeitpunkt
            time.sleep(0.05)
