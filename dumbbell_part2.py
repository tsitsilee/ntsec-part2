# CMU 18731 HW3
# Code referenced from: git@bitbucket.org:huangty/cs144_bufferbloat.git
# Edited by: Soo-Jin Moon, Deepti Sunder Prakash

#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os

# Parse arguments

parser = ArgumentParser(description="Shrew tests")
parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links",
                    required=True)
parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link",
                    required=True)
parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay in milliseconds of host links",
                    default=10)
parser.add_argument('--maxq',
                    dest="maxq",
                    action="store",
                    help="Max buffer size of network interface in packets",
                    default=20)

# Expt parameters
args = parser.parse_args()

class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self, bw_net=100, delay='20ms', bw_host=10, maxq=None):
    #TODO: Add your code to create topology#Adding the two (2) switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(s1, s2, bw=bw_net, delay=delay, max_queue_size=maxq)

        #Part A of the topology
        hl1 = self.addHost('hl1')
        hl2 = self.addHost('hl2')
        a1 = self.addHost('a1')


        ##Part B of the topology (Right part)
        hr1 = self.addHost('hr1')
        hr2 = self.addHost('hr2')
        a2 = self.addHost('a2')
# Connecting the nodes on the left part of the network using 10 Mbps and        #20ms delay
        self.addLink(hl1, s1, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(hl2, s1, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(a1, s1, bw=bw_host, delay=delay, max_queue_size=maxq)


        #Connecting the nodes on the right part of the network using 10 Mbps and        # 20ms delay
        self.addLink(hr1, s2, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(hr2, s2, bw=bw_host, delay=delay, max_queue_size=maxq)
        self.addLink(a2, s2, bw=bw_host, delay=delay, max_queue_size=maxq)


def test_dumbbell():
    "Create network and run shrew  experiment"
    print "starting mininet ...."
    topo = DumbbellTopo(bw_net=args.bw_net,
                    delay='%sms' % (args.delay),
                    bw_host=args.bw_host, maxq=int(args.maxq))

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink,
                  autoPinCpus=True)
    net.start()
    dumpNodeConnections(net.hosts)

    #TODO: Add your code to test reachability of hosts 

    print "Testing if all nodes are reachable"
    net.pingAll()

    print "Testing the bandwidth between the hosts"

    hr1, hr2, hl1, hl2, a1 = net.get('hr1', 'hr2', 'hl1', 'hl2', 'a1')

    hl1_IP_addr = hl1.IP()
    hl2_IP_addr = hl2.IP()
    a1_IP_addr = a1.IP()
    print hl1_IP_addr
    ### CREATING IPERF SERVERS ON HL1 AND HL2
    result = hl1.cmd('iperf -s -p 5001 &')
    result = hl2.cmd('iperf -s -p 5002 &')

    ## creating IPERF CLIENTS ON HR1 AND HR2
    result = hr1.cmd('iperf -c ' + hl1_IP_addr + ' -p 5001 -t 100 &')
    result = hr2.cmd('iperf -c ' + hl2_IP_addr + ' -p 5002 -t 100 &')


    #TODO: Add yoour code to start long lived TCP flows 
    

    CLI(net)
    net.stop()

if __name__ == '__main__':
    test_dumbbell()
