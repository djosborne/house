from scapy.all import *
from phue import Bridge
from collections import namedtuple

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


Light = namedtuple('Light', ['id', 'default_mode', 'backup_mode'])
"""
:param default_mode: Represents the settings the light should switch to if
it (or any other light) is not in its default_mode. 
Usually, this is "lights off". But if we're doing a mood switch,
this is the pretty mode.

:param backup_mode: Respresents the settings the light should switch to if
it *and* all other lights are currently in default_mode.
"""


class MoodRoom(object):
    def __init__(self, nickname, lights):
        self.nickname = nickname
        self.lights = lights

    def __repr__(self):
        return self.nickname

    def not_in_default_mode(self):
        """
        return True if not in default mode.
        """
        for light in self.lights:
            hue_light = b.get_light(light.id)
            for option, value in light.default_mode.iteritems():
                try:
		    if hue_light['state'][option] != value:
                        return True
		except TypeError:
		    print "Broken light: %s" % light.id 
        return False

    def activate_default_mode(self):
        for light in self.lights:
            b.set_light(light.id, light.default_mode)

    def activate_backup_mode(self):
        for light in self.lights:
            b.set_light(light.id, light.backup_mode)


dans_room = MoodRoom('Dans Room',
                   [# TV Area
                    Light('Dans room 1', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dans Window', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dans Bookcase', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dans Globe', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dans Desk', {'on': False}, {'on': True, 'bri': 254})])

dans_room_moody = MoodRoom('Dans Room Moody',
                   [# TV Area
                       Light('Dans room 1', {'on': True, 'sat': 0, 'bri': 254, 'effect': 'colorloop', 'colormode': 'hs'}, {'on': False}),
                       Light('Dans Window', {'on': True, 'sat': 64, 'bri': 254, 'effect': 'colorloop', 'colormode': 'hs'}, {'on': False}),
                       Light('Dans Bookcase', {'on': True, 'sat': 128, 'bri': 254, 'effect': 'colorloop', 'colormode': 'hs'}, {'on': False}),
                       Light('Dans Globe', {'on': True, 'sat': 200, 'bri': 254, 'effect': 'colorloop', 'colormode': 'hs'}, {'on': False}),
                       Light('Dans Desk', {'on': True, 'sat': 160, 'bri': 254, 'effect': 'colorloop', 'colormode': 'hs'}, {'on': False})])


living_room_moody = MoodRoom('Living Room - Moody',
                   [# TV Area
                    Light('Fireplace Strips', {'on': True, 'bri': 254}, {'on': True}),
                    Light('Cats',             {'on': True, 'bri': 254}, {'on': True}),
                    Light('TV Left',          {'on': True, 'bri': 254}, {'on': True}),
                    Light('TV Strip Left',    {'on': True, 'bri': 254}, {'on': True}),
                    Light('TV Right 1',       {'on': True, 'bri': 254}, {'on': True}),
                    Light('TV Right 2',       {'on': True, 'bri': 254}, {'on': True}),
                    Light('TV Strips Right',  {'on': True, 'bri': 254}, {'on': True}),

                    # Left wall
                    Light('Paintings', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Clock 1',   {'on': False}, {'on': True, 'bri': 254}),
                    Light('Clock 2',   {'on': False}, {'on': True, 'bri': 254}),
                    Light('Clock 3',   {'on': False}, {'on': True, 'bri': 254}),
                    Light('iMac',      {'on': False}, {'on': True, 'bri': 254}),

                    # Dining Room
                    Light('Dining Room 1', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dining Room 2', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dining Room 3', {'on': False}, {'on': True, 'bri': 254}),

                    # Tyler's desk
                    Light('Desk Strips', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Desk',        {'on': False}, {'on': True, 'bri': 254}),
                    Light('Go',         {'on': False}, {'on': True, 'bri': 254})])


living_room = MoodRoom('Living Room',
                   [# TV Area
                    Light('Fireplace Strips', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Cats',             {'on': False}, {'on': True, 'bri': 254}),
                    Light('TV Left',          {'on': False}, {'on': True, 'bri': 254}),
                    Light('TV Strip Left',    {'on': False}, {'on': True, 'bri': 254}),
                    Light('TV Right 1',       {'on': False}, {'on': True, 'bri': 254}),
                    Light('TV Right 2',       {'on': False}, {'on': True, 'bri': 254}),
                    Light('TV Strips Right',  {'on': False}, {'on': True, 'bri': 254}),

                    # Left wall
                    Light('Paintings', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Clock 1',   {'on': False}, {'on': True, 'bri': 254}),
                    Light('Clock 2',   {'on': False}, {'on': True, 'bri': 254}),
                    Light('Clock 3',   {'on': False}, {'on': True, 'bri': 254}),
                    Light('iMac',      {'on': False}, {'on': True, 'bri': 254}),

                    # Dining Room
                    Light('Dining Room 1', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dining Room 2', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Dining Room 3', {'on': False}, {'on': True, 'bri': 254}),

                    # Tyler's desk
                    Light('Desk Strips', {'on': False}, {'on': True, 'bri': 254}),
                    Light('Desk',        {'on': False}, {'on': True, 'bri': 254}),
                    Light('Go',         {'on': False}, {'on': True, 'bri': 254})])


room_by_mac = {'a0:02:dc:d3:42:4d': dans_room,
               'a0:02:dc:26:d7:7a': dans_room_moody,
               '74:75:48:dc:2b:2f': living_room,
               '00:bb:3a:8c:53:14': living_room_moody}
seen_arps = []
def arp_display(pkt):
    try:
        if pkt[ARP].op == 1: #who-has (request)
            #if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
            if True:
                mac = pkt[ARP].hwsrc
                try:
                    room = room_by_mac[mac]
                except KeyError:
                    if mac not in seen_arps: 
                        print "Unknown Arp: " + mac
                        seen_arps.append(mac)
                else:
                    print room
                    if room.not_in_default_mode():
                        room.activate_default_mode()
                    else:
                        room.activate_backup_mode()
            else:
                print pkt[ARP].psrc
    except IndexError:
        pass
print sniff(prn=arp_display, filter="arp", store=0, count=0)
