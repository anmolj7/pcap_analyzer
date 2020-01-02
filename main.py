import subprocess as sp 
from functions import breakline, clrscr, take_input
import os 
from itertools import chain 
from collections import Counter


PCAP_FILE = None 

def return_text(fName):
    with open(fName) as f:
        return f.read()


def print_user_agents():
    output = sp.check_output(['tshark -r {} -Y http.request -T fields -e http.host -e http.user_agent | sort | uniq -c | sort -n'.format(PCAP_FILE)], shell=True)
    print(str(output, "utf8"))


def print_visited_sites():
    output = sp.check_output(["tshark -r {} -Y http.request -T fields -e http.host -e http.request.uri | sed -e 's/?.*$//' | sed -e 's#^(.*)t(.*)$#http://12#' | sort | uniq -c | sort -rn | head".format(PCAP_FILE)], shell=True)
    print(str(output, "utf8"))


def print_connection_details():
    output = sp.check_output(['tshark -r {}'.format(PCAP_FILE)], shell=True)
    print(str(output, "utf8"))


def print_grep():
    output = sp.call(["grep --binary-file=text -E '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' {}".format(PCAP_FILE)], shell=True)


def print_ips():
    output = sp.call(['tshark -r {} -T fields -e ip.dst ip.src | sort | uniq'.format(PCAP_FILE)], shell=True)


def print_ports():
    output = sp.check_output(['tshark -r {} -Y "tcp" -T fields -e tcp.srcport -e tcp.dstport'.format(PCAP_FILE)], shell=True)
    output = str(output, "utf8").split('\t')
    output = [port.split('\n') for port in output]
    output = Counter(list(chain.from_iterable(output)))
    for key in output:
        print(f'{key}: {output[key]}')


def main():
    global PCAP_FILE
    clrscr()
    print(return_text('heading.txt'))    
    breakline()
    fName = input('Enter The Pcap File Path: ')
    PCAP_FILE = fName
    assert os.path.isfile(fName), "File Doesn't Exist."

    options = ['Top 10 Visited Sites', 'User-Agents', 'Connection Details', 'Grep Mode', 'IP List', 'Ports Present', 'Clear', 'Exit']
    funcs = [print_visited_sites, print_user_agents, print_connection_details, print_grep, print_ips, print_ports, clrscr, exit]    

    while True:
        take_input(options, *funcs)


if __name__ == "__main__":
    main()