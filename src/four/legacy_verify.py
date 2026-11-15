import csv, json, mmap, re
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ORDER='KQRBNP'
flip=lambda m:'v'.join(m.split('v')[::-1])
def parse(f):
 a,turn,_,ep,*_=f.split(); b={}
 for y,row in enumerate(a.split('/')[::-1]):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:b[y*8+x]=c;x+=1
  assert x==8
 return b,turn=='b',None if ep=='-' else sq(ep)
def sq(s):return ord(s[0])-97+8*(int(s[1])-1)
def alg(s):return chr(97+s%8)+str(1+s//8)
def mirror(s):
 b,t,e=s;return {p^56:c.swapcase() for p,c in b.items()},not t,None if e is None else e^56
def fen(s):
 b,t,e=s;rows=[]
 for y in range(7,-1,-1):
  r='';n=0
  for x in range(8):
   c=b.get(y*8+x)
   if not c:n+=1
   else:r+=(str(n) if n else '')+c;n=0
  rows.append(r+(str(n) if n else ''))
 return '/'.join(rows)+(' b - ' if t else ' w - ')+(alg(e) if e is not None else '-')+' 0 1'
def material(s):
 b=s[0];return 'v'.join(''.join(sorted((c.upper() for c in b.values() if c.islower()==col),key=ORDER.index)) for col in (False,True))
def attacks(b,p,q,c):
 if p==q:return False
 x=q%8-p%8;y=q//8-p//8;a=c.upper()
 if a=='K':return max(abs(x),abs(y))==1
 if a=='N':return abs(x*y)==2
 if a=='P':return abs(x)==1 and y==(-1 if c.islower() else 1)
 diag=abs(x)==abs(y);straight=x==0 or y==0
 if not {'Q':diag or straight,'R':straight,'B':diag}[a]:return False
 step=(x>0)-(x<0)+8*((y>0)-(y<0));r=p+step
 while r!=q:
  if r in b:return False
  r+=step
 return True
def check(b,t):
 k=next(p for p,c in b.items() if c==('k' if t else 'K'))
 return any(c.islower()!=t and attacks(b,p,k,c) for p,c in b.items())
def valid(s):
 b,t,e=s;assert sum(c=='K' for c in b.values())==sum(c=='k' for c in b.values())==1
 assert all(c.upper()!='P' or 8<=p<56 for p,c in b.items());assert not check(b,not t)
def play(s,u):
 b,t,e=s;valid(s);p,q=sq(u[:2]),sq(u[2:4]);c=b[p];a=c.upper();assert c.islower()==t and p!=q
 assert q not in b or (b[q].islower()!=t and b[q].upper()!='K')
 x=q%8-p%8;y=q//8-p//8;nb=b.copy();del nb[p];ne=None
 if a=='P':
  d=-1 if t else 1
  if x==0:
   assert q not in b and (y==d or (y==2*d and p//8==(6 if t else 1) and p+8*d not in b))
   if y==2*d and any(0<=q%8+i<8 and b.get(q+i)==('P' if t else 'p') for i in (-1,1)):ne=p+8*d
  else:
   assert abs(x)==1 and y==d and (q in b or e==q)
   if q not in b:assert nb.pop(q-8*d)==('P' if t else 'p')
  if q//8 in (0,7):assert len(u)==5 and u[4] in 'qrbn';c=u[4] if t else u[4].upper()
  else:assert len(u)==4
 else:assert len(u)==4 and attacks(b,p,q,c)
 nb[q]=c;assert not check(nb,t);return nb,not t,ne
FILES={}
def probe(s):
 b,t,e=s;valid(s);w,bl=material(s).split('v');sw=len(w)<len(bl) or (len(w)==len(bl)==2 and ORDER.index(w[1])>ORDER.index(bl[1]));
 if sw:b,t,e=mirror(s);w,bl=bl,w
 m=w+'v'+bl;pp=[next(p for p,c in b.items() if c=='K'),next(p for p,c in b.items() if c=='k')]
 for col in (False,True):pp.extend(sorted((p for p,c in b.items() if c.upper()!='K' and c.islower()==col),key=lambda p:(ORDER.index(b[p].upper()),p)))
 h=pp[0]%8>=4;v='P' not in m and pp[0]//8>=4;pp=[p^(7 if h else 0)^(56 if v else 0) for p in pp]
 ix=pp[0]//8*4+pp[0]%8
 for p in pp[1:]:ix=ix*64+p
 ix=ix*2+int(t)
 if m=='KPvKP':ix=ix*2+int(e is not None)
 if m not in FILES:
  f=open(ROOT/('tb_'+m+'.bin'),'rb');FILES[m]=(f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ))
 z=FILES[m][1][ix];z=z if z<128 else z-256;assert z in (-1,0,1,2),(s,m,ix,z)
 return (0 if z==2 else z*(-1 if sw else 1)),z==2

def decode(s):
 sw,f,u=s.split(':');st=parse(f)
 if sw=='1':st=mirror(st);u=alg(sq(u[:2])^56)+alg(sq(u[2:4])^56)+u[4:]
 return st,u

def verify_path(k,steps):
 z,*ms=k.split('/');z=int(z);actual=[];moves=[];prev=None;initial=None
 for x in steps:
  s,u=decode(x)
  if initial is None:initial=s
  if prev is not None:assert s==prev,(k,fen(s),fen(prev))
  v,dead=probe(s);assert v==z and not dead,(k,fen(s),v,dead)
  m=material(s)
  if not actual or actual[-1]!=m:actual.append(m)
  prev=play(s,u);assert probe(prev)[0]==z,(k,u,fen(prev));moves.append(u)
 m=material(prev)
 if not actual or actual[-1]!=m:actual.append(m)
 assert actual==ms,(k,actual);return fen(initial),' '.join(moves),fen(prev)

def run():
 vertices={};edges={};paths={}
 for line in open(ROOT/'results.tsv'):
  a=line.rstrip().split('\t');typ,m=a[:2]
  if typ=='V':
   z=int(a[2]);s=parse(a[3]);assert probe(s)[0]==z and material(s)==m
   vertices[m,z]=fen(s);vertices[flip(m),-z]=fen(mirror(s))
  else:
   n,z=a[2],int(a[3]);s=parse(a[4]);u=a[5];assert material(s)==m and probe(s)==(z,False);t=play(s,u);assert material(t)==n and probe(t)[0]==z
   edges[m,n,z]=(fen(s),u,fen(t));s2=mirror(s);u2=alg(sq(u[:2])^56)+alg(sq(u[2:4])^56)+u[4:];edges[flip(m),flip(n),-z]=(fen(s2),u2,fen(mirror(t)))
 # Exact paths.tsv can be generated from scratch. The fast run uses three intermediate files.
 names=['paths.tsv']
 for name in names:
  for line in open(ROOT/name):
   k,st,*steps=line.rstrip().split('\t')
   if st=='UNKNOWN':continue
   z,*p=k.split('/');z=int(z);key=(z,tuple(p));key2=(-z,tuple(map(flip,p)))
   if st=='YES':
    f,u,last=verify_path(k,steps);s=parse(f);s2=mirror(s);u2=' '.join(alg(sq(x[:2])^56)+alg(sq(x[2:4])^56)+x[4:] for x in u.split());data=(st,f,u,last);data2=(st,fen(s2),u2,fen(mirror(parse(last))))
   else:data=data2=(st,'','','')
   for kk,dd in [(key,data),(key2,data2)]:
    if kk in paths:assert paths[kk][0]==st
    paths[kk]=dd
 adj=defaultdict(set)
 for m,n,z in edges:adj[m,z].add(n)
 expected=set()
 def go(z,p):
  if len(p)>1:expected.add((z,p))
  for n in adj[p[-1],z]:go(z,p+(n,))
 for m,z in vertices:go(z,(m,))
 assert set(paths)==expected,(len(paths),len(expected))
 H={k:len(k[0])-1 for k in vertices};hc={k:('','') for k in vertices}
 for (z,p),(st,f,u,last) in paths.items():
  if st=='YES' and len(p[0])-1>H[p[-1],z]:H[p[-1],z]=len(p[0])-1;hc[p[-1],z]=(f,u)
 assert all(v==4 for v in H.values())
 def write(name,header,rows):
  with open(ROOT/name,'w',newline='') as f:w=csv.writer(f);w.writerow(header);w.writerows(rows)
 write('vertices.csv',['material','WDL','FEN'],[(m,z,f) for (m,z),f in sorted(vertices.items())]);write('edges.csv',['source','target','WDL','FEN','UCI','target_FEN'],[(m,n,z,*d) for (m,n,z),d in sorted(edges.items())]);write('material_paths.csv',['WDL','material_path','status','FEN','UCI_moves','final_FEN'],[(z,' -> '.join(p),*d) for (z,p),d in sorted(paths.items())]);write('heights.csv',['material','WDL','height_le4','start_FEN','UCI_moves'],[(m,z,h,*(hc[m,z] if hc[m,z][0] else (vertices[m,z],''))) for (m,z),h in sorted(H.items())]);
 print('Verified',len(vertices),'vertices',len(edges),'edges',len(paths),'paths',Counter(d[0] for d in paths.values()),'heights',Counter(H.values()))
if __name__=='__main__':run()
