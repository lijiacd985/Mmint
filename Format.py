
def formdata(files,cov=0):
    dic={}
    for file in files:
        with open(file) as f:
            for line in f:
                if line[0]=='#': continue
                t = line.strip().split()
                key=(t[0],t[1],t[2])
                if len(t)>4 and int(t[4])<cov: continue
                if not key in dic:
                    dic[key]=[t[3]]
                else:
                    dic[key].append(t[3])

    result=[]
    for key in dic:
        if len(dic[key])==len(files):
            result.append(dic[key])
    return result

if __name__=="__main__":
    formdata([1,2,3])
