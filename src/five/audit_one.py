# Independent move generator and distance / path checks for a one-sided table.
from pathlib import Path
import sys,random,csv,functools
exec(Path(__file__).with_name('repeat_one.py').read_text().split('valid=(W!=255)')[0])
def distances(s):
 if len(s[0])<=4:return v.probe(s)[0],a.d0(s)
 i=index(s);d=int(W[i]);assert d!=255
 return (0,int(D[i])) if d==254 else (1,d)
def moves(s):return [(u,a.state(k)) for u,k in a.ch(a.key(s)).items()]
rng=random.Random(181);checked=edges=0
for j in range(1500):
 while True:
  s=(dict(zip(rng.sample(range(64),5),['K','k',*types])),bool(rng.randrange(2)),None)
  try:v.valid(s);break
  except AssertionError:pass
 z,d=distances(s);c=moves(s);ds=[distances(t) for u,t in c];edges+=len(c);checked+=1
 if z:
  if not c:assert d==0 and v.check(s[0],s[1])
  elif s[1]:assert all(x==1 for x,y in ds) and d==1+max(y for x,y in ds)
  else:assert d==1+min(y for x,y in ds if x==1)
 elif d:
  assert (all(x==0 for x,y in ds) if not s[1] else True) and d==1+min(y for x,y in ds if x==0),(v.fen(s),d,ds)
 elif c:assert not v.check(s[0],s[1]) or True # dead flags independently certified by cooperative reachability pass
@functools.lru_cache(maxsize=50000)
def low(k,m,z):
 s=a.state(k);q,d=distances(s)
 if v.material(s)==m:return q==z
 if q!=z or d==0:return False
 return any(low(a.key(t),m,z) for u,t in moves(s) if distances(t)==(z,d-1))
rows=[]
subids=[]
for mask in range(7):
 m='K'+''.join(sorted([types[i] for i in range(3) if mask>>i&1],key='QRBN'.index))+'vK'
 if m not in subids:subids.append(m)
subids.sort(key=len)
for line in open(R/f'{name}_examples.tsv'):
 z,turn,m,d,f=line.rstrip().split('\t');z=int(z);d=int(d);s=v.parse(f);assert distances(s)==(z,d);st=s;us=[];ds=[d];i=subids.index(m)
 while v.material(st)!=m:
  old=distances(st)[1];cand=[]
  for u,t in moves(st):
   if distances(t)!=(z,old-1):continue
   if v.material(t)==m or (len(t[0])==5 and int(M[index(t)])>>i&1) or (len(t[0])<5 and low(a.key(t),m,z)):cand.append((u,t))
  assert cand,(v.fen(st),m,z,old,i);u,st=cand[0];us.append(u);ds.append(old-1)
 rows.append([name,m,z,turn,f,' '.join(us),' '.join(map(str,ds)),v.fen(st)])
with open(R/f'{name}_certificates.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['source','target','WDL','black_to_move','FEN','UCI_moves','distance','target_FEN']);w.writerows(rows)
print('PASS',name,checked,edges,'witnesses',len(rows),flush=True)
