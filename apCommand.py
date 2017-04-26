
import time
import paramiko
import re
import pprint
import socket


#Global Variables


# Switch username
switch_un = "username"
# Switch password
switch_pw = "password"

ip= '10.155.4.5'


ipRe =re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
cidrRe = re.compile("(?<!\d\.)(?<!\d)(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}(?!\d|(?:\.\d))")


def openSSH(ip):
    firstRouterSession = paramiko.SSHClient()


    firstRouterSession.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    firstRouterSession.connect(ip, username=switch_un,password=switch_pw,look_for_keys=False, allow_agent=False)

    firstRouterShell = firstRouterSession.invoke_shell()
    print("SSH session established \n Commands and output will be displayed")


  # Strip the initial router prompt
    time.sleep(2)
    #output = disable_paging(firstRouterShell)
    output = firstRouterShell.recv(1000)
    print(output)

    text = switchCommand(firstRouterShell)

    time.sleep(1800)
    # #restart(firstRouterShell)
    return(firstRouterShell)




def switchCommand(session):
    '''Function that gets the Clients from a WLC's given LAN. Returns an array of:
    MAC Address       AP Name           Status        Auth Protocol         Port Wired Mobility Role  Device Type
    '''
    session.send("\n")
    session.send('conf t \n')
    time.sleep(1)
    session.send('int g1/48 \n')
    time.sleep(1)
    session.send('shut')

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
