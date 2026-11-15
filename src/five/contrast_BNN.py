import csv,sys,random,pathlib
sys.argv=[sys.argv[0],'KBNNvK'];exec(pathlib.Path(__file__).with_name('repeat_one.py').read_text().split('valid=(W!=255)')[0])
rng=random.Random(1817)
for j in range(500000):
 bk=rng.randrange(64);near=[p for p in range(64) if max(abs(p%8-bk%8),abs(p//8-bk//8))==1];b=rng.choice(near);k,n1,n2=rng.sample([x for x in range(64) if x not in (bk,b)],3);s=({k:'K',bk:'k',b:'B',n1:'N',n2:'N'},True,None)
 try:
  v.valid(s);u=v.alg(bk)+v.alg(b);t=v.play(s,u)
 except AssertionError:continue
 if v.probe(t)[0]!=1:continue
 d=int(W[index(s)]);assert d!=255
 if d==254:continue
 e=a.d0(t);assert e<d-1
 r=[v.fen(s),u,v.fen(t),d,e,j+1]
 with open(R/'BNN_WDL_contrast.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['FEN','UCI','target_FEN','DTM_source','DTM_target','trials']);w.writerow(r)
 print(r);break
else:raise AssertionError('not found')
