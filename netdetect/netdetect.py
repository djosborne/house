from scapy.all import *
import json
from users import username_by_mac

# Key: mac,    Value: time
last_check_in_by_username = {}

# Key: mac,   value: owner


def arp_display(pkt):
  try:
    if pkt[ARP].op == 1: #who-has (request)
        mac = pkt[ARP].hwsrc
        print "ARP Probe from: ", mac

        if not mac in username_by_mac:
          print "No clue who that is though."
          return
        else:
          username = username_by_mac[mac]
          print "Its %s!" % username

        last_check_in_by_username[username] = time.time()
        save_results_to_json()

  except IndexError:
    pass

def save_results_to_json():
  outdata = {"last-updated": time.time()}
  outdata["data"] = last_check_in_by_username

  with open('whose_home.json', 'w') as f:
    f.write(json.dumps(outdata))

print "Sniffing..."
sniff(prn=arp_display, store=0, count=0)
