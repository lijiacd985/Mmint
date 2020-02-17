import sys

files = sys.argv[1:]
dic={}
mark=True
for file in files:
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        t = line.strip().split()
        pos=t[0]+'-'+t[1]+'-'+t[2]
        if pos in dic:
            dic[pos].append([float(t[3]),int(t[4]),int(t[5])])
        else:
            if mark: dic[pos]=[[float(t[3]),int(t[4]),int(t[5])]]
    mark=False

for pos in dic:
    if len(dic[pos])!=len(files): continue
    c,s,t=pos.split('-')
    #print(c,s,t)
    temp=c+'\t'+s+'\t'+t
    for info in dic[pos]:
        temp=temp+'\t'+str(info[0])
    temp=temp+'\n'
    print(temp)



