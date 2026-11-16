import csv, collections, mmap, struct, json
from pathlib import Path
import legacy_verify as v
ROOT=Path(__file__).parent
D={}
def distance(s):
    b,t,e=s;w,bl=v.material(s).split('v');sw=len(w)<len(bl) or (len(w)==len(bl)==2 and v.ORDER.index(w[1])>v.ORDER.index(bl[1]));
    if sw:b,t,e=v.mirror(s);w,bl=bl,w
    m=w+'v'+bl;pp=[next(p for p,c in b.items() if c=='K'),next(p for p,c in b.items() if c=='k')]
    for col in (False,True):pp.extend(sorted((p for p,c in b.items() if c.upper()!='K' and c.islower()==col),key=lambda p:(v.ORDER.index(b[p].upper()),p)))
    h=pp[0]%8>=4;vert='P' not in m and pp[0]//8>=4;pp=[p^(7 if h else 0)^(56 if vert else 0) for p in pp]
    ix=pp[0]//8*4+pp[0]%8
    for p in pp[1:]:ix=ix*64+p
    ix=ix*2+int(t)
    if m=='KPvKP':ix=ix*2+int(e is not None)
    if m not in D:
        f=open(ROOT/(('rep3_' if m=='KPvKP' else 'rep4_')+m+'.bin'),'rb');D[m]=(f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ))
    return struct.unpack_from('<H',D[m][1],ix*2)[0]
def check(k,steps):
    a,m,b=v.verify_path(k,steps)
    s=v.parse(a);d=distance(s);assert d<65535;initial=d
    for u in m.split():
        s=v.play(s,u);dd=distance(s);assert dd==d-1,(k,u,d,dd);d=dd
    return a,m,b,initial,d
def flipkey(k):
    z,*ms=k.split('/');return '/'.join([str(-int(z))]+[v.flip(m) for m in ms])
def flipcert(a,m,b):
    return v.fen(v.mirror(v.parse(a))),' '.join(v.alg(v.sq(u[:2])^56)+v.alg(v.sq(u[2:4])^56)+u[4:] for u in m.split()),v.fen(v.mirror(v.parse(b)))
def write(name,head,rows):
    with open(ROOT/name,'w',newline='') as f:w=csv.writer(f);w.writerow(head);w.writerows(rows)
paths={}
for line in open(ROOT/'repeat_paths_canon.tsv'):
    k,status,*steps=line.rstrip('\n').split('\t');val=check(k,steps) if status=='YES' else ('','','','','');paths[k]=(status,*val)
    if status=='YES':a,m,b,di,df=val; paths[flipkey(k)]=(status,*flipcert(a,m,b),di,df)
    else:paths[flipkey(k)]=(status,*val)
old={ '/'.join([x['WDL']]+x['material_path'].split(' -> ')):x for x in csv.DictReader(open(ROOT/'material_paths.csv'))}
assert paths.keys()==old.keys(),(len(paths),len(old))
rows=[];pairs={};oldpairs=set();bad=[]
for k,x in sorted(paths.items()):
    z,*ms=k.split('/');st,a,m,b,di,df=x;prior=old[k]['status'];assert st!='YES' or prior=='YES'
    rows.append([z,' -> '.join(ms),prior,st,a,m,b,di,df]);pair=(z,ms[0],ms[-1]);oldpairs.add(pair)
    if st=='YES':pairs[pair]=[a,m,b,di,df,' -> '.join(ms)]
    else:bad.append([z,' -> '.join(ms),prior,st])
write('repeat_paths.csv',['WDL','material_path','WDL_status','strict_status','FEN','UCI_moves','final_FEN','initial_distance','final_distance'],rows)
write('repeat_forbidden_paths.csv',['WDL','material_path','WDL_status','strict_status'],bad)
write('repeat_pairs.csv',['WDL','source','target','strict_status','FEN','UCI_moves','final_FEN','initial_distance','final_distance','material_path'],[[*p,'YES',*pairs[p]] if p in pairs else [*p,'NO','','','','','',''] for p in sorted(oldpairs)])
mins=[]
for k,(st,*_) in paths.items():
    if st=='YES':continue
    z,*ms=k.split('/');subs=['/'.join([z]+ms[i:j]) for i in range(len(ms)) for j in range(i+2,len(ms)+1) if j-i<len(ms)]
    if all(paths[x][0]=='YES' for x in subs):mins.append([z,' -> '.join(ms),old[k]['status']])
write('repeat_minimal_obstructions.csv',['WDL','path','WDL_status'],sorted(mins))
E={}
for line in open(ROOT/'strict_edges_canon.tsv'):
    a,b,z,n,d,f,u,dd=line.rstrip('\n').split('\t');s=v.parse(f);t=v.play(s,u);assert v.material(s)==a and v.material(t)==b;assert v.probe(s)==(int(z),False) and v.probe(t)[0]==int(z);assert distance(s)==int(d) and distance(t)==int(d)-1
    E[(a,b,z)]=[f,u,v.fen(t),d,dd]
    E[(v.flip(a),v.flip(b),str(-int(z)))]=[*flipcert(f,u,v.fen(t)),d,dd]
write('repeat_edges.csv',['source','target','WDL','FEN','UCI','target_FEN','distance','source_distance_values_DTD0'],[[*k,*x] for k,x in sorted(E.items())])
assert len(E)==356
verts=list(csv.DictReader(open(ROOT/'vertices.csv')))
heights=[]
for x in verts:
    m=x['material'];z=x['WDL'];n=len(m)-1;h=n
    for zz,a,b in pairs:
        if zz==z and b==m:h=max(h,len(a)-1)
    heights.append([m,z,h])
write('repeat_heights.csv',['material','WDL','height_cap4'],heights)
summary={'paths':dict(collections.Counter(x[0] for x in paths.values())),'new_no_paths':sum(x[0]=='NO' and old[k]['status']=='YES' for k,x in paths.items()),'pairs_yes':len(pairs),'pairs_no':len(oldpairs)-len(pairs),'minimal_obstructions':len(mins),'heights':dict(collections.Counter(x[2] for x in heights)),'no_by_WDL':dict(collections.Counter(k.split('/')[0] for k,x in paths.items() if x[0]=='NO')),'new_no_by_WDL':dict(collections.Counter(k.split('/')[0] for k,x in paths.items() if x[0]=='NO' and old[k]['status']=='YES'))}
print(json.dumps(summary,indent=2));json.dump(summary,open(ROOT/'repeat_summary.json','w'),indent=2)
