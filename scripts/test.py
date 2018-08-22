#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys,os,socket,struct
def socket_build():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(('115.182.224.11',8080))
    except socket.error as msg:
        print msg
        sys.exit(1)

   # print s.recv(1024)
    return s
def send(s):
    os.system("tar -jcf ../dpvs-ci.tar.bz2 ../dpvs")
    os.system("ls -la")
    while 1:
        filepath = '../dpvs-ci.tar.bz2'
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
            s.send(fhead)
            print 'client filepath: {0}'.format(filepath)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print '{0} file send over...'.format(filepath)
                    break
                s.send(data)
        s.close()
        sys.exit(0)

def run_commond(s,input_command):
    s.send(input_command)
    # 利用shutdown()函数使socket双向数据传输变为单向数据传输
    # 该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写
    s.shutdown(1)
    print '收到内容：\n'
    while 1:
        buff = s.recv(4096)
        if not len(buff):
            break
        sys.stdout.write(buff)
    flag = s.recv(1024)
    s.close()
    print '----------'
    print flag
    if flag == '0':
        sys.exit(0)
    else:
        sys.exit(1)



def build(s):
    input_command = './travis-ci.sh build'
    run_commond(s,input_command)

def deploy(s):
    input_command = './travis-ci.sh deploy'
    run_commond(s, input_command)

def test(s):
    input_command = './travis-ci.sh test'
    run_commond(s, input_command)

if __name__=="__main__":
    print 'start'
    s = socket_build()
    if sys.argv[1] == "send":
        send(s)
    elif sys.argv[1] == "build":
        build(s)
    elif sys.argv[1] == "deploy":
        deploy(s)
    elif sys.argv[1] == "test":
        test(s)
