import csv,collections
from pathlib import Path
import audit as a
v=a.v;R=Path(__file__).resolve().parent

def cap(f,u,z,model):
 s=v.parse(f);k=a.key(s);c=a.ch(k);assert u in c;t=a.state(c[u]);assert len(s[0])==5 and len(t[0])==4 and v.probe(t)[0]==z;d=(a.d3 if model==3 else a.d0);dt=d(t)
 if all(len(x[0])<=4 for x in c.values()):
  vals=[v.probe(a.state(x))[0] for x in c.values()];assert (min if s[1] else max)(vals)==z
  opt=(max if z and s[1]!=(z==-1) else min)(d(a.state(x)) for x in c.values() if v.probe(a.state(x))[0]==z)
  assert dt==opt and (z!=0 or a.live(k,4));return dt+1
 return a.verify(f,u,'',z,model)[1]
def promo(f,u,z,tf,tail,model):
 s=v.parse(f);t=v.parse(tf);k=a.key(s);c=a.ch(k);assert u in c and a.state(c[u])==t and len(t[0])==5 and len(u)==5 and len(s[0])==5
 if tail:d=cap(tf,tail,z,model)
 else:
  assert not a.ch(a.key(t));assert (0 if not v.check(t[0],t[1]) else (1 if t[1] else -1))==z;d=0
 if z:
  side=z==-1
  if s[1]==side:assert not a.mate(k,side,d-1)
  else:assert len(c)==1 or a.mate(k,side,d+1)
 else:
  assert a.live(k,4) and (len(c)==1 or a.bound(k,not s[1],3,0));assert len(c)==1 or d==0 or (d+1<=8 and a.nodraw(k,d,model))
 return d+1
