#!/usr/bin/env python

from os import rename, replace
from os.path import abspath, dirname, join
from subprocess import check_output

script = abspath(join(dirname(__file__), 'list-hosts.sh'))
mapfile = join(dirname(__file__), 'mapfile.txt')
tempfile = join(dirname(__file__), 'temp')

def save_map(mac_map):
    with open(tempfile, 'w') as f:
        for mac,oid in sorted(mac_map.items()):
            f.write('{} {}\n'.format(mac,oid))
    replace(tempfile, mapfile)

def load_map():
    mac_map = {}
    try:
        with open(mapfile) as f:
            for line in f:
                (mac,oid) = line.strip().split(' ', 1)
                mac_map[mac] = oid
    except FileNotFoundError:
        pass
    return mac_map

def main():
    mac_map = load_map()
    hosts = check_output(['sudo',script]).decode('utf-8').splitlines()
    for h in hosts:
        (ip,mac,oid) = (h.split(' ', 2) + ['', ''])[0:3]
        if mac and mac not in mac_map:
            mac_map[mac] = oid
        nick = mac_map.get(mac, '')
        print('{}\t{}\t{}'.format(ip, mac, nick))
    save_map(mac_map)
    return 0

if __name__ == '__main__':
    exit(main())
