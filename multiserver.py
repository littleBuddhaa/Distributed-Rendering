
import socket               # Import socket module
import thread
import time


cpulist = []
count=0 
file_rec_count=0 

def on_new_client(clientsocket,addr,Tframes,filename,mynum,waittime,file_rec_count):
    #clientsocket.send(isfile)
    #if isfile =='y':
    global count
    global file_rec_count
    frame_start = 0
    frame_end = Tframes

    cpu =  clientsocket.recv(1024)
    cpu = float(cpu)
    cpu = int(cpu)
    #print cpu
    print ('Idle CPU of client ' + str(mynum) + ' = ' + str(cpu) )
    cpulist.append([mynum,cpu])
    cpulist.sort(key=lambda x: x[1])

    print'Waiting for more clients...'
    time.sleep(waittime)
    f = open(filename, 'rb')
    l = f.read(1024)
    print 'Sending file to connection no.', mynum
    while (l) :
        clientsocket.send(l)
        l = f.read(1024)

    f.close()
    print 'Sent targate file'
    file_rec_count = file_rec_count + 1 



    
    frames_for_one = (Tframes/count)
    #print(frames_for_one)
    

    for i,j in cpulist:
        print( i,j)
    #check if all the clients sent their info
    #time.sleep(5)
    #if(file_rec_count == count) :
        #job_scheduler(mynum) #send parameters to the client using their data
    
    
    clientsocket.close()


















def main():

    s = socket.socket()        
    #host = socket.gethostname() 
    port = 50000    
    global count
    global file_rec_count           
    fileUrl = '/home/sominee/Desktop/distributed_system/movie.blend'
    print 'Server started!'
    print 'enter the name of the file (with extension)'
    filename = raw_input("->")
    print(filename)
    print 'enter the number of total frames you want to render - '
    Tframes = int(raw_input("->")) 
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
        
        thread.start_new_thread(on_new_client,(c,addr,Tframes,filename,mynum,waittime,file_rec_count))



    s.close()

if __name__ == "__main__":
    main()