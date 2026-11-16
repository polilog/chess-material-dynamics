from pathlib import Path
import csv,collections,itertools,numpy as np, functools
ROOT=Path(__file__).resolve().parent.parent;OUT=Path(__file__).resolve().parent;S=ROOT/'four'
def read(p):return list(csv.DictReader(open(ROOT/p)))
def write(name,fields,rows):
 with open(OUT/name,'w',newline='') as f:
  w=csv.writer(f);w.writerow(fields);w.writerows(rows)
order='KQRBNP'
def flip(m):return 'v'.join(m.split('v')[::-1])
def canonical(m):
 a,b=m.split('v');return len(a)<len(b) or (len(a)==len(b)==2 and order.index(a[1])>order.index(b[1]))
def canon(z,ms):return (-z,tuple(map(flip,ms))) if canonical(ms[0]) else (z,ms)
def key(x):return str(x[0])+'/'+ '/'.join(x[1])
def n(m):return len(m)-1
V4={(r['material'],int(r['WDL'])) for r in read('four/vertices.csv')}
E={(r['source'],r['target'],int(r['WDL'])) for r in read('four/strict_edges.csv')}
P={};old={}
for line in open(S/'path_input.tsv'):
 z,word,status=line.rstrip().split('\t');z=int(z);ms=tuple(word.split('/'));P[key(canon(z,ms))]=canon(z,ms)
for r in read('four/repeat_paths.csv'):
 old[(int(r['WDL']),tuple(r['material_path'].split(' -> ')))]=r['status'] if 'status' in r else r['strict_status']
rows=collections.defaultdict(list)
for k,(z,ms) in sorted(P.items()):
 if all((a,b,z) in E for a,b in zip(ms,ms[1:])):rows[ms[0]].append((z,ms))
turnwords={}
for m,pp in rows.items():
 nw=(len(pp)+63)//64;size=(S/('tb_'+m+'.bin')).stat().st_size;ep=2 if m=='KPvKP' else 1
 a=np.memmap(S/('mask_'+m+'.bin'),dtype='<u8',mode='r',shape=(size,nw));
 # ep-state pairs precede side-to-move bit in original indexing.
 rr=a.reshape(-1,2,ep,nw);o=np.bitwise_or.reduce(np.bitwise_or.reduce(rr,axis=0),axis=1)
 for i,(z,ms) in enumerate(pp):
  for t in (0,1):
   yes=bool((int(o[t,i//64])>>(i%64))&1);turnwords[z,ms,t]=yes
   if flip(ms[0])!=ms[0]:turnwords[-z,tuple(map(flip,ms)),1-t]=yes
 del rr,a
for (z,ms),st in old.items():
 assert (turnwords.get((z,ms,0),False) or turnwords.get((z,ms,1),False))==(st=='YES'),(z,ms,st)
# aggregate exact fresh-history turn-specific pairs (terminal target can be first position reached).
T=sorted(V4);ix={k:i for i,k in enumerate(T)}
base={(m,z,t):1<<ix[m,z] for m,z in V4 for t in (0,1)}
for (z,ms,t),yes in turnwords.items():
 if yes:base[ms[0],z,t]|=1<<ix[ms[-1],z]
oldpairs=read('four/strict_pairs.csv');out=[];no=[]
for r in oldpairs:
 a,b,z=r['source'],r['target'],int(r['WDL']);v=1<<ix[b,z];ys=[bool(base[a,z,t]&v) for t in (0,1)];assert any(ys)==(r['strict_status']=='YES');out.append((a,b,z,*map(int,ys)))
 if any(ys) and not all(ys):no.append((a,b,z, 'white' if not ys[0] else 'black'))
write('turn_pairs4.csv',['source','target','WDL','white_to_move_yes','black_to_move_yes'],out)
write('turn_sensitive4.csv',['source','target','WDL','forbidden_start_turn'],no)
print('4-piece turn-sensitive pairs',len(no),'by WDL',collections.Counter(x[2] for x in no),flush=True)
