"""Script to connect to multiple switches, add a specific command and logout."""

import os
import sys
import pexpect
import subprocess
import time
import logging

# device_list = open('device_list.txt', 'r')
# count_lines = 0
#
# start_time = time.time()
# details = open("Details.log", "w")
#
# logger = logging.getLogger('info_logger')
# logger.setLevel(logging.DEBUG)
# # Create file handler which logs even debug messages
# fh = logging.FileHandler('Info.log', 'w')
# fh.setLevel(logging.DEBUG)
# # Create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# # Create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # Add the handlers to logger
# logger.addHandler(ch)
# logger.addHandler(fh)

# Switch username
switch_un = "username"
# Switch password
switch_pw = "password"

ip= '10.155.4.5'

# Function that will be called to send commands to the switch
def main(ip):
    try:
        child = pexpect.spawn('ssh %s@%s' % (switch_un, ip))
        # child.logfile = details
        child.timeout = 60
        i = child.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF, 'Connection refused', 'Connection timed out',
                          'Connection refused by server'], timeout=120)
        if i == 0:
            child.sendline(switch_pw)
            child.expect('#')
            child.sendline('conf t')
            child.expect('\(config\)#')
            child.sendline('int g1/48')
            child.expect('\(config-if\)#')
            child.sendline('shut')
            # with open('commands.txt', 'r') as commands:
            #     for items in commands:
            #         end = str('exit1')
            #         if 'exit1' in items:
            #             break
            #         else:
            #             child.sendline(items)
            #             child.expect('#')
            child.sendline('end')
            child.expect('#')
            output = child.read(self,2000)

            child.sendline('quit')
            # logger.info('%s has been sucessfully configured', ip)
            print('%s has been sucessfully configured -o_0-' % ip)
            sys.exit
        elif i == 1:
            # logger.info('%s : Timeout', ip)
            print('%s : Timeout' % ip)
            sys.exit
        elif i == 2:
            # logger.info('%s : Reached EOF', ip)
            print('%s : Reached EOF' % ip)
            sys.exit
        elif i == 3:
            # logger.info('%s : Connection refused', ip)
            print('%s : Connection refused' % ip)
            sys.exit
        elif i == 4:
            # logger.info('%s : Connection Timed Out', ip)
            print('%s : Connection Timed Out' % ip)
            sys.exit
        elif i == 5:
            # logger.info('%s : Connection refused by server', ip)
            print('%s : Connection refused by server' % ip)
            sys.exit
    except:
        raise

main(ip)
#
# with open(os.devnull, "wb") as limbo:
#     for ip in device_list:
#         result = subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
#                                   stdout=limbo, stderr=limbo).wait()
#         if result:
#             logger.info('%s is not an active switch, skipping', ip)
#             print('%s is not an active switch, skipping -X_X-' % ip)
#         else:
#             main(ip)
#
#
# device_list.close()
# details.close()
# print("--- %s seconds ---" % str(time.time() - start_time))
