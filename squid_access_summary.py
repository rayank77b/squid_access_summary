#!/usr/bin/python

import fileinput
import time ,os
import datetime
import socket

MAXCNT=250
MAXZEIT=60*5  # 5 minuten
ips={}
hostname={}
zeitpunkt=0
zeitpunktlast=0
zeitpunktstart=-1

def pr(ip, h, bcnt):
    print "  %15s    %30s   %5d MB (%5d kB)"%(ip, h, (bcnt/1024/1024), (bcnt/1024))

def display():
    keylist=ips.keys()
    keylist.sort()
    os.system('clear')
    summe500=0
    summe100=0
    summe010=0
    # print first all who ist > 500MB
    print "User > 500MB download"
    for key in keylist:
        if(ips[key]>(500*1024*1024)):
            pr(key, hostname[key], ips[key])
            summe500=summe500+ips[key]
    print ("                                                                   Summe:%5d MB"%(summe500/1024/1024))
    print "\nUser > 100MB download"
    for key in keylist:
        if((ips[key]>(100*1024*1024)) and (ips[key]<=(500*1024*1024))):
            pr(key, hostname[key], ips[key])
            summe100=summe100+ips[key]
    print ("                                                                   Summe:%5d MB"%(summe100/1024/1024))
    print "\nUser > 10MB download"
    for key in keylist:
        if((ips[key]>(10*1024*1024)) and (ips[key]<=(100*1024*1024))):
            pr(key, hostname[key], ips[key])
            summe010=summe010+ips[key]
    print ("                                                                   Summe:%5d MB"%(summe010/1024/1024))

    print "\n\nGestartet am: ", datetime.datetime.fromtimestamp(zeitpunktstart).strftime('%Y-%m-%d %H:%M'),
    print "  laueft: %d min"%((zeitpunkt-zeitpunktstart)/60)
    print "\nZeit: ", datetime.datetime.fromtimestamp(zeitpunkt).strftime('%Y-%m-%d %H:%M') 


for line in fileinput.input():
        line = " ".join(line.split())
        lines = line.split(" ")
        bytecnt = int(lines[1])
        ip = lines[2]
        zeitpunkt=int(lines[0].split(".")[0])
        if(zeitpunktstart==-1):
            zeitpunktstart=zeitpunkt
        if(ips.has_key(ip)):
            ips[ip]=ips[ip]+bytecnt
        else:
            ips.update({ip:bytecnt})
            hostname.update({ip:socket.getfqdn(ip)})
        if((zeitpunkt-zeitpunktlast)>MAXZEIT):
            display()
            zeitpunktlast=zeitpunkt
            time.sleep(0.2)
