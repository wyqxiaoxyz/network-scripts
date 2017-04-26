import socket, time, _thread

socket.setdefaulttimeout(3)


def socket_port(ip, port):

    try:
        if port >= 65535:
            print
            u'portscan completed'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            lock.acquire()
            print
            ip, u':', port, u'port open'
            lock.release()
        s.close()
    except:
        print
        u'portscan exception'


def ip_scan(ip):

    try:
        print
        u'start scanning %s' % ip
        start_time = time.time()
        for i in range(0, 65534):
            _thread.start_new_thread(socket_port, (ip, int(i)))
        print
        u'portscan completed, total time ：%.2f' % (time.time() - start_time)
        raw_input("Press Enter to Exit")
    except:
        print
        u'scan error'


if __name__ == '__main__':
    url = input('Input the ip you want to scan:\n')
    lock = _thread.allocate_lock()
    ip_scan(url)