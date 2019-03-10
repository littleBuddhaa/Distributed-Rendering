import subprocess


d = subprocess.check_output(['iostat','-c'])


a = (d[-8])
b  =(d[-7])
c = (d[-5])
d = (d[-4])
print a,b + '.' +c,d

cpu = int(a)*10 + int(b)*1 + int(c)*0.1 + int(d)*0.01
print cpu