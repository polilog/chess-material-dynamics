import csv, sys, collections, functools, json
from pathlib import Path
R=Path(__file__).resolve().parent; S=R.parent/'four';sys.path.insert(0,str(S));import legacy_verify as v
# Load only the distance readers; avoid running the old exporters.
for fname,name in [('export_strict.py','d0'),('export_repeat.py','d3')]:
 ns={'__file__':str(S/fname)};exec((S/fname).read_text().split('def check(')[0],ns);globals()[name]=ns['distance']
def key(s):return tuple(sorted(s[0].items())),s[1],s[2]
def state(k):return dict(k[0]),k[1],k[2]
@functools.lru_cache(maxsize=50000)
def ch(k):
 s=state(k);b,t,e=s;out={}
 for p,c in b.items():
  if c.islower()!=t:continue
  for q in range(64):
   if p==q:continue
   for pr in ('qrbn' if c.upper()=='P' and q//8 in (0,7) else ['']):
    u=v.alg(p)+v.alg(q)+pr
    try:out[u]=key(v.play(s,u))
    except AssertionError:continue
 return out
@functools.lru_cache(maxsize=50000)
def live(k,h):
 if len(k[0])<=4:return not v.probe(state(k))[1] and (bool(ch(k)) or v.check(dict(k[0]),k[1]))
 c=ch(k)
 if not c:return v.check(dict(k[0]),k[1])
 return h>0 and any(live(t,h-1) for t in c.values())
@functools.lru_cache(maxsize=50000)
def bound(k,side,h,threshold):
 if len(k[0])<=4:return v.probe(state(k))[0]*(-1 if side else 1)>=threshold
 c=ch(k)
 if not c:return ((-1 if k[1]==side else 1) if v.check(dict(k[0]),k[1]) else 0)>=threshold
 if not h:return False
 return (any if k[1]==side else all)(bound(t,side,h-1,threshold) for t in c.values())
@functools.lru_cache(maxsize=50000)
def mate(k,side,h):
 if len(k[0])<=4:return v.probe(state(k))[0]==(-1 if side else 1) and d0(state(k))<=h
 c=ch(k)
 if not c:return v.check(dict(k[0]),k[1]) and k[1]!=side
 if h<=0:return False
 return (any if k[1]==side else all)(mate(t,side,h-1) for t in c.values())
@functools.lru_cache(maxsize=50000)
def nodraw(k,h,model):
 if h<0:return True
 if len(k[0])<=4:return v.probe(state(k))[0]!=0 or (d3 if model==3 else d0)(state(k))>h
 c=ch(k)
 if not c:return v.check(dict(k[0]),k[1])
 if not live(k,4):return False
 return h==0 or all(nodraw(t,h-1,model) for t in c.values())
def verify(f,u,tail,z,model):
 distance=d3 if model==3 else d0;s=v.parse(f);k=key(s);c=ch(k);assert len(s[0])==5 and u in c;t=state(c[u]);assert len(t[0])==4 and v.probe(t)[0]==z;d=distance(t);assert d<65535
 if z:
  side=z==-1
  if k[1]==side:
   assert not mate(k,side,d-1);reason='mate_minimum'
  else:
   assert len(c)==1 or mate(k,side,d+1);reason='mate_maximum'
 else:
  assert live(k,4) and (len(c)==1 or bound(k,not k[1],3,0));assert len(c)==1 or (d==0 or (d+1<=8 and nodraw(k,d,model)));reason='forced_draw' if len(c)==1 else 'terminal_draw' if d==0 else 'shortest_draw'
 p=t;dd=d
 for a in tail.split():
  assert v.probe(p)==(z,False);p=v.play(p,a);assert v.probe(p)[0]==z and distance(p)==dd-1;dd-=1
 return v.material(p),d+1,dd,v.fen(p),reason,len(c)
def flipmoves(moves):return ' '.join(v.alg(v.sq(u[:2])^56)+v.alg(v.sq(u[2:4])^56)+u[4:] for u in moves.split())
