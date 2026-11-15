"""Expand canonical predecessor flags to all physical boards and compare with released barriers."""
import csv,sys,pathlib,collections
import audit as a
v=a.v;root=pathlib.Path(sys.argv[1]);bs={}
for r in csv.DictReader(open(sys.argv[2]),delimiter='\t'):
 s=v.parse(r['FEN']);b,t,e=s;flags=int(r['flags']);z=int(r['WDL']);assert not flags&4
 cat='GEOMETRIC' if not flags&1 else 'TERMINAL_PREDECESSOR' if not flags&2 else 'WDL'
 for x in ([0,7] if 'P' in r['material'] else [0,7,56,63]):
  q=({p^x:c for p,c in b.items()},t,None if e is None else e^x)
  for st,zz in [(q,z),(v.mirror(q),-z)]:
   f=v.fen(st);z2,dead=v.probe(st);assert z2==zz;bs[f]=(v.material(st),zz,cat,str(dead))
ref={r['FEN']:(r['material'],int(r['WDL']),r['category'],r['dead']) for r in csv.DictReader(open(root/'results/wdl/absolute_position_barriers.csv'))};assert bs==ref;assert len(bs)==4332
print('PASS: 4,332 absolute position barriers; 2,268 genuine WDL barriers')
