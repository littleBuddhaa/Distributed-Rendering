
import socket               # Import socket module
import thread
import time
import os
import subprocess

cpulist = []
count  =0
file_rec_count=0 
Tframes =0
startEnd = []
failiure = []
st = 0
en = 0
def on_new_client(clientsocket,addr,filename,mynum,waittime):
    #clientsocket.send(isfile)
    #if isfile =='y':
    global count
    global file_rec_count
    flag = 1
    #clientsocket.send(str(format))
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
            startEnd.append((l[0],l[1]))
            clientsocket.send(str(l[0]))
            clientsocket.send(str(l[1]))
            flag =0
    m = clientsocket.recv(1024)
    if(m[:] == "Failed"):
        print('Rendering failed at ' + str(mynum))
    else:
        output = clientsocket.recv(1024) #receiving rendered file name and its size
        out = output.split(" ")
        print((out[1]) , " sd " , out[0]) # filename , filesize
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
            if(totalRecv>= int(out[1])): #stop receiving if length of file <= total received data
                break

            data = clientsocket.recv(1024)

            totalRecv =totalRecv  + len(data)
            print(totalRecv)
            f.write(data)
            print('receiving data...')
        print('File Received')
        f.close()
    
    print('Successfully got the file')
   


def jobscheduler(mynum): # gives as equal as possible jobs , was used initially
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

def CPUjobscheduler(mynum): # schedules jobs on the basis of system configs
    global Tframes
    s =0
    for x  in cpulist:
        s = s + int(x[1]) #sum of all weights
    #print(s)
    #t = float(s*0.001)

    t = float(Tframes/float(s)) #total frames/total weight
    print(t)
    #print(cpulist[mynum-1][1])

    myShare = (t*float(cpulist[mynum-1][1])) #(total frames/ total weight)*own weight
    #print("My share =" ,myShare) # number of frames in float

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

def ping_check(clientsocket,host,port,h,mynum):
    global file_rec_count
    global count

    while(True):
        
        if(file_rec_count ==count): # start to ping when file received , pings during rendering 
            break 
 
    print(port,h)
    count =0
    while(True):
        #res = os.system(["ping -c 1 " + str(hnam)])
        res = subprocess.check_output(["ping" , "-c" , "1", h[:-1]]) # sends one ping to connected host (client) 
        #if(res ==0):
        print(res)
        if res==1: # if down (returns 1 for down 0 for success) 
            count = count+1
        
        else:
            count =0
        if(count >=10):
            failedClient(clientsocket,port,h,mynum)
            break

        break
        time.sleep(3) # pings in every 3 sec
    
    clientsocket.close()
    
    
def failedClient(clientsocket,port, h,mynum):
    global client
    print("Client number " , mynum , " crashed")
    s = startEnd[mynum-1][0]
    e = startEnd[mynum-1][1]
    failiure.append([mynum,s,e])
    l = len(startEnd)

    subprocess.call(['blender', '-b' ,'move.blend', '-o' ,'//rec/render_','-s',str(start), '-e' , str(end),'-F', 'MPEG' ,'-x' ,'1', '-a'])



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
#print('enter the output format. Type 1 for PNG, 2 for mkv')
#format = int(raw_input())
print 'set your time to connect all clients'
waittime = int(raw_input())
print 'Waiting for clients... Connect all clients within ' + str(waittime)   +' sec'

#print isfile

s.bind(('', port))       
s.listen(5)                
host = socket.gethostname()
mynum = 0
while True:
   c, addr = s.accept()     
   count = count +1
   mynum = mynum +1


   print 'Got connection from', addr
   print 'Total number of connections = ' , count
   clientHostName = c.recv(1024)
   print("Client = " ,clientHostName )
   
   thread.start_new_thread(on_new_client,(c,addr,filename,mynum,waittime))
   #thread.start_new_thread(ping_check,(c,host,addr[1],clientHostName,mynum))



s.close()
#ps -fA | grep python
