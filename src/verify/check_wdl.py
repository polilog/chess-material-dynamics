"""Verify the final WDL proof dependency graph and published WDL witness tables."""
import csv,json,sys,collections
from pathlib import Path
import audit as a
v=a.v
known={};live=set();external={};nodes=0

def kf(f):return a.key(v.parse(f))
def put(k,z):
 for q,y in ((k,z),(a.key(v.mirror(a.state(k))),-z)):
  if q in known:assert known[q]==y,(v.fen(a.state(q)),known[q],y)
  known[q]=y
  if y:live.add(q)
def value(k):return v.probe(a.state(k))[0] if len(k[0])<=4 else known[k]
def terminal(k):
 assert not a.ch(k);return (1 if k[1] else -1) if v.check(dict(k[0]),k[1]) else 0
def islive(k):return not v.probe(a.state(k))[1] if len(k[0])<=4 else k in live

def mark_live(k,line):
 seq=[k]
 for u in line:k=a.ch(k)[u];seq.append(k)
 assert islive(k) or (not a.ch(k) and v.check(dict(k[0]),k[1])),v.fen(a.state(k))
 for p in seq:
  live.add(p);live.add(a.key(v.mirror(a.state(p))))

def prove(k,side,th,p):
 global nodes
 nodes+=1;v.valid(a.state(k));sgn=-1 if side else 1
 if isinstance(p,dict):
  if 'table' in p:assert len(k[0])<=4 and value(k)==p['table'] and value(k)*sgn>=th;return
  if 'terminal' in p:assert terminal(k)*sgn>=th;return
  if 'exists' in p:typ='exists';u,pp=p[typ];p=[typ,u,pp]
  else:p=['forall',list(p['forall'].items())]
 typ=p[0]
 if typ in ('table','known','leaf','external'):
  if typ=='table':assert len(k[0])<=4
  if typ=='external':assert k in external
  assert value(k)*sgn>=th;return
 if typ=='terminal':assert terminal(k)*sgn>=th;return
 ch=a.ch(k)
 if typ=='exists':assert k[1]==side;prove(ch[p[1]],side,th,p[2]);return
 assert typ=='forall' and k[1]!=side and ch and set(ch)=={u for u,_ in p[1]}
 for u,pp in p[1]:prove(ch[u],side,th,pp)

def step(s,t,u,z,p,line):
 assert len(s[0])==len(t[0])+1 and a.ch(s)[u]==t and value(t)==z
 if not z or s[1]!=(z==-1):assert p is not None;prove(s,(not s[1]) if not z else z==-1,int(z!=0),p)
 if not z:
  if line is None:assert islive(t);mark_live(s,[u])
  else:mark_live(s,line)
 put(s,z)

def main(root):
 global external
 ps=json.load(open(root/'proofs/wdl_proofs.json'));external={kf(r['FEN']):int(r['WDL']) for r in csv.DictReader(open(root/'proofs/external_wdl_anchors.csv'))}
 for r in ps['base']:
  k=kf(r['start_FEN']);z=r['WDL'];assert {p['side'] for p in r['bounds']}==({'w','b'} if z==0 else {'w' if z==1 else 'b'})
  for p in r['bounds']:assert p['threshold']==int(z!=0);prove(k,p['side']=='b',p['threshold'],p['tree'])
  mark_live(k,r['live_line']);put(k,z)
 print('WDL base',len(known),flush=True)
 for r in ps['reverse_lifts']:
  if 'base' in r:assert kf(r['FEN']) in known;continue
  if 'mirror' in r:
   k=kf(r['mirror']);assert k in known;put(k,value(k));continue
  s=kf(r['FEN']);t=kf(r['next']);step(s,t,r['move'],r['z'],r['proof'],r.get('live_line'))
 print('WDL reverse proofs',len(known),flush=True)
 for r in ps['five_targets']:
  t=kf(r['target_FEN']);z=r['WDL'];pp=r['target_proofs']
  if isinstance(pp,str):assert external[t]==z
  else:
   assert {x[0] for x in pp}==({False,True} if not z else {z==-1})
   for side,th,p in pp:assert th==int(z!=0);prove(t,side,th,p)
  put(t,z)
  for x in r['steps']:
   s=kf(x['FEN']);step(s,t,x['move'],z,x['proof'],x['live_line']);t=s
 print('WDL five proof closure',len(known),flush=True)
 for r in ps['seven_targets']:
  t=kf(r['anchor_FEN']);z=r['WDL']
  if r.get('anchor_terminal'):assert terminal(t)==z;put(t,z)
  else:assert value(t)==z
  for x in r['steps']:
   s=kf(x['FEN']);step(s,t,x['move'],z,x['proof'],x['live_line']);t=s
 print('WDL seven proof closure',len(known),'nodes',nodes,flush=True)
 def path(f,us,z,m,end,n):
  k=kf(f);assert len(k[0])==n and value(k)==z
  for u in us:assert islive(k) and a.ch(k);k=a.ch(k)[u];assert value(k)==z
  assert v.material(a.state(k))==m and (not end or v.fen(a.state(k))==end)
 for r in csv.DictReader(open(root/'results/wdl/reachability_from7.csv')):
  if r['start7']=='YES':path(r['start_FEN'],r['moves'].split(),int(r['WDL']),r['material'],r['target_FEN'],7)
 for r in csv.DictReader(open(root/'results/wdl/five_targets_best_witness.csv')):path(r['start_FEN'],r['UCI_moves'].split(),int(r['WDL']),r['material'],r['target_FEN'],int(r['height_lower']))
 for r in json.load(open(root/'results/wdl/small_targets_from8.json')):path(r['FEN'],r['moves'],r['z'],r['material'],'',8)
 print('PASS: WDL witness tables, external anchors:',len(external),flush=True)
if __name__=='__main__':main(Path(sys.argv[1]))
