import time
import paramiko
import re
import pprint
import socket


#Global Variables

#username = input('Enter your Username: ')
username = 'username'
#password = input('Enter your Password: ')
password = 'password'
#enablePass = input('Enter the Enable Password: ')
hostTest = '10.155.204.210'
command = 'show AP summary'

ipRe =re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
cidrRe = re.compile("(?<!\d\.)(?<!\d)(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}(?!\d|(?:\.\d))")

# start SSH session
def openSSH(hostname):
    firstRouterSession = paramiko.SSHClient()


    firstRouterSession.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    firstRouterSession.connect(hostname, username=username,password=password,look_for_keys=False, allow_agent=False)

    firstRouterShell = firstRouterSession.invoke_shell()
    print("SSH session established \n Commands and output will be displayed")


    # Strip the initial router prompt
    firstRouterShell.send("SJC12-RO\n")
    firstRouterShell.send("1ReadOnly1\n")
    time.sleep(2)

    # Turn off paging
    #disable_paging(firstRouterShell)

    output = firstRouterShell.recv(65535)
    print(output)

    text = getWlanAPs(firstRouterShell)
    print('Command sent')

    # skip --more--
    doneIndicater = False
    while doneIndicater == False:
        if '--More-- or (q)uit' in text :
            text = skipandScrape(firstRouterShell)
            print(' skip --more--  ')
    #     else :
    #         doneIndicater = True
    #         print('      End of Output       ')
    #
    # return(firstRouterShell)



def getWlanAPs(session):
    '''Function that gets the AP from a WLC. Returns an array of:
    AP Name   Slots  AP Model   Ethernet MAC   Location  Country  IP Address  Clients   DSE Location
    '''
    session.send("\n")
    session.send('show AP summary \n')
    # Wait for the command to run
    time.sleep(4)
    output = session.recv(65535)
    output = formatOutput(output)
    deviceArray = []
    for index, item in enumerate(output):
        print(index)
        print(item)
        if 'AIR-CAP3702I-A-K9' in item:
            deviceArray.insert(-1, output[index])


    print('APs are: ')
    print(deviceArray)
    with open("SJC12APList.txt",'a') as f:
        for item in deviceArray:
            f.write(item+'\n')

    return output

def skipandScrape(session):
    #Function that only gets a list of APs

    session.send('show AP summary ')
    time.sleep(2)
    output = session.recv(50000)
    output = formatOutput(output)
    deviceArray = []
    for index, item in enumerate(output):
         print(index)
         print(item)
         if 'AIR-CAP3702I-A-K9' in item:
             deviceArray.insert(-1, output[index])
    print(deviceArray)
    with open("SJC12APList.txt",'a') as f:
        for item in deviceArray:
            f.write(item+'\n')
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

# def showIpRoutes(session):
#     '''Function to get routes from Show Ip Route'''
#     session.send("\n")
#     session.send('show ip route\n')
#     time.sleep(2)
#     output = session.recv(5000)
#     output = formatOutput(output)
#     routes = getCIDRinText(output)
#     print("Routes: ")
#     print(routes)
#     return routes


# def disable_paging(firstRouterShell):
#     '''
#     Disable the paging of output (i.e. --More--)
#     '''
#     firstRouterShell.send('config paging disable')
#     # Wait for the command to complete
#     time.sleep(2)
#     output = firstRouterShell.recv(65535)
#     return output


openSSH(hostTest)