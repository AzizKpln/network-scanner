import scapy.all as scapy
import urllib.request as urllib2
import json
import codecs
import optparse
import os
import time
def get_arg():
        parser=optparse.OptionParser()

        parser.add_option("-r","--range",dest="ip_range",action="store",help="This parameter shows you ip addresses,mac addresses and company names in the network")
        parser.add_option("-l","--look_always",dest="look_always",action="store",help="This Parameter shows you io addresses,mac addresses and company names in the network every 5 sec")
        (options,arguments)=parser.parse_args()
        if not options.ip_range and not options.look_always:
                parser.error("Please Use The '-r' Parameter")
        return options

def scan(ip_range):
    arp_request=scapy.ARP(pdst=ip_range)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    answered,unanswered=scapy.srp(broadcast/arp_request,timeout=1,verbose=False)
    print("IP ADDRESS:\t\t\tMAC ADDRESS:\t\t\tCOMPANY:")        
    print("-"*90)
    
    for i in answered:
        url="http://macvendors.co/api/"
        req=urllib2.Request(url+i[1].hwsrc,headers={"User-Agent":"API Browser"})
        resp=urllib2.urlopen(req)
        read=codecs.getreader("utf-8")
        obj=json.load(read(resp))
        print(i[1].psrc+"\t\t\t"+i[1].hwsrc+"\t\t"+obj["result"]["company"])
        
os.system("clear")
options=get_arg()
if options.ip_range:
        scan(options.ip_range)
elif options.look_always:
        while True:
                scan(options.look_always)
                time.sleep(5)
                os.system("clear")


