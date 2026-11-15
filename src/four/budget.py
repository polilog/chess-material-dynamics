import csv,json,collections
E={(r['source'],r['target'],r['WDL']):set(map(int,r['source_distance_values'].strip(',').split(','))) for r in csv.DictReader(open('strict_edges.csv'))}
R=list(csv.DictReader(open('strict_paths.csv')));fails=[]
for r in R:
    m=r['material_path'].split(' -> ');z=r['WDL'];ds=[E[a,b,z] for a,b in zip(m,m[1:])];p=ds[0]
    for d in ds[1:]:p={x for x in d if any(y>x for y in p)}
    if not p:
        assert r['strict_status']=='NO'
        fails.append([z,r['material_path'],r['WDL_status'],json.dumps([sorted(x) for x in ds])])
with open('budget_forbidden.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['WDL','material_path','old_WDL_status','edge_source_distance_sets']);w.writerows(fails)
print('budget forbidden',len(fails),'new vs WDL',sum(x[2]=='YES' for x in fails))
