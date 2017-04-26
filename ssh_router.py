import paramiko

if __name__ == "__main__":

    ip = '10.155.237.239'
    username = 'yinqwu.web'
    password = '123'

    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip, username=username, password=password)
    remote_conn = self.remote_conn_pre.invoke_shell()
    output = remote_conn.recv(5000)
    print(output)

# remote_conn.send("\n")
# remote_conn.send("show version\n")

#wait for the command to complete
time.sleep(1)

output = remote_conn.recv(65535)
print(output)
