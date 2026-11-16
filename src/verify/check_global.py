import sys,csv,collections,pathlib
R=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(R));import audit as a
v=a.v
# No trust in C++ search output. Draw lower bounds are stronger than required:
# rule out all earlier terminals even along non-WDL-preserving paths.
def bare(k,side):return not any(c!='K' and c!='k' and c.islower()==side for _,c in k[0])
def nonloss(k,side,depth):return bare(k,not side) or a.bound(k,side,depth,0)
def term(k):
 if a.ch(k):return None
 return (1 if k[1] else -1) if v.check(dict(k[0]),k[1]) else 0

def verify(r):
 m,z,f,u,tf,d,e,*tail=r;z,d,e=int(z),int(d),int(e);k=a.key(v.parse(f));v.valid(a.state(k));assert len(k[0])==6 and d==e+1
 ch=a.ch(k);assert u in ch;t=ch[u];assert len(t[0])==5 and v.fen(a.state(t))==tf and v.material(a.state(t))==m
 if z:
  side=z==-1;assert a.mate(t,side,e) and (e==0 or not a.mate(t,side,e-1))
  assert a.mate(k,side,d) and not a.mate(k,side,d-2)
 else:
  assert a.live(k,4)
  # Target must have a certified shortest drawing continuation.
  if e==0:assert term(t)==0 or len(t[0])<=4 and v.probe(a.state(t))[1]
  else:
   assert tail and len(tail[0].split())==e
   p=t
   for uu in tail[0].split():
    assert a.live(p,4) and all(nonloss(p,i,3) for i in (False,True));p=a.ch(p)[uu]
   assert term(p)==0 or len(p[0])<=4 and v.probe(a.state(p))[1]
   assert a.nodraw(t,e-1,0)
  # The chosen move proves nonloss for mover; other side must also not lose.
  assert len(ch)==1 or nonloss(k,not k[1],3)
  assert len(ch)==1 or d==1 or a.nodraw(k,d-1,0)
  assert d<=8 # repetitions cannot terminate before eight plies from a fresh state
 return [m,z,f,u,tf,d,e,tail[0].strip() if tail else '']

import functools
from audit_edges import cap

def verify_row(r):
 z=int(r['WDL']);d=int(r['distance_start']);e=int(r['distance_end']);f=r['start_FEN'];seq=r['UCI_moves'].split();k=a.key(v.parse(f));v.valid(a.state(k));ch=a.ch(k);t=ch[seq[0]];n=int(r['start_n']);assert len(k[0])==n and len(t[0])==n-1
 if n==6 and len(r['target'])-1==5:
  assert len(seq)==1 and d==e+1 and v.material(a.state(t))==r['target'] and v.fen(a.state(t))==r['target_FEN']
  if r['proof'].startswith('same_color_bishops_dead'):
   assert z==0 and e==0 and a.live(k,4) and a.bound(k,not k[1],4,0)
   assert all(c.upper() in 'KB' for _,c in t[0]);bishops=[q for q,c in t[0] if c.upper()=='B'];assert len(set((q%8+q//8)%2 for q in bishops))==1;return
  if r['proof'].startswith('two_forced_captures'):
   assert z==0 and len(ch)==1 and a.live(k,4) and a.live(t,4);cc=a.ch(t);assert len(cc)==1 and r['draw_tail']==next(iter(cc));p=next(iter(cc.values()));assert len(p[0])==4 and v.probe(a.state(p))[0]==0 and a.d0(a.state(p))==a.d3(a.state(p))==e-1;return
  verify([r['target'],z,f,seq[0],r['target_FEN'],d,e,r['draw_tail']]);return
 if n==6:
  for model in [0,3]:
   mat,ds,dd,end,reason,num=a.verify(v.fen(a.state(t)),seq[1],' '.join(seq[2:]),z,model);assert (mat,ds,dd,end)==(r['target'],d-1,e,r['target_FEN'])
  if z and len(ch)>1:
   side=z==-1;assert a.mate(k,side,d) and not a.mate(k,side,d-2)
  if not z and len(ch)>1:
   @functools.lru_cache(None)
   def nl(p,side,h):
    if p==t:return True
    if len(p[0])<=4:return v.probe(a.state(p))[0]*(-1 if side else 1)>=0
    cc=a.ch(p)
    if not cc:return (0 if not v.check(dict(p[0]),p[1]) else (-1 if p[1]==side else 1))>=0
    if not h:return False
    return (any if p[1]==side else all)(nl(c,side,h-1) for c in cc.values())
   assert nl(k,not k[1],3) and a.nodraw(k,d-1,0) and d<=8
  return
 assert n==5
 model=3 if r['model'].endswith('3') else 0;dt=a.d3 if model==3 else a.d0;p=a.state(t);assert v.probe(p)[0]==z and dt(p)==d-1
 if len(ch)==1:pass
 elif all(len(x[0])<=4 for x in ch.values()):assert cap(f,seq[0],z,model)==d
 elif z:
  side=z==-1;assert a.mate(k,side,d) and not a.mate(k,side,d-2)
 else:
  assert a.live(k,4) and (a.bound(k,not k[1],3,0) or a.bound(k,not k[1],4,0));assert d<=8 and (d==1 or a.nodraw(k,d-1,0))
 if not z:assert a.live(k,4)
 for u in seq[1:]:
  assert v.probe(p)==(z,False);dd=dt(p);p=v.play(p,u);assert v.probe(p)[0]==z and dt(p)==dd-1
 assert v.fen(p)==r['target_FEN'] and v.material(p)==r['target'] and dt(p)==e

if __name__=='__main__':
 rows=list(csv.DictReader(open(sys.argv[1])));counts=collections.Counter();errors=[]
 for r in rows:
  try:verify_row(r);counts[int(r['start_n']),len(r['target'])-1]+=1
  except (AssertionError,KeyError,ValueError) as exc:errors.append((r['start_n'],r['target'],r['WDL'],r['model'],str(exc)));print('FAIL',errors[-1],flush=True)
  if sum(counts.values())%100==0:print('checked',sum(counts.values()),flush=True)
 print('global certificates:',dict(counts),'failures:',len(errors),flush=True);assert not errors and len(rows)==1020
