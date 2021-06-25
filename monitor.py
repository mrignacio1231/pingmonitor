import subprocess
import platform
import itertools
from functools import reduce
import multiprocessing

ip2int = lambda ip: reduce(lambda a,b: int(a) * 256 + int(b), ip.split('.'))

int2ip = lambda num: '.'.join([ str((num >> 8*i) % 256 ) for i in [3,2,1,0]])

def iter_iprange(start, stop, step=1):
    start = ip2int(start)
    stop = ip2int(stop)

    negative_step = False
    if step < 0:
        negative_step = True

    index = start - step

    while True:
        index += step
        if negative_step:
            if not index >= stop:
                break
        else:
            if not index <= stop:
                break
        yield int2ip(index)


def load_hosts():
    with open('hosts.txt') as f:
        return (i.strip() for i in f.readlines())

def parse_host(hosts):
    new_hosts = []
    for host in hosts:
        if '-' in host:
            start, end = host.split('-')
            new_hosts.extend(iter_iprange(start, end))
        else:
            new_hosts.append(host)
    return new_hosts

def ping(host='127.0.0.1'):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W 1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def check_connectivity(host):
    if ping(host):
        return host, True

    return host, False

if __name__ == '__main__':
    hosts = parse_host(load_hosts())
    pool = multiprocessing.Pool(None)

    r = pool.map(check_connectivity, hosts)
    
    for d in r:
        host, result = d
        if result:
            print(f'{host} is UP')
        else:
            print(f'{host} is DOWN')