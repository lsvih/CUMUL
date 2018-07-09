class Instance:
    def __init__(self, url='', timestamp=0, entries=0, packets=None):
        self.url = url
        self.timestamp = int(timestamp)
        self.entries = int(entries)
        self.packets = packets
        self.incoming_size = sum([packet.packetsize for packet in self.packets])


class EntryNodePacket:
    def __init__(self, entry=''):
        self.entry = str(entry)
        self.packets = []


class Packet:
    def __init__(self, torip='', packetsize=''):
        self.torip = str(torip)
        if packetsize is '':
            self.packetsize = 0
        else:
            self.packetsize = int(packetsize)
