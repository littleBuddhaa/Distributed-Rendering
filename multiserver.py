
import socket               # Import socket module
import thread
import time
import os

cpulist = []
count  =0
file_rec_count=0 
Tframes =0
st = 0
en = 0
def on_new_client(clientsocket,addr,filename,mynum,waittime,format):
    #clientsocket.send(isfile)
    #if isfile =='y':
    global count
    global file_rec_count
    flag = 1
    clientsocket.send(str(format))
    #frame_start = 0
    #frame_end = Tframes
    try:
        cpu =  clientsocket.recv(1024)
    except:
        print('Parameters not received, Connecet again')

    cpuInfo = cpu.split(',')
    fileSize = str(os.path.getsize(filename))
    #print cpu
    print ('Idle CPU of client ' + str(mynum) + ' = ' + cpuInfo[0][:] + ' no of processor = ' +cpuInfo[1][:] + ' RAM in mb = ' + cpuInfo[2][:] + ' CPU speed = ' + cpuInfo[3][:] + ' MHz' )
    w = getMyWeight(cpuInfo)
    #send file size()
    clientsocket.send(fileSize)
    
    cpulist.append([mynum,w])

    #cpulist.sort(key=lambda x: x[1])
    print(cpulist)
    print'Waiting for more clients...'
    time.sleep(waittime)


    #file sendinggggg---------------
    confirmation = clientsocket.recv(1024)
    if(confirmation[:] =="SEND"):
        f = open(filename, 'rb')
        l = f.read(1024)
        clientsocket.send(l)
        print 'Sending file to connection no.', mynum
        while (l) :
            l = f.read(1024)
            clientsocket.send(l)
        f.close()
    else:
        print("Kuch toh kaho")


    #clientsocket.send("sominee")
    print('File sent')
    #--------------------------------

    file_mili = clientsocket.recv(1024)
    if(file_mili[:] == 'Got'):
        print 'Sent targate file'
        file_rec_count = file_rec_count + 1

    
    
    


    #######for i,j in cpulist:
    ########    print( i,j)
    while(flag):
        if(file_rec_count == count):
            l = CPUjobscheduler(mynum)
        
            clientsocket.send(str(l[0]))
            clientsocket.send(str(l[1]))
            flag =0
    m = clientsocket.recv(1024)
    if(m[:] == "Failed"):
        print('Rendering failed at ' + str(mynum))
    else:
        output = clientsocket.recv(1024)
        out = output.split(" ")
        print((out[1]) , " sd " , out[0])
    clientsocket.send("send")
    filename = 'outputs/'  +out[0]  
    with open(filename, 'wb') as f:
        print 'file opened'
        data = clientsocket.recv(1024)
        #print(data)
        totalRecv = len(data)
        print(totalRecv)

        f.write(data)

        while True:
            if(totalRecv>= int(out[1])):
                break

            data = clientsocket.recv(1024)

            totalRecv =totalRecv  + len(data)
            print(totalRecv)
            f.write(data)
            print('receiving data...')
        print('File Received')
        f.close()
    
    print('Successfully got the file')
   


def jobscheduler(mynum):
    global Tframes
    global count
    if(Tframes%count==0):
        start = (Tframes/count )*(mynum -1) +1
        end = start + (Tframes/count) -1  # assuming no 0th frame is there 
    else:
        quotient = int(Tframes/count)  + 1
        NewTotal = count*quotient
        start = (NewTotal/count )*(mynum -1) +1
        e1 = start + (NewTotal/count) 
        if(e1 < Tframes):
            end = e1
        else:
            end = Tframes
    
    print(str(start) +" " + str(end))
    return [start, end]


def getMyWeight(cpuInfo):
    a = (float(cpuInfo[1][:])*float(cpuInfo[0][:])*float(cpuInfo[2][:]))/100000
    return int(a) 

def CPUjobscheduler(mynum):
    global Tframes
    s =0
    for x  in cpulist:
        s = s + int(x[1])
    #print(s)
    #t = float(s*0.001)

    t = float(Tframes/float(s))
    print(t)
    #print(cpulist[mynum-1][1])

    myShare = (t*float(cpulist[mynum-1][1]))
    print("My share =" ,myShare)

    global st, en
    start = 0
    end = 0
    for i in range(mynum):
        if i == 0:
            start = 1
            end = start + int(t*float(cpulist[i][1])) -1
        else:
            start = end  +1
            end = start  + int(t*float(cpulist[i][1])) -1
        if(i + 1 ==count):
            end = Tframes

    return start , end  


s = socket.socket()  
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      
#host = socket.gethostname() 
port = 50000               
fileUrl = '/home/sominee/Desktop/distributed_system/movie.blend'
print 'Server started!'
while(True):
    print 'enter the name of the file (with extension)'
    filename = raw_input("->")
    if(os.path.isfile(filename)):
        break
    else:
        print('File Does not exist! Enter Again')

print 'enter the number of total frames you want to render - '
Tframes = int(raw_input("->")) 
print('enter the output format. Type 1 for PNG, 2 for mkv')
format = int(raw_input())
print 'set your time to connect all clients'
waittime = int(raw_input())
print 'Waiting for clients... Connect all clients within ' + str(waittime)   +' sec'

#print isfile

s.bind(('', port))       
s.listen(5)                

mynum = 0
while True:
   c, addr = s.accept()     
   count = count +1
   mynum = mynum +1


   print 'Got connection from', addr
   print 'Total number of connections = ' , count
   
   thread.start_new_thread(on_new_client,(c,addr,filename,mynum,waittime,format))



s.close()
#ps -fA | grep python
