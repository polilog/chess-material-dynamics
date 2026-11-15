"""Check final positive five-piece edges/pairs using exact or finite certificates.
Requires the final global certificates to have passed check_global.py and exact 4/selected 5 tables.
"""
import csv,sys,collections,math,mmap,functools
from pathlib import Path
import audit as a
from audit_edges import cap,promo
v=a.v;R=Path(sys.argv[1]);F=Path(__file__).resolve().parent.parent/'five'
def rows(f):return list(csv.DictReader(open(R/'results'/f)))
# Values from already certified global paths and their complete draw tails.
K={}
def add(s,z,d,model):
 k=a.key(s);kk=(k,model)
 if kk in K:assert K[kk]==(z,d),(v.fen(s),K[kk],z,d)
 K[kk]=(z,d)
for r in rows('global/strict_witnesses.csv'):
 z=int(r['WDL']);s=v.parse(r['start_FEN']);d=int(r['distance_start']);models=(0,3) if r['model']=='DTM+DTD0+DTD3' else (3,) if r['model'].endswith('3') else (0,)
 for u in (r['UCI_moves']+' '+r['draw_tail']).split():
  if len(s[0])==5:
   for model in models:add(s,z,d,model)
  s=v.play(s,u);d-=1
 if len(s[0])==5:
  for model in models:add(s,z,d,model)
exact={'QQQ','QQR','QRR','RRR','BBB','BBN','BNN','NNN'};files={}
def tr(p,i):
 x,y=p%8,p//8
 if i&1:x=7-x
 if i&2:y=7-y
 if i&4:x,y=y,x
 return x+8*y
def probe5(s):
 b,t,e=s;mm=v.material(s);w,bl=mm.split('v');sgn=1
 if w=='K':s=v.mirror(s);b,t,e=s;w,bl=bl,w;sgn=-1
 p=w[1:];assert bl=='K' and p in exact
 k=next(i for i,c in b.items() if c=='K');bk=next(i for i,c in b.items() if c=='k');typ=list(p);same=len(set(typ))==1
 if not same and typ[0]!=typ[1]:typ=[typ[1],typ[2],typ[0]]
 x=[i for i,c in b.items() if c==typ[0]];y=next((i for i,c in b.items() if c==typ[-1]),None)
 C=41664 if same else 2016*64;ii=[]
 for i in range(8):
  q=tr(bk,i);u,h=q%8,q//8
  if not u<=h<4:continue
  qx=sorted(tr(sq,i) for sq in x)
  rank=qx[0]+math.comb(qx[1],2)+(math.comb(qx[2],3) if same else 0)
  if not same:rank=rank*64+tr(y,i)
  ii.append(((h*(h+1)//2+u)*64+tr(k,i))*C*2+rank*2+t)
 i=min(ii);m='K'+p+'vK';f=F/(m+'_dtm.bin')
 if m not in files:
  f1=open(f,'rb');mm1=mmap.mmap(f1.fileno(),0,access=mmap.ACCESS_READ);f2=F/(m+'_dtd0.bin');files[m]=(f1,mm1,open(f2,'rb') if f2.exists() else None)
  if files[m][2]:files[m]=(*files[m],mmap.mmap(files[m][2].fileno(),0,access=mmap.ACCESS_READ))
 d=files[m][1][i];assert d!=255
 if d==254:return (0,files[m][3][i] if len(files[m])==4 else 0)
 return sgn,d

def oracle(s,model):
 if len(s[0])<=4:return v.probe(s)[0],(a.d3 if model==3 else a.d0)(s)
 k=(a.key(s),model)
 if k in K:return K[k]
 w,b=v.material(s).split('v');p=w[1:] if b=='K' else b[1:] if w=='K' else ''
 if p in exact:return probe5(s)
 return None

def verify(f,seq,z,target,model,start_distance=None,tail=''):
 s=v.parse(f);k=a.key(s);u=seq[0];t=a.state(a.ch(k)[u]);d=None
 o=oracle(s,model)
 if o is not None:assert o[0]==z;d=o[1]
 elif len(t[0])==4:d=cap(f,u,z,model)
 elif len(seq)==1 and (tail or not a.ch(a.key(t))):d=promo(f,u,z,v.fen(t),tail,model)
 elif z and start_distance is not None:
  d=start_distance;assert a.mate(k,z==-1,d) and not a.mate(k,z==-1,d-2)
 elif len(seq)>=2:
  # Two promotions are supported by a certified last promotion and its suffix.
  uu=seq[1];p=v.play(t,uu)
  if len(p[0])==4:dd=cap(v.fen(t),uu,z,model)
  else:dd=promo(v.fen(t),uu,z,v.fen(p),tail,model)
  d=dd+1
  if z:assert a.mate(k,z==-1,d) and not a.mate(k,z==-1,d-2)
  else:assert a.live(k,4) and a.bound(k,not k[1],3,0) and d<=8 and a.nodraw(k,d-1,model)
  add(t,z,dd,model)
 else:raise AssertionError(('no proof',f,seq,z))
 if start_distance is not None:assert d==start_distance,(d,start_distance)
 start=d;p=s
 for j,u in enumerate(seq):
  k=a.key(p);assert d>0 and u in a.ch(k);t=a.state(a.ch(k)[u]);q=oracle(t,model)
  if q is None:
   if z and d<=10:assert a.mate(a.key(t),z==-1,d-1) and (d==1 or not a.mate(a.key(t),z==-1,d-2))
   elif j==len(seq)-1 and tail:assert cap(v.fen(t),tail,z,model)==d-1
   elif j==len(seq)-1 and not a.ch(a.key(t)):assert z==0 and d==1 and not v.check(t[0],t[1])
   else:raise AssertionError(('no child proof',v.fen(t),d,z,seq))
  else:assert q==(z,d-1),(q,z,d-1,v.fen(t))
  add(t,z,d-1,model) if len(t[0])==5 else None
  p=t;d-=1
 assert v.fen(p)==target
 return start
counts=collections.Counter()
for f,st,us in [('five/edges.csv','status_both_models','UCI'),('five/pairs_same_layer.csv','status','moves'),('five/pairs_to_lower.csv','status','UCI_moves')]:
 for r in rows(f):
  if r[st]!='YES':continue
  d=int(r['distance_start']) if r.get('distance_start') else None;seq=r[us].split();tail=r.get('target_capture','');z=int(r['WDL'])
  try:
   for model in (0,3):verify(r['FEN'],seq,z,r['target_FEN'],model,d,tail)
  except AssertionError as ex:print('FAIL',f,r,ex,flush=True);raise
  counts[f]+=1
 print('PASS',f,counts[f],flush=True)
