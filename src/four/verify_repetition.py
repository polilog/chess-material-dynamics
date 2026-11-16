import collections
import legacy_verify as v
from pathlib import Path
for line in open(Path(__file__).parent/'infinite_repeat_examples.tsv'):
    m,a,f,d,seq=line.rstrip('\n').split('\t');s=v.parse(f);counts=collections.Counter([v.fen(s).split(' 0 1')[0]])
    for i,u in enumerate(seq.split(),1):
        assert v.probe(s)==(0,False);s=v.play(s,u);assert v.probe(s)[0]==0;k=v.fen(s).split(' 0 1')[0];counts[k]+=1
        assert counts[k]<3 or i==int(d)
    assert i==int(d) and counts[k]==3
print('240 repetition witnesses checked')
