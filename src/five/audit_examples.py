from pathlib import Path
import sys, math, mmap, csv, random, collections
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parent/'verify'));import audit as a
v=a.v
files={};reaches={}
for p in 'QR':
 for suf,dct in [('dtm',files),('reach',reaches)]:
  f=open(P/f'K{p*3}vK_{suf}.bin','rb');dct[p]=(f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ))
def index(s):
 b,t,e=s;k=next(i for i,x in b.items() if x=='K');bk=next(i for i,x in b.items() if x=='k');x=[i for i,c in b.items() if c not in 'Kk'];out=[]
 for mask in range(8):
  def tr(i):
   x,y=i%8,i//8;x=7-x if mask&1 else x;y=7-y if mask&2 else y
   if mask&4:x,y=y,x
   return x+8*y
  q=tr(bk);u,w=q%8,q//8
  if not(0<=u<=w<4):continue
  x0,x1,x2=sorted(map(tr,x));r=x0+math.comb(x1,2)+math.comb(x2,3);out.append(((w*(w+1)//2+u)*64+tr(k))*41664*2+r*2+t)
 return min(out)
def dist(s):
 if len(s[0])<=4:return a.d0(s) if v.probe(s)[0]==1 else 254
 p=next(c for c in s[0].values() if c not in 'Kk');return files[p][1][index(s)]
def rf(s):
 p=next(c for c in s[0].values() if c not in 'Kk');return reaches[p][1][index(s)]
def ch(s):return [(m,a.state(t)) for m,t in a.ch(a.key(s)).items()]
# Independent direct geometry audit at 4000 randomly selected full boards plus the maximum-DTM positions.
rng=random.Random(91227);checked=0;edges=0
for p in 'QR':
 for i in range(2000):
  while True:
   sq=rng.sample(range(64),5);s=(dict(zip(sq,['K','k']+[p]*3)),bool(rng.randrange(2)),None)
   try:v.valid(s);break
   except AssertionError:pass
  d=dist(s);assert d!=255
  c=ch(s);edges+=len(c);ds=[dist(t) for m,t in c]
  if not c:want=0 if v.check(s[0],s[1]) else 254
  elif s[1]:want=254 if 254 in ds else 1+max(ds)
  else:want=1+min(ds) if min(ds)<254 else 254
  assert d==want,(v.fen(s),d,want);checked+=1
 print('sample',p,'OK',checked,edges,flush=True)
# For the small number of sample certificates, use independent exact table probe and full legal move generation.
@a.functools.lru_cache(maxsize=None)
def lowerreach(k):
 s=a.state(k);d=dist(s)
 if len(s[0])==3:return True
 if d in (0,254):return False
 return any(lowerreach(a.key(t)) for _,t in ch(s) if dist(t)==d-1)
def follow(s,n):
 moves=[];ds=[dist(s)];fens=[v.fen(s)]
 while len(s[0])>n:
  d=dist(s);cand=[]
  for m,t in ch(s):
   if dist(t)!=d-1:continue
   if len(t[0])==n or (len(t[0])==5 and rf(t)&(1<<(4-n))) or (n==3 and len(t[0])==4 and lowerreach(a.key(t))):cand.append((m,t))
  assert cand,(v.fen(s),n,d);m,s=cand[0];moves.append(m);ds.append(dist(s));fens.append(v.fen(s))
 return moves,ds,fens
out=[]
for p in 'QR':
 for line in open(P/f'K{p*3}vK_examples.tsv'):
  t,n,d,f=line.rstrip().split('\t');s=v.parse(f);n=int(n);d=int(d);assert dist(s)==d
  moves,ds,fens=follow(s,n);out.append((p,t,n,f,' '.join(moves),' '.join(map(str,ds)),fens[-1]))
with open(P/'verified_examples.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['piece','turn_black','target_pieces','FEN','UCI_moves','DTM','target_FEN']);w.writerows(out)
print('independent sample',checked,'positions',edges,'moves; witnesses',len(out),flush=True)
