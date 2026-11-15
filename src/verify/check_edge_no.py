"""Revalidate every final direct five-piece NO using generated target statistics."""
import csv,collections,sys,pathlib
import audit as a
v=a.v;root=pathlib.Path(sys.argv[1]);turn={};prom={}
for line in open(sys.argv[2]):
 x=line.strip().split('\t');typ,m,z,c=x[:4];z,c=int(z),int(c)
 if typ=='T':
  for k in ((m,z,c),(v.flip(m),-z,1-c)):turn[k]=int(x[4])
 else:
  for k in ((m,z,c,x[4]),(v.flip(m),-z,1-c,x[4])):prom[k]=tuple(map(int,x[5:]))
exact=collections.defaultdict(int);solved=set()
for r in csv.DictReader(open(root/'results/five/exact/turn_pairs.csv')):
 m,t,z=r['source'],r['target'],int(r['WDL']);solved|={m,v.flip(m)};cnt=int(r['count_DTM_or_DTD0'])+int(r['count_DTM_or_DTD3']);exact[m,t,z]+=cnt;exact[v.flip(m),v.flip(t),-z]+=cnt
count=0
for r in csv.DictReader(open(root/'results/five/edges.csv')):
 if r['status_both_models']!='NO':continue
 m,t,z,ty=r['source'],r['target'],int(r['WDL']),r['type'];ss=m.split('v');tt=t.split('v');w=[collections.Counter(x) for x in ss];b=[collections.Counter(x) for x in tt];why=r['reason']
 if why=='exact_five_DTM_DTD_exhaustion':assert m in solved and not exact[m,t,z]
 elif ty=='capture':
  c=next(i for i in (0,1) if len(ss[i])>len(tt[i]));assert not turn[t,z,c]
 elif ty=='capture_promotion':
  c=next(i for i in (0,1) if w[i]['P']>b[i]['P'] and sum(w[i].values())==sum(b[i].values()));p=next(x for x in 'QRBN' if b[c][x]>w[c][x]);rank,wdl,d0,d3=prom[t,z,c,p];assert not rank or not wdl or not d0 and not d3
 else:raise AssertionError(r)
 count+=1
assert count==192;print('PASS: 192 direct-edge negative certificates')
