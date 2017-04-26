import getpass
import sys
import telnetlib
import paramiko
import time

#Ask for the user name and password
#Left enable password option if needed
username = raw_input("Username: ")
password = getpass.getpass()
#print "Enter enable password: "
#enablepass = getpass.getpass()

host = raw_input("Router: ")
host = host.strip()
	#username = raw_input("Username: ")
	#password = getpass.getpass()
port = 22
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	ssh.connect(host, port, username, password)
except:
	print "Host name and/or password is incorrect"
#continue
	
print "Connecting to router..."
print "connected to router: " + host
ssh_con = ssh.invoke_shell()
print "Interactive SSH session established"

#output = ssh_con.recv(100000)
#ssh_con.send("terminal length 0\n")
#print output
time.sleep(2)
ssh_con.send("\n")
ssh_con.send("\n")
ssh_con.send("terminal length 0\n")
ssh_con.send("ping www.google.com\n")
ssh_con.send("\n")
time.sleep(2)
ssh_con.send("\n")
ssh_con.send("ping www.cisco.com\n")	
ssh_con.send("\n")
ssh_con.send("\n")
#print output
time.sleep(2)

output = ssh_con.recv(100000)
print output



	



