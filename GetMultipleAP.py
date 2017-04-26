"""Chen Wu 2016- Python
Script to connect to multiple APs, add a specific command and logout."""
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





# open the txt file
f = open('SJC12APList.txt', 'r')
ap_details = f.read()
f.close()

# extract IP address
ap_addr = []
ap_data_line = ap_details.split("\n")
for line in ap_data_line:
    ap_data_single = line.split("  ")

    for single in ap_data_single:
        print(single)
        if '171' in single:
            ap_addr.insert(-1, single)


#log file

count_lines = 0

start_time = time.time()
details = open("Details.log","w")

logger = logging.getLogger('info_logger')
logger.setLevel(logging.DEBUG)
#Create file handler which logs even debug messages
fh = logging.FileHandler('Info.log', 'w')
fh.setLevel(logging.DEBUG)
#Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
#Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
#Add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)



#username = input('Enter your Username: ')
username = 'apadmin'
#password = input('Enter your Password: ')
password = 'kL1f0rn1a'



def main(ip):
    try:

            child = pexpect.spawn('ssh %s@%s' % (username, ip))
            child.logfile = details
            child.timeout = 60
            i = child.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF, 'Connection refused', 'Connection timed out',
                          'Connection refused by server'], timeout=120)
            if i == 0:
                child.sendline(password)
                child.expect('>')
                child.sendline('en')
                child.timeout = 60
                child.expect('Password:')
                child.sendline(password)
                child.expect('#')
                with open('ap_memory_workaround.txt', 'r') as commands:
                    for items in commands:
                        end = str('exit1')
                        if 'exit1' in items:
                            break
                        else:
                            child.sendline(items)
                            child.expect('#')
                child.sendline('quit')
                logger.info('%s has been sucessfully configured', ip)
                print('%s has been sucessfully configured -o_0-' % ip)
                sys.exit
            elif i == 1:
                logger.info('%s : Timeout', ip)
                print('%s : Timeout' % ip)
                sys.exit
            elif i == 2:
                logger.info('%s : Reached EOF', ip)
                print('%s : Reached EOF' % ip)
                sys.exit
            elif i == 3:
                logger.info('%s : Connection refused', ip)
                print('%s : Connection refused' % ip)
                sys.exit
            elif i == 4:
                logger.info('%s : Connection Timed Out', ip)
                print('%s : Connection Timed Out' % ip)
                sys.exit
            elif i == 5:
                logger.info('%s : Connection refused by server', ip)
                print('%s : Connection refused by server' % ip)
                sys.exit
    except:
        raise


#For loop that will loop through APs in a specific range

with open(os.devnull, "wb") as limbo:
    for ip in ap_addr:
        # result = subprocess.Popen(["ping", "-n", "1",ip],
        #                           stdout=limbo, stderr=limbo).wait()
        # if result:
        #     logger.info('%s is not an active ap, skipping', ip)
        #     print('%s is not an active ap, skipping -X_X-' % ip)
        # else:
        #     print(ip, "host is available")
            main(ip)



# ping APs in the loop
# for ip in ap_addr:
#     response = os.system("ping -n 1 " + ip)
#    #and then check the response...
#     if response == 0:
#         print(ip, 'is up!')
#     else:
#         print (ip, 'is down!')



