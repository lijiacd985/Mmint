def get_fasta(file):
    with open(file) as f:
        chr=''
        ans={}
        s=''
        chr_order=[]
        for line in f:
            temp = line.strip()
            if temp[0]=='>':
                if chr!='':
                    ans[chr]=s
                    s=''
                chr= temp[1:]
                chr_order.append(chr)
                continue
            s+=temp
        ans[chr]=s
    return ans,chr_order

if __name__=="__main__":
    import time
    t = time.time()
    bases,chr=get_fasta('/data/yyin/data/ref/hg19/hg19.fa')
    for c in bases:
        print((len(bases[c])))
    print((time.time()-t))

'''
ll=len(s)
l.append(ll)
length+=ll
import random
#print(ans)
def getcg(read):
'''
