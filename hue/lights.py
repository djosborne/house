from phue import Bridge
b = Bridge('192.168.1.65')

dans_lights = ['Dans room 1', 'Dans Window', 'Dans Bookcase', 'Dans Globe', 'Dans Desk']

def dans_lights_on():
	b.set_light(dans_lights, {'on': True, 'bri': 254})

def dans_lights_off():
	b.set_light(dans_lights, 'on', False)

def any_light_is_on():
	for light in dans_lights:
		if b.get_light('Dans Window')['state']['on']:
			return True
	return False


from scapy.all import *

def arp_display(pkt):
  try:
    if pkt[ARP].op == 1: #who-has (request)
      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
        if pkt[ARP].hwsrc == 'a0:02:dc:d3:42:4d': # ON - dans room
          print 'Dans Room - On'
          if any_light_is_on():
            dans_lights_off()
          else:
            dans_lights_on()
        else:
          print "Unknown Arp: " + pkt[ARP].hwsrc
  except IndexError:
    pass
print sniff(prn=arp_display, filter="arp", store=0, count=0)
