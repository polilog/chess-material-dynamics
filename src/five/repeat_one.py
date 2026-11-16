# Exact DTD-3 correction for one-sided pawnless tables whose maximum DTD-0 is <=9.
# For d0=9, only a cycle of length 4 starting at the very same physical position can shorten it.
import sys,math,mmap,csv,collections,pathlib,itertools,numpy as np
R=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'verify'));import audit as a
v=a.v;name=sys.argv[1];p=name[1:-2];types=list(p);types.sort(key='QRBN'.index)
if types[0]==types[1]==types[2]:form=0;C=41664;triples=[None]*C
elif types[0]==types[1] or types[1]==types[2]:
 form=1;C=2016*64;triples=[None]*C
 if types[1]==types[2]:types[0],types[2]=types[2],types[0]
else:form=2;C=64**3;triples=[None]*C
if form==0:
 for x,y,z in itertools.combinations(range(64),3):triples[x+math.comb(y,2)+math.comb(z,3)]=(x,y,z)
elif form==1:
 for x,y in itertools.combinations(range(64),2):
  for z in range(64):triples[(x+math.comb(y,2))*64+z]=(x,y,z)
else:
 for x,y,z in itertools.product(range(64),repeat=3):triples[(x*64+y)*64+z]=(x,y,z)
cb=[8*y+x for y in range(4) for x in range(y+1)]
D=np.memmap(R/f'{name}_dtd0.bin',dtype='u1',mode='r');W=np.memmap(R/f'{name}_dtm.bin',dtype='u1',mode='r');M=np.memmap(R/f'{name}_reach.bin',dtype='u1',mode='r')
def rank(x):
 if form==0:x=sorted(x);return x[0]+math.comb(x[1],2)+math.comb(x[2],3)
 if form==1:i,j=sorted(x[:2]);return (i+math.comb(j,2))*64+x[2]
 return (x[0]*64+x[1])*64+x[2]
def tr(p,t):
 x,y=p%8,p//8
 if t&1:x=7-x
 if t&2:y=7-y
 if t&4:x,y=y,x
 return x+8*y
def index(s):
 b,t,e=s;k=next(i for i,x in b.items() if x=='K');bk=next(i for i,x in b.items() if x=='k');xs=[]
 for c in dict.fromkeys(types):xs += sorted(i for i,z in b.items() if z==c)
 if form==1 and types[0]!=types[2]:xs=sorted(i for i,z in b.items() if z==types[0])+[next(i for i,z in b.items() if z==types[2])]
 out=[]
 for r in range(8):
  q=tr(bk,r);x,y=q%8,q//8
  if x<=y<4:out.append(((y*(y+1)//2+x)*64+tr(k,r))*C*2+rank([tr(i,r) for i in xs])*2+t)
 return min(out)
def decode(idx):
 t=idx&1;idx>>=1;xs=triples[idx%C];idx//=C;k=idx%64;bk=cb[idx//64];return (dict(zip([k,bk,*xs],['K','k',*types])),bool(t),None)
def draw(k):
 s=a.state(k);return len(k[0])==5 and W[index(s)]==254 and D[index(s)]!=0
# a physical reversible four-ply cycle (not a symmetry-quotient cycle)
def cycle(k):
 for u,t in a.ch(k).items():
  if not draw(t):continue
  for w,r in a.ch(t).items():
   if not draw(r):continue
   uu=u[2:4]+u[:2];ww=w[2:4]+w[:2];q=a.ch(r).get(uu)
   if q is not None and draw(q) and a.ch(q).get(ww)==k:return [u,w,uu,ww]
 return None
valid=(W!=255)&(W==254);assert not np.any(D[valid]==254);maximum=int(D[valid].max());assert maximum<=9,(name,maximum)
# Lower pawnless one-sided DTD0 maxima are <=8 for all sub-materials checked here.
sub=set();from itertools import combinations
for n in range(3):
 for xx in combinations(types,n):sub.add('K'+''.join(sorted(xx,key='QRBN'.index))+'vK')
stat={}
for l in open(R.parent/'four/dist_stats.tsv'):
 m,z,c,inf,mi,ma=l.split('\t');
 if int(z)==0:stat[m]=(int(inf),int(ma))
assert all(stat[m][0]==0 and stat[m][1]<=8 for m in sub),[(m,stat[m]) for m in sub]
changes=[];ns=0
for idx in np.flatnonzero(D==9):
 s=decode(int(idx));k=a.key(s);assert index(s)==idx;ns+=1;c=cycle(k)
 if c:changes.append((int(idx),v.fen(s),' '.join(c+c),int(M[idx])))
with open(R/f'{name}_dtd3_changes.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['index','FEN','UCI_moves','old_reach_mask']);w.writerows(changes)
# d0<=8 states have identical shortest-material reachability. A changed d0=9 state has no material-changing shortest path of length 8.
rows=list(csv.DictReader(open(R/f'{name}_pairs.tsv'),delimiter='\t'));subids=sorted(sub,key=lambda m:len(m))
# Solver order within same n may differ; reconstruct from subset enumeration (not set iteration).
subids=[]
for mask in range(7):
 m='K'+''.join(sorted([types[i] for i in range(3) if mask>>i&1],key='QRBN'.index))+'vK'
 if m not in subids:subids.append(m)
subids.sort(key=len)
for r in rows:
 if r['WDL']=='0':
  j=subids.index(r['target']);t=int(r['turn']);r['count_DTD3']=int(r['count'])-sum(1 for idx,fen,moves,mask in changes if idx%2==t and mask>>j&1)
 else:r['count_DTD3']=r['count']
with open(R/f'{name}_pairs_DTD3.tsv','w',newline='') as f:
 w=csv.DictWriter(f,list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
print(name,'max DTD0',maximum,'d0=9',ns,'changed',len(changes),'max DTD3',8 if ns and ns==len(changes) else maximum,flush=True)
