import socket
import time 
import subprocess
import os
host = ''
port = 50000


s = socket.socket()
s.connect((host, port))
subprocess.call(['rm' , '-rf' , 'rec'])
#s.setblocking(False)
print 'Connection Established from server '
#get cpu %

def getCPUper():
    d = subprocess.check_output(['iostat','-c'])
    a = (d[-8])
    b  =(d[-7])
    c = (d[-5])
    dd = (d[-4])
    cpu = int(a)*10 + int(b)*1 + int(c)*0.1 + int(dd)*0.01
    #print 'My idle CPU percentage is '+ str(cpu)  
    return str(cpu); 
    
def recvFile(fileSize):
    s.send("SEND")
    with open('received_file.blend', 'wb') as f:
        print 'file opened'
        data = s.recv(1024)
        #print(data)
        totalRecv = len(data)
        print(totalRecv)

        f.write(data)

        while True:
            if(totalRecv>= int(fileSize)):
                break

            data = s.recv(1024)

            totalRecv =totalRecv  + len(data)
            print(totalRecv)
            f.write(data)
            print('receiving data...')
        print('File Received')
        f.close()
    
    print('Successfully got the file')
    
def getProc():
    d = subprocess.check_output(['nproc', '--all'])
    print 'Number of cores = ' +str(d)
    return d

def getCPUspeed():
    d = subprocess.check_output(['lscpu'])

    t = d.find('CPU max MHz')
    e = d.find('CPU min MHz')
    print(t)
    print(e)
    st = d[t+12:e]
    st.replace(" ", "")
    print(float(st))
    return float(st)

def getRAM(): #ram in MB
    d = subprocess.check_output(['vmstat', '-s'])
    t = d.find('total memory')
    ram = d[:t-3]
    ram.replace(" ","")

    print(int(ram))
    print(int(ram)/1024)
    return int(ram)/1024

#def flush(self):
    #self.buffer+=(BUFFER_SIZE-len(self.buffer)%BUFFER_SIZE)*"\x00"

def goRender(start , end , F):
    print(F)
    try:
        subprocess.call(['blender', '-b' ,'received_file.blend', '-o' ,'//rec/render_','-s',str(start), '-e' , str(end),'-F', str(F) ,'-x' ,'1', '-a'])
        s.send("Successfull Render")
    except:
        print('Failed to render !')
        s.send("Failed")        
     

cpu = getCPUper()
processors = getProc()
speed = getCPUspeed()
ram = getRAM() # in mb

format = s.recv(1024) # receiving format
if(int(format) ==1 ):

    F = "PNG"

elif (int(format) ==2):
    F = "MPEG"

send = str(cpu)+","+str(processors) +"," + str(speed) +"," + str(ram)
print(send)
try:
    s.send(send) #sendCPUper
except:
    'Did not send params'


#receive file from server
fileSize = s.recv(1024)
print("filesize = " + fileSize)
recvFile(fileSize) # receive file from server

s.send('Got')
start = s.recv(1024) #start param
end = s.recv(1024) # end param
print("start = " + start + " end = " + end)
goRender(int(start), int(end), F) #call rendering
outfilename = subprocess.check_output(['ls' ,'rec'])
outfilename = outfilename.rstrip()

outsize = str(os.path.getsize('rec/' + outfilename))
print(outfilename+ ","+ str(outsize) )
s.send(outfilename + " "+str(outsize) )

m = s.recv(1024)
print(m)
if(m[:] =="send"):
    f = open( 'rec/' + outfilename,'rb')
    l = f.read(1024)
    s.send(l)
    print 'Sending file to Server'
    while (l) :
        l = f.read(1024)
        s.send(l)
    f.close()


 #connection closed

s.close()
    