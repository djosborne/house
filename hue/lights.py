from scapy.all import *
from phue import Bridge

b = Bridge('192.168.1.65')

class Room(object):
    def __init__(self, lights):
        self.lights = lights

    def turn_lights_off(self):
        b.set_light(self.lights, 'on', False)

    def turn_lights_on(self):
        b.set_light(self.lights, {'on': True, 'bri': 254})

    def any_light_is_on(self):
        for light in self.lights:
            if b.get_light(light)['state']['on']:
                return True
        return False

dans_room = Room(['Dans room 1',
                  'Dans Window',
                  'Dans Bookcase',
                  'Dans Globe',
                  'Dans Desk'])

living_room = Room(['Fireplace Strips',
                    'Clock 2',
                    'TV Strip Left',
                    'TV Left',
                    'Desk',
                    'Paintings',
                    'Desk Strips',
                    'Cats',
                    'Dining Room 1', # May be unnecessary
                    'Clock 1',
                    'Clock 3',
                    'TV Strips Right',
                    'Dining Room 3',
                    'TV Right 1',
                    'iMac',
                    'TV Right 2',
                    'Dining Room 2',
                    'Go'])


def arp_display(pkt):
    try:
        if pkt[ARP].op == 1: #who-has (request)
            if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
                # Dans Room
                if pkt[ARP].hwsrc == 'a0:02:dc:d3:42:4d':
                    print 'Dans Room'
                    if dans_room.any_light_is_on():
                        dans_room.turn_lights_off()
                    else:
                        dans_room.turn_lights_on()
                elif pkt[ARP].hwsrc == '74:75:48:dc:2b:2f':
                    print 'Living Room On/Off'
                    if living_room.any_light_is_on():
                        living_room.turn_lights_off()
                    else:
                        living_room.turn_lights_on()
                else:
                  print "Unknown Arp: " + pkt[ARP].hwsrc
    except IndexError:
        pass
print sniff(prn=arp_display, filter="arp", store=0, count=0)
