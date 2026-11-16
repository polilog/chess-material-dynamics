#!/usr/bin/env python3
"""Check the released schema, candidate universe and conservative negative closures."""
import csv, collections as C, itertools as I, functools as F, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/four'));import legacy_verify as v
R=ROOT/'results'
def read(f):return list(csv.DictReader(open(R/f)))
def key(r):return r['source'],r['target'],int(r['WDL'])
def n(m):return len(m)-1
def mat(s):return 'v'.join(''.join(sorted(x,key='KQRBNP'.index)) for x in s)
def transitions(m):
 a=m.split('v');out=set()
 for side in (0,1):
  for x in set(a[side][1:]):
   t=[list(q) for q in a];t[side].remove(x);out.add((mat(t),'capture'))
  if 'P' in a[side]:
   for x in 'QRBN':
    t=[list(q) for q in a];t[side].remove('P');t[side].append(x);out.add((mat(t),'promotion'))
    for y in set(a[1-side][1:]):
     u=[q[:] for q in t];u[1-side].remove(y);out.add((mat(u),'capture_promotion'))
 return out
V4={(r['material'],int(r['WDL'])) for r in read('four/vertices.csv')};V5={(r['material'],int(r['WDL'])) for r in read('five/classification.csv') if r['status']=='YES'}
V6={(r['material'],int(r['WDL'])) for r in read('wdl/six_classification.csv') if r['WDL_exists']=='YES'}
assert (len(V4),len(V5),len(V6))==(146,582,1995)
E=read('five/edges.csv');assert len(E)==3412 and len({key(r) for r in E})==3412
expected={(m,t,z,ty) for m,z in V5 for t,ty in transitions(m) if (t,z) in V4|V5}
assert expected=={(*key(r),r['type']) for r in E}
assert C.Counter(r['status_both_models'] for r in E)=={'YES':1784,'NO':192,'UNKNOWN':1436}
A=C.defaultdict(set)
for r in E:
 m,t,z=key(r)
 if r['status_both_models']!='NO':A[m,z].add(t)
# exact small-layer reachability, and turn-specific bounds.
B={(m,z,t):{m} for m,z in V4 for t in (0,1)}
for r in read('four/turn_pairs.csv'):
 m,t,z=key(r)
 for c,col in ((0,'white_to_move_yes'),(1,'black_to_move_yes')):
  if r[col]=='1':B[m,z,c].add(t)
X=C.defaultdict(set);exact=set()
for r in read('five/exact/turn_pairs.csv'):
 m,t,z=key(r);c=int(r['black_to_move']);exact|={m,v.flip(m)}
 for k,y in [((m,z,c),t),((v.flip(m),-z,1-c),v.flip(t))]:
  if int(r['count_DTM_or_DTD0']) or int(r['count_DTM_or_DTD3']):X[k].add(y)
@F.lru_cache(None)
def same(m,z):
 out=set()
 for t in A[m,z]:
  if n(t)==5:out.add(t);out|=same(t,z)
 return out

def formal(N):
 return {(mat([['K',*w],['K',*b]]),z) for i in range(N-1) for w in I.combinations_with_replacement('QRBNP',i) for b in I.combinations_with_replacement('QRBNP',N-2-i) for z in (-1,0,1) if (z!=1 or w) and (z!=-1 or b)}
V=V4|V5|V6|formal(7)|formal(8)
# first-capture boundaries. Exact turn constraints are only used at the instant of capture.
@F.lru_cache(None)
def upper(m,z):
 N=n(m)
 if N<=4:return B[m,z,0]|B[m,z,1]
 if m in exact:return X[m,z,0]|X[m,z,1]
 out=set();edges=A[m,z] if N==5 else {x for x,ty in transitions(m) if (x,z) in V}
 for t in edges:
  if n(t)==4 or (n(t)==5 and n(t)<N and t in exact):
   a=m.split('v');b=t.split('v');c=next(i for i in (0,1) if len(a[i])>len(b[i]))
   out|=(B[t,z,c] if n(t)==4 else X[t,z,c])
  else:out|=upper(t,z)
 return out
p=read('five/pairs_to_lower.csv');assert len(p)==29000 and C.Counter(r['status'] for r in p)=={'YES':1981,'NO':24034,'UNKNOWN':2985}
for r in p:
 m,t,z=key(r)
 if r['status']=='NO':assert t not in upper(m,z),r
 if r['status']=='YES':assert t in upper(m,z),r
p=read('five/pairs_same_layer.csv');assert len(p)==113340 and C.Counter(r['status'] for r in p)=={'YES':316,'NO':110884,'UNKNOWN':2140}
for r in p:
 m,t,z=key(r)
 if r['status']=='NO':assert t not in same(m,z),r
 if r['status']=='YES':assert t in same(m,z),r
for r in read('propagation/certified_pairs.csv'):
 m,t,z=key(r);assert t not in upper(m,z),r
print('PASS: all five-piece candidate keys, 134,918 negative pair rows, 1,002 propagated exclusions',flush=True)
# Legal replay, no tablebase required. The strict/WDL distance proofs are checked separately.
def replay(f,us,tar,tf,src=None):
 s=v.parse(f);v.valid(s)
 if src:assert v.material(s)==src
 for u in us.split():s=v.play(s,u)
 assert v.material(s)==tar and (not tf or v.fen(s)==tf)
 return s
for r in read('four/paths.csv'):
 for name,status in [('wdl','wdl_status'),('dtd0','strict_status'),('dtd3','strict_status')]:
  if r[status]=='YES':
   ms=r['material_path'].split(' -> ');replay(r[name+'_FEN'],r[name+'_UCI_moves'],ms[-1],r[name+'_final_FEN'],ms[0])
for f,st,us in [('five/edges.csv','status_both_models','UCI'),('five/pairs_to_lower.csv','status','UCI_moves'),('five/pairs_same_layer.csv','status','moves')]:
 for r in read(f):
  if r[st]=='YES':replay(r['FEN'],r[us],r['target'],r['target_FEN'],r['source'])
for r in read('global/strict_witnesses.csv'):replay(r['start_FEN'],r['UCI_moves'],r['target'],r['target_FEN'])
print('PASS: all released strict positive FEN/UCI paths replay legally')
