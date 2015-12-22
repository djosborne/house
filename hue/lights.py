from phue import Bridge
b = Bridge('192.168.1.65')

def dans_lights_on():
	b.set_light(['Dans Window', 'Dans Bookcase', 'Dans Globe', 'Dans Desk'], 'on', True)

from scapy.all import *

def arp_display(pkt):
  try:
    if pkt[ARP].op == 1: #who-has (request)
      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
        if pkt[ARP].hwsrc == 'a0:02:dc:d3:42:4d': # ON - dans room
          print 'Dans Room - On'
          dans_lights_on()
        else:
          print "Unknown Arp: " + pkt[ARP].hwsrc
  except IndexError:
    pass
print sniff(prn=arp_display, filter="arp", store=0, count=0)
