import socket
import time 
import subprocess

host = ''
port = 50000


s = socket.socket()
s.connect((host, port))
print 'Connection Established from server '

d = subprocess.check_output(['iostat','-c'],shell=True)
a = (d[-8])
b  =(d[-7])
c = (d[-5])
dd = (d[-4])
cpu = int(a)*10 + int(b)*1 + int(c)*0.1 + int(dd)*0.01
print 'My idle CPU percentage is '+ str(cpu)   


s.send(str(cpu))

with open('received_file.blend', 'wb') as f:
    print 'file opened'
    while True:
        print('receiving data...')
        data  =s.recv(1024)
        if not data:
            break
        f.write(data)
        
f.close()

print('Successfully got the file')

s.close()


