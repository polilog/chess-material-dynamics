"""Recheck all positive four-piece paths, exact values, and distance gradients."""
import csv,sys,collections
from pathlib import Path
import audit as a
v=a.v
root=Path(sys.argv[1]);count=collections.Counter()
for r in csv.DictReader(open(root/'results/four/paths.csv')):
 z=int(r['WDL']);mat=r['material_path'].split(' -> ')
 for mode,dt,status in [('wdl',None,'wdl_status'),('dtd0',a.d0,'strict_status'),('dtd3',a.d3,'strict_status')]:
  if r[status]!='YES':continue
  s=v.parse(r[mode+'_FEN']);assert v.probe(s)[0]==z;ms=[v.material(s)]
  if dt:assert dt(s)==int(r[mode+'_initial_distance'])
  for u in r[mode+'_UCI_moves'].split():
   assert v.probe(s)==(z,False) and a.ch(a.key(s));t=v.play(s,u);assert v.probe(t)[0]==z
   if dt:assert dt(t)==dt(s)-1
   s=t;m=v.material(s)
   if m!=ms[-1]:ms.append(m)
  assert ms==mat and v.fen(s)==r[mode+'_final_FEN']
  if dt:assert dt(s)==int(r[mode+'_final_distance'])
  count[mode]+=1
assert count=={'wdl':1280,'dtd0':940,'dtd3':940};print('PASS: four-piece witness paths',dict(count))
