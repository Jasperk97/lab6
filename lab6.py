"""
Networks and Network Security
Lab 6 - Distributed Sensor Network
NAME: Jasper Koppen & Danny Opdam
STUDENT ID: 11302445

DESCRIPTION:

"""
import sys
import struct
from socket import *
from random import randint
from gui import MainWindow
from sensor import *


# Get random position in NxN grid.
def random_position(n):
    x = randint(0, n)
    y = randint(0, n)
    return (x, y)


def parse(peer, mcast, w, mcast_addr, sensor_pos, sensor_strength, sensor_decay,
         grid_size, ping_period):
    input = w.getline()
    mcast.setblocking(0)
    if (input == "ping"):
        ping(mcast, peer, sensor_pos, sensor_decay, sensor_strength)

    ready = select.select([mcast], [], [], 1)
    if ready[0]:
        data = mcast.recv(4096)
        data = data.decode()
        w.writeln(data)


def get_distance(x, y):
    print("nog niks ermee gedaan")

# v-d^(x)
def ping(mcast, peer, pos, decay, strength):
    """
    v = strength
    x = decay
    d = distance a tot b
    """
    # peer.sendto(bytes("Hello World", "utf-8"), ('127.0.0.1', 50000))
    # peer.sendto(bytes("Hello World", "utf-8"), ('', 50000))
    message = "Ping sent!!!!!\n"
    message += "   From position: " + str(pos) + "\n"
    message += "               x: " + str(pos[0]) + "\n"
    message += "               y: " + str(pos[1]) + "\n"
    message += "   Decay        : " + str(decay) + "\n"
    message += "   Strength     : " + str(strength) + "\n"
    peer.sendto(bytes(message, "utf-8"), (mcast_addr[0], 50000))



def main(mcast_addr, sensor_pos, sensor_strength, sensor_decay,
         grid_size, ping_period):
    """
    mcast_addr: udp multicast (ip, port) tuple.
    sensor_pos: (x,y) sensor position tuple.
    sensor_strength: initial strength of the sensor ping (radius).
    grid_size: length of the  of the grid (which is always square).
    ping_period: time in seconds between multicast pings.
    """

    # Create the peer-to-peer socket.
    peer = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    # Set the socket multicast TTL so it can send multicast messages.
    peer.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 5)
    # Bind the socket to a random port.
    if sys.platform == 'win32':  # windows special case
        peer.bind(('localhost', INADDR_ANY))
    else:  # should work for everything else
        peer.bind(('', INADDR_ANY))

    # Create the multicast listener socket.
    mcast = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    # Sets the socket address as reusable so you can run multiple instances
    # of the program on the same machine at the same time.
    mcast.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    if sys.platform == 'win32':  # windows special case
        mcast.bind(('localhost', mcast_addr[1]))
    else:  # should work for everything else
        mcast.bind(mcast_addr)

    # Subscribe the socket to multicast messages from the given address.
    # mreq = struct.pack('4sl', inet_aton(mcast_addr[0]), INADDR_ANY)
    print(mcast_addr)
    mreq = struct.pack('4sl', inet_aton(mcast_addr[0]), INADDR_ANY)
    mcast.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)


    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


    # make the gui.
    w= MainWindow()
    w.writeln('my address is %s:%s' % peer.getsockname())
    w.writeln('my position is (%s, %s)' % sensor_pos)
    w.writeln('my strength is %s' % sensor_strength)
    w.writeln('my decay is %s' % sensor_decay)

    """
    Hier moeten wij gaan programmeren.
    """
    # # print(peer.sendto(bytes("Hello World", "utf-8"), ('127.0.0.1', 10000)))

    while w.update():
        parse(peer, mcast, w, mcast_addr, sensor_pos, sensor_strength, sensor_decay,
                 grid_size, ping_period)

        pass


# program entry point.
if __name__ == '__main__':
    import sys
    import argparse
    import select
    p = argparse.ArgumentParser()
    p.add_argument('--group', help='multicast group', default='224.1.1.1')
    p.add_argument('--port', help='multicast port', default=50000, type=int)
    p.add_argument('--pos', help='x,y sensor position', default=None)
    p.add_argument('--grid', help='size of grid', default=100, type=int)
    p.add_argument('--strength', help='sensor strength', default=50, type=int)
    p.add_argument('--decay', help='decay rate', default=1, type=int)
    p.add_argument('--period', help='period between autopings (0=off)',
                   default=10, type=int)
    args = p.parse_args(sys.argv[1:])
    if args.pos:
        pos = tuple(int(n) for n in args.pos.split(',')[:2])
    else:
        pos = random_position(args.grid)
    if args.decay > 1.0 and args.decay <= 2.0:
        decay = args.decay
    else:
        decay = 1
    mcast_addr = (args.group, args.port)
    main(mcast_addr, pos, args.strength, decay, args.grid, args.period)
