from pathlib import Path
import sys,math,mmap,csv,random,collections
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'verify'));import audit as a
v=a.v
files={};reaches={}
for p in ('QQR','QRR'):
 for suf,dct in [('dtm',files),('reach',reaches)]:
  f=open(P/f'K{p}vK_{suf}.bin','rb');dct[p]=(f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ))
def ptype(s):return ''.join(sorted(c for c in s[0].values() if c not in 'Kk'))
def index(s):
 b,t,e=s;k=next(i for i,x in b.items() if x=='K');bk=next(i for i,x in b.items() if x=='k');p=ptype(s);r='Q' if p=='QQR' else 'R';x=[i for i,c in b.items() if c==r];y=next(i for i,c in b.items() if c not in ('K','k',r));out=[]
 for mask in range(8):
  def tr(i):
   x,y=i%8,i//8;x=7-x if mask&1 else x;y=7-y if mask&2 else y
   if mask&4:x,y=y,x
   return x+8*y
  q=tr(bk);u,w=q%8,q//8
  if not(0<=u<=w<4):continue
  x0,x1=sorted(map(tr,x));idx=(x0+math.comb(x1,2))*64+tr(y);out.append(((w*(w+1)//2+u)*64+tr(k))*2016*64*2+idx*2+t)
 return min(out)
def dist(s):
 if len(s[0])<=4:return a.d0(s) if v.probe(s)[0]==1 else 254
 return files[ptype(s)][1][index(s)]
def rf(s):return reaches[ptype(s)][1][index(s)]
def ch(s):return [(m,a.state(t)) for m,t in a.ch(a.key(s)).items()]
rng=random.Random(938);checked=edges=0
for p in ('QQR','QRR'):
 for i in range(2000):
  while True:
   sq=rng.sample(range(64),5);s=(dict(zip(sq,['K','k']+list(p))),bool(rng.randrange(2)),None)
   try:v.valid(s);break
   except AssertionError:pass
  d=dist(s);assert d!=255;c=ch(s);edges+=len(c);ds=[dist(t) for m,t in c]
  if not c:want=0 if v.check(s[0],s[1]) else 254
  elif s[1]:want=254 if 254 in ds else 1+max(ds)
  else:want=1+min(ds) if min(ds)<254 else 254
  assert d==want,(v.fen(s),d,want)
  if d==254:assert not c and not v.check(s[0],s[1])
  checked+=1
 print('sample',p,'OK',checked,edges,flush=True)
@a.functools.lru_cache(maxsize=50000)
def lowerreach(k,material):
 s=a.state(k);d=dist(s)
 if v.material(s)==material:return True
 if d in (0,254):return False
 return any(lowerreach(a.key(t),material) for _,t in ch(s) if dist(t)==d-1)
rows=[]
for p in ('QQR','QRR'):
 targets=['KQvK','KRvK','KQRvK','K'+('QQ' if p=='QQR' else 'RR')+'vK']
 for line in open(P/f'K{p}vK_examples.tsv'):
  t,i,d,f=line.rstrip().split('\t');i=int(i);s=v.parse(f);m=targets[i];assert dist(s)==int(d);moves=[];ds=[int(d)];st=s
  while v.material(st)!=m:
   old=dist(st);cand=[]
   for u,c in ch(st):
    if dist(c)!=old-1:continue
    if v.material(c)==m or (len(c[0])==5 and rf(c)&(1<<i)) or (len(c[0])<5 and lowerreach(a.key(c),m)):cand.append((u,c))
   assert cand,(v.fen(st),m,old);u,st=cand[0];moves.append(u);ds.append(dist(st))
  rows.append(['K'+p+'vK',m,t,f,' '.join(moves),' '.join(map(str,ds)),v.fen(st)])
with open(P/'mixed_certificates.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['source','target','black_to_move','FEN','UCI_moves','DTM','target_FEN']);w.writerows(rows)
print('PASS',checked,edges,'witnesses',len(rows))
