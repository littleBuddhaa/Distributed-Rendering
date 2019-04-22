import subprocess


d = subprocess.check_output(['iostat','-c'])


a = (d[-8])
b  =(d[-7])
c = (d[-5])
d = (d[-4])
print a,b + '.' +c,d

cpu = int(a)*10 + int(b)*1 + int(c)*0.1 + int(d)*0.01
print cpu

def speed():
    d = subprocess.check_output(['lscpu'])

    t = d.find('CPU max MHz')
    e = d.find('CPU min MHz')
    print(t)
    print(e)
    st = d[t+12:e]
    st.replace(" ", "")
    print(float(st))
    return st

a = speed()
print a

d = subprocess.check_output(['vmstat', '-s'])
t = d.find('total memory')
ram = d[:t-3]
ram.replace(" ","")

print(int(ram))
print(int(ram)/1024)
