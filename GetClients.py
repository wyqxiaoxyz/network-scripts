
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


ipRe =re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
cidrRe = re.compile("(?<!\d\.)(?<!\d)(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}(?!\d|(?:\.\d))")



def openSSH( hostname):
    firstRouterSession = paramiko.SSHClient()


    firstRouterSession.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())
    firstRouterSession.connect(hostname, username=username,password=password,look_for_keys=False, allow_agent=False)

    firstRouterShell = firstRouterSession.invoke_shell()
    print("SSH session established \n Commands and output will be displayed")

    # Turn off paging
    #disable_paging(firstRouterShell)
    # def disable_paging(firstRouterShell):
    #     '''
    #     Disable the paging of output (i.e. --More--)
    #     '''
    #     firstRouterShell.send("\n")
    #
    #     firstRouterShell.send(" config paging disable \n")
    #
    #     # Wait for the command to complete
    #     time.sleep(1)
    #
    #     output = firstRouterShell.recv(65535)
    #
    #     return output




    # Strip the initial router prompt
    firstRouterShell.send("username\n")
    firstRouterShell.send("password\n")
    time.sleep(2)
    #output = disable_paging(firstRouterShell)
    output = firstRouterShell.recv(1000)
    print(output)
    wlan = '1'

    text = getWlanClients(firstRouterShell,wlan)
    doneIndicater = False

    while doneIndicater == False:
        if 'Would you like to display the next 15 entries? (y/n) ' in text :
            text = enterYesandScrape(firstRouterShell)
        else :
            doneIndicater = True
            print('      End of Output       ')
    time.sleep(1800)
    # #restart(firstRouterShell)
    return(firstRouterShell)




def getWlanClients(session, wlan):
    '''Function that gets the Clients from a WLC's given LAN. Returns an array of:
    MAC Address       AP Name           Status        Auth Protocol         Port Wired Mobility Role  Device Type
    '''
    session.send("\n")
    session.send('show client wlan 1 \n')
    # Wait for the command to run
    time.sleep(4)
    output = session.recv(2000)
    output = formatOutput(output)
    deviceArray = []
    for index, item in enumerate(output):
        if ':' in item:
            deviceArray.insert(-1, output[index])


    print('WLAN Clients are: ')
    print(deviceArray)
    with open("devices.txt",'a') as f:
        for item in deviceArray:
            f.write(item+'\n')

    return output

def enterYesandScrape(session):
    session.send('y')
    time.sleep(2)
    output = session.recv(2000)
    output = formatOutput(output)
    deviceArray = []
    for index, item in enumerate(output):
        if ':' in item:
            deviceArray.insert(-1, output[index])
    print(deviceArray)
    with open("devices.txt",'a') as f:
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



openSSH(hostTest)
