# -*- coding: utf-8 -*-
import re

regex = re.compile('(?P<mac>.+?) +(?P<ip>.*?) +(\d+) +([\w-]+) +(?P<vlan>\d+) +(?P<int>.*$)')
result = []

with open('dhcp_snooping.txt') as data:
    for line in data:
        if line[0].isdigit():
            result.append(regex.search(line).groupdict())

print("К коммутатору подключено {} устройства".format( len(result) ))

for num, comp in enumerate(result, 1):
    print("Параметры устройства {}:".format( num ))
    for key in comp:
        print("{:10}: {:10}".format( key,comp[key] ))


"""
Example:

$ python parse_dhcp_snooping.py
К коммутатору подключено 4 устройства
Параметры устройства 1:
mac       : 00:09:BB:3D:D6:58
ip        : 10.1.10.2
vlan      : 10
int       : FastEthernet0/1
Параметры устройства 2:
mac       : 00:04:A3:3E:5B:69
ip        : 10.1.5.2
vlan      : 5
int       : FastEthernet0/10
Параметры устройства 3:
mac       : 00:05:B3:7E:9B:60
ip        : 10.1.5.4
vlan      : 5
int       : FastEthernet0/9
Параметры устройства 4:
mac       : 00:09:BC:3F:A6:50
ip        : 10.1.10.6
vlan      : 10
int       : FastEthernet0/3

"""
