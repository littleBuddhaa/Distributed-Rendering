# Distributed-Rendering
Implementing Distributed Rendering for Blender

<h3>Installation</h3>
Have Python 2.7 installed <br>
install Blender from command---> sudo apt install blender<br>
pip install subprocess <br>
sudo apt install sysstat <br>

<h3>Note</h3>
--change host ='' variable to the ip address of the server. (Ex host = '172.32.0.111')<br><br>

--In client.py getCPUper() function might need to be changed for some systems because the system call returns the host name too which is different for each system. 
Set the variables a,b,c,e so that they correspond to last characters of d (excluding the spaces ). This part is a percentage of the format ab.ce% where  a will be d[-i],b = d[-i-1],c = d[-i-3] , e = d[-i-4]. For my system i was 8, this may varry in other systems. 

<h3>Run</h3>
--run the server by command ---> python multiserver.py<br>
--run the clients by command ---> python client.py
