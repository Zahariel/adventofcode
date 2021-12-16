import functools
import operator

with open("input.txt") as f:
    hex = f.readline().strip()

def get_bit(hex, pos):
    char = hex[pos // 4]
    idx = pos % 4
    val = int(char, 16)
    return 1 if (val & (1 << (3 - idx))) else 0

def get_bits(hex, pos, len):
    val = get_bit(hex, pos)
    for i in range(len - 1):
        val *= 2
        val += get_bit(hex, pos + i + 1)
    return pos + len, val

def read_literal(hex, pos):
    pos, nybble = get_bits(hex, pos, 5)
    result = 0
    while nybble >= 16:
        result *= 16
        result += nybble - 16
        pos, nybble = get_bits(hex, pos, 5)
    result *= 16
    result += nybble
    return pos, result

class Packet():
    def __init__(self, version, typeid):
        self.version = version
        self.typeid = typeid

    def version_sum(self):
        return self.version

    def value(self):
        raise NotImplemented

class LiteralPacket(Packet):
    def __init__(self, version, value):
        super().__init__(version, 4)
        self.val = value

    def value(self):
        return self.val


OPERATIONS = [
    sum,
    lambda l: functools.reduce(operator.mul, l),
    min,
    max,
    lambda l: 0,
    lambda l: 1 if l[0] > l[1] else 0,
    lambda l: 1 if l[0] < l[1] else 0,
    lambda l: 1 if l[0] == l[1] else 0,
]


class OperatorPacket(Packet):
    def __init__(self, version, typeid, subpackets):
        super().__init__(version, typeid)
        self.subpackets = subpackets

    def version_sum(self):
        return self.version + sum(packet.version_sum() for packet in self.subpackets)

    def value(self):
        return OPERATIONS[self.typeid]([packet.value() for packet in self.subpackets])


def read_packet(hex, pos):
    pos, version = get_bits(hex, pos, 3)
    pos, typeid = get_bits(hex, pos, 3)
    if typeid == 4:
        pos, value = read_literal(hex, pos)
        return pos, LiteralPacket(version, value)
    else:
        pos, length_type = get_bits(hex, pos, 1)
        if length_type == 0:
            pos, length = get_bits(hex, pos, 15)
            end_pos = pos + length
            packets = []
            while pos < end_pos:
                pos, packet = read_packet(hex, pos)
                packets.append(packet)
            return pos, OperatorPacket(version, typeid, packets)
        else:
            pos, amt = get_bits(hex, pos, 11)
            packets = []
            for i in range(amt):
                pos, packet = read_packet(hex, pos)
                packets.append(packet)
            return pos, OperatorPacket(version, typeid, packets)

pos, packet = read_packet(hex, 0)
print(pos, len(hex) * 4) # just as a check, these should be pretty similar
print(packet.version_sum())

# part 2
print(packet.value())
