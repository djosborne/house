from scapy.all import *
from phue import Bridge

b = Bridge('192.168.1.65')

class Room(object):
    def __init__(self, nickname, lights):
        self.nickname = nickname
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

    def __str__(self):
        return self.nickname

dans_room = Room('Dans Room',
                 ['Dans room 1',
                  'Dans Window',
                  'Dans Bookcase',
                  'Dans Globe',
                  'Dans Desk'])

living_room = Room('Living Room',
                   ['Fireplace Strips',
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

room_by_mac = {'a0:02:dc:d3:42:4d': dans_room,
               '74:75:48:dc:2b:2f': living_room}

def arp_display(pkt):
    try:
        if pkt[ARP].op == 1: #who-has (request)
            if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
                mac = pkt[ARP].hwsrc
                try:
                    room = room_by_mac[mac]
                    print room
                    if room.any_light_is_on():
                        room.turn_lights_off()
                    else:
                        room.turn_lights_on()
                except KeyError:
                  print "Unknown Arp: " + pkt[ARP].hwsrc
    except IndexError:
        pass
print sniff(prn=arp_display, filter="arp", store=0, count=0)
