import socket
import time
import sys
from tem import testHDC1080
import LED
import stu_management1


#设置IP和端口
host = '192.168.43.122'
port = 5000
print("服务端开启")
#套接字接口
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#立即释放端口
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#bind绑定该端口
mySocket.bind((host, port))
mySocket.listen(1)
tem = testHDC1080.TempHum()
led = LED.Led()




while True:
    #接收客户端连接
    print("等待连接....")
    client, address = mySocket.accept()
    print("新连接")
    print("IP is %s" % address[0])
    print("port is %d\n" % address[1]) 
    while True:
        try:
            #read.Door()
            #读取消息
            msg = client.recv(1024)
            if msg == b"close":
                client.close()
                mySocket.close()
                print("通信结束\n")
                sys.exit(1)
        #把接收到的数据进行解码
            if len(msg)>0:
                uid=msg.decode("utf-8")
                print(uid)
                print(tem.read())
                stu_management1.add_temp(uid,tem.read())
                led.blue()
            #led.clean()
        except Exception:
            client.close()
            mySocket.close()
            print('error\n')
            print("通信结束\n")
            ssys.exit(1)