#!/usr/bin/python

import fileinput
import time ,os
import datetime
import socket

MAXZEIT=3  # 3 sek
ips={}
hostname={}
last1={}
last5={}
cnt5=0
last10={}
cnt10=0
last30={}
cnt30=0
last100={}
cnt100=0
zeitpunkt=0
zeitpunktlast=0
zeitpunktstart=-1

def pr(ip, h, bcnt, l1, l2, l3, l4, l5):
    print "  %15s    %30s   %8d MB  %8d kB %8d kB %8d kB %8d kB %8d kB"%(ip, h, (bcnt/1024/1024), l1/1024, l2/1024, l3/1024, l4/1024, l5/1024)
def pr2(ip, h, bcnt, l1, l2, l3, l4, l5):
    print "  %15s    %30s   %8d kB  %8d B  %8d B  %8d B  %8d B  %8d kB"%(ip, h, (bcnt/1024), l1, l2, l3, l4, l5/1024)

def display():
    keylist=ips.keys()
    keylist.sort()
    os.system('clear')
    summe1000=0
    summe100=0
    summe010=0
    # print first all who ist > 500MB
    print "  %15s    %30s        %8s    %8s    %8s    %8s    %8s    %8s   "%("IP-Address", "Hostname", "Gesammt", "Last1", "Last 5", "Last 10", "Last 30", "Last 100")
    print "User > 1000MB download"
    for key in keylist:
        if(ips[key]>(1000*1024*1024)):
            pr(key, hostname[key], ips[key], last1[key], last5[key], last10[key],last30[key],last100[key])
            summe1000=summe1000+ips[key]
    print ("                                               Summe: %8d MB"%(summe1000/1024/1024))
    print "\nUser > 100MB - 1000MB download"
    for key in keylist:
        if((ips[key]>(100*1024*1024)) and (ips[key]<=(1000*1024*1024))):
            pr(key, hostname[key], ips[key], last1[key], last5[key], last10[key],last30[key],last100[key])
            summe100=summe100+ips[key]
    print ("                                               Summe: %8d MB"%(summe100/1024/1024))
    print "\nUser > 1MB - 100MB download"
    for key in keylist:
        if((ips[key]>(1*1024*1024)) and (ips[key]<=(100*1024*1024))):
            pr(key, hostname[key], ips[key], last1[key], last5[key], last10[key],last30[key],last100[key])
            summe010=summe010+ips[key]
    print ("                                               Summe: %8d MB"%(summe010/1024/1024))
    print "\nUser < 1MB download"
    for key in keylist:
        if((ips[key]<(1*1024*1024)) ):
            pr2(key, hostname[key], ips[key], last1[key], last5[key], last10[key],last30[key],last100[key])
            summe010=summe010+ips[key]
    print ("                                               Summe: %8d MB"%(summe010/1024/1024))

    print "\n\nGestartet am: ", datetime.datetime.fromtimestamp(zeitpunktstart).strftime('%Y-%m-%d %H:%M'),
    print "  laueft: %d min"%((zeitpunkt-zeitpunktstart)/60)
    print "\nZeit: ", datetime.datetime.fromtimestamp(zeitpunkt).strftime('%Y-%m-%d %H:%M') 


for line in fileinput.input():
        line = " ".join(line.split())
        lines = line.split(" ")
        bytecnt = int(lines[4])
        ip = lines[2]
        zeitpunkt=int(lines[0].split(".")[0])
        if(zeitpunktstart==-1):
            zeitpunktstart=zeitpunkt
        if(ips.has_key(ip)):
            ips[ip]=ips[ip]+bytecnt
            last1[ip]=bytecnt
            if cnt5 == 5 :
                last5[ip]=bytecnt
                cnt5=0
            else:
                last5[ip]=last5[ip]+bytecnt
            if cnt10 == 10 :
                last10[ip]=bytecnt
                cnt10=0
            else:
                last30[ip]=last30[ip]+bytecnt
            if cnt30 == 30 :
                last30[ip]=bytecnt
                cnt30=0
            else:
                last30[ip]=last30[ip]+bytecnt
            if cnt100 == 100 :
                last100[ip]=bytecnt
                cnt100=0
            else:
                last100[ip]=last100[ip]+bytecnt
            cnt5 = cnt5+1
            cnt10 = cnt10+1
            cnt30 = cnt30+1
            cnt100 = cnt100+1
        else:
            ips.update({ip:bytecnt})
            hostname.update({ip:socket.getfqdn(ip)})
            last1.update({ip:bytecnt})
            last5.update({ip:bytecnt})
            last10.update({ip:bytecnt})
            last30.update({ip:bytecnt})
            last100.update({ip:bytecnt})
        if((zeitpunkt-zeitpunktlast)>MAXZEIT):
            display()
            zeitpunktlast=zeitpunkt
            #time.sleep(0.2)
