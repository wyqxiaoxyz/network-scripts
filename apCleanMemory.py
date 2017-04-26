"""Chen Wu 2016- Python Script to connect to multiple APs, add a specific command and logout."""
import os
import sys
import pexpect
import subprocess
import time
import logging
import paramiko
import re
import pprint
import socket

#Global Variables

#username = input('Enter your Username: ')
apun = 'username'
#password = input('Enter your Password: ')
appw = 'password'
ip = '171.70.250.166'


# open the AP list file
f = open('SJC12APList.txt', 'r')
ap_details = f.read()
f.close()

# extract IP address of every AP
ap_addr = []
ap_data_line = ap_details.split("\n")
for line in ap_data_line:
    ap_data_single = line.split("  ")

    for single in ap_data_single:
        print(single)
        if '171' in single:
            ap_addr.insert(-1, single)


ipRe =re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
cidrRe = re.compile("(?<!\d\.)(?<!\d)(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}(?!\d|(?:\.\d))")


def openSSH(ip):
    # function that starts the ssh session

    firstRouterSession = paramiko.SSHClient()
    firstRouterSession.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    firstRouterSession.connect(ip, username=apun,password=appw,look_for_keys=False, allow_agent=False)
    firstRouterShell = firstRouterSession.invoke_shell()
    print("SSH session established \n Commands and output will be displayed")


    # Strip the initial router prompt
    time.sleep(2)
    #output = disable_paging(firstRouterShell)
    output = firstRouterShell.recv(1000)
    print(output)

    text = apCommand(firstRouterShell)

    time.sleep(1800)
    # #restart(firstRouterShell)
    return(firstRouterShell)


def apCommand(session):
    '''Function that gets the Clients from a WLC's given LAN. Returns an array of:
    MAC Address       AP Name           Status        Auth Protocol         Port Wired Mobility Role  Device Type
    '''
    session.send("\n")
    session.send("en")
    session.send("\n")
    time.sleep(1)
    session.send(appw)
    session.send("\n")
    time.sleep(1)


    with open('ap_memory_workaround.txt', 'r') as commands:
        for items in commands:
            end = str('exit1')
            if 'exit1' in items:
                break
            else:
                session.send(items)


    # Wait for the command to run
    time.sleep(4)
    output = session.recv(2000)
    output = formatOutput(output)
    print(output)

    return output


def formatOutput(output):
    '''Function to format the SSH returned outout into a string'''
    formated = output.decode('utf-8')
    formated = formated.split('\r\n')
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(formated)
    return formated


def getIPinText(text):
    ipArray = []
    for iterable in text:
        if ipRe.search(iterable) != None:
            ipArray.append(ipRe.search(iterable).group(0))
    return ipArray

def getCIDRinText(text):
    ipArray = []
    for iterable in text:
        if cidrRe.search(iterable) != None:
            ipArray.append(cidrRe.search(iterable).group(0))
    return ipArray
openSSH(ip)

# with open(os.devnull, "wb") as limbo:
#     for ip in ap_addr:
        # result = subprocess.Popen(["ping", "-n", "1",ip],
        #                           stdout=limbo, stderr=limbo).wait()
        # if result:
        #     logger.info('%s is not an active ap, skipping', ip)
        #     print('%s is not an active ap, skipping -X_X-' % ip)
        # else:
        #     print(ip, "host is available")
