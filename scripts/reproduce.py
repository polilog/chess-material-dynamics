#!/usr/bin/env python3
"""Rebuild exact data in an ignored work directory, then audit release artifacts.
No binary tablebase downloads; C++17 and NumPy required. Never overwrite results/.
"""
import argparse,csv,pathlib,shutil,subprocess,sys,os,collections,json
ROOT=pathlib.Path(__file__).resolve().parents[1];DATA=ROOT/'results'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('stage',choices=['structure','certificates','four','five','wdl','wdl-four','full']);p.add_argument('--work',type=pathlib.Path,default=ROOT/'work');p.add_argument('--rebuild',action='store_true');a=p.parse_args();w=a.work.resolve();CXX=os.environ.get('CXX','g++')
 def run(args,cwd=None,stdout=None):
  args=list(map(str,args));print('+',' '.join(args),flush=True);subprocess.run(args,cwd=cwd,check=True,stdout=stdout)
 def py(f,*args,cwd=None):run([sys.executable,f,*args],cwd)
 def build(d,src,out=None):
  out=out or src.removesuffix('.cpp');run([CXX,'-O3','-std=c++17','-pthread',src,'-o',out],d);return d/out
 def exe(d,src,*args,stdout=None):run([build(d,src),*args],d,stdout)
 def rows(f):return list(csv.DictReader(open(f)))
 def wr(f,head,rs):
  with open(f,'w',newline='') as fp:q=csv.DictWriter(fp,head);q.writeheader();q.writerows(rs)
 py(ROOT/'scripts/check_structure.py')
 if a.stage=='structure':return
 # Source files copied into work tree; release data never modified.
 for d in ('four','five','verify','wdl'):shutil.copytree(ROOT/'src'/d,w/d,dirs_exist_ok=True)
 four,five,ver,wdl=(w/d for d in ('four','five','verify','wdl'))
 # Candidate words are derived from the final public WDL table, not a search log.
 ps=rows(DATA/'four/paths.csv');shutil.copyfile(DATA/'four/vertices.csv',four/'vertices.csv')
 wr(four/'material_paths.csv',['WDL','material_path','status','FEN','UCI_moves','final_FEN'],[dict(WDL=r['WDL'],material_path=r['material_path'],status=r['wdl_status'],FEN=r['wdl_FEN'],UCI_moves=r['wdl_UCI_moves'],final_FEN=r['wdl_final_FEN']) for r in ps])
 with open(four/'path_input.tsv','w') as f:
  for r in ps:print(r['WDL'],r['material_path'].replace(' -> ','/'),r['wdl_status'],sep='\t',file=f)
 def have(prefix,count):return len(list(four.glob(prefix+'*.bin')))==count
 if a.rebuild or not have('tb_',36):exe(four,'solve.cpp')
 if a.rebuild or not have('dist_',36):exe(four,'strict.cpp')
 if a.rebuild or not (have('rep4_',36) and (four/'rep3_KPvKP.bin').exists()):exe(four,'repeat_dp.cpp');exe(four,'repeat6.cpp')
 py(ver/'check_four.py',ROOT);py(ver/'check_global.py',DATA/'global/strict_witnesses.csv')
 if a.stage=='certificates':return
 if a.stage in ('four','full'):
  exe(four,'audit_wdl.cpp');exe(four,'audit_strict.cpp');exe(four,'path_strict.cpp');py(four/'export_strict.py',cwd=four);exe(four,'repeat_audit.cpp');py(four/'verify_repetition.py',cwd=four);exe(four,'path_repeat.cpp');py(four/'export_repeat.py',cwd=four);py(four/'budget.py',cwd=four);py(four/'turn_graph.py',cwd=four)
  for file,col in [('strict_paths.csv','strict_status'),('repeat_paths.csv','strict_status')]:
   got={(r['WDL'],r['material_path']):r[col] for r in rows(four/file)};want={(r['WDL'],r['material_path']):r['strict_status'] for r in ps};assert got==want,file
  assert {(r['source'],r['target'],r['WDL'],r['white_to_move_yes'],r['black_to_move_yes']) for r in rows(four/'turn_pairs4.csv')}=={(r['source'],r['target'],r['WDL'],r['white_to_move_yes'],r['black_to_move_yes']) for r in rows(DATA/'four/turn_pairs.csv')}
  assert len(rows(four/'budget_forbidden.csv'))==108
  # independent exact DTD0 boundary and WDL pawn/queen turn test
  exe(five,'dtd0_boundary.cpp');exe(five,'wdl_turn.cpp')
  print('PASS: exhaustive four-piece strict classifications match the release',flush=True)
 if a.stage in ('wdl-four','full'):
  # Independent WDL graph construction and exact material-word enumeration.
  if not (four/'results.tsv').exists():exe(four,'solve.cpp')
  exe(four,'paths_wdl.cpp');py(four/'legacy_verify.py',cwd=four)
  got={(r['WDL'],r['material_path']):r['status'] for r in rows(four/'material_paths.csv')}
  assert got=={(r['WDL'],r['material_path']):r['wdl_status'] for r in ps}
  print('PASS: full WDL path universe reproduced',flush=True)
 if a.stage in ('five','full'):
  for source,args in [('solve5.cpp',['Q','R']),('mixed.cpp',['Q','R']),('one_sided.cpp',['BBB','BBN','BNN','NNN'])]:
   bin=build(five,source)
   for x in args:run([bin,x],five)
  py(five/'audit_examples.py',cwd=five);py(five/'audit_mixed.py',cwd=five)
  for x in ('BBB','BBN','BNN','NNN'):py(five/'repeat_one.py','K'+x+'vK',cwd=five);py(five/'audit_one.py','K'+x+'vK',cwd=five)
  # Compare numeric exact results, not arbitrary choice of witness FEN.
  for ref in (DATA/'five/exact').glob('*_stats.tsv'):
   def parsed(path):
    xs=list(csv.reader(open(path),delimiter='\t'));return xs[0],[r[:-1] if xs[0][-1]=='max_fen' else r for r in xs[1:3]],xs[3]
   assert parsed(ref)==parsed(five/ref.name),ref
  ref={(r['source'],r['WDL'],r['black_to_move'],r['target']):(int(r['count_DTM_or_DTD0']),int(r['count_DTM_or_DTD3'])) for r in rows(DATA/'five/exact/turn_pairs.csv')}
  for x in ('BBB','BBN','BNN','NNN'):
   with open(five/f'K{x}vK_pairs_DTD3.tsv') as inp:
    for r in csv.DictReader(inp,delimiter='\t'):
     assert ref[r['source'],r['WDL'],r['turn'],r['target']]==(int(r['count']),int(r['count_DTD3']))
  # Recompute and verify the 192 direct-edge exclusions from exact target-side filters and solved sources.
  with open(w/'edge_upper.tsv','w') as out:exe(ver,'edge_upper.cpp',stdout=out)
  py(ver/'check_edge_no.py',ROOT,w/'edge_upper.tsv');py(ver/'check_five.py',ROOT)
  print('PASS: selected exact five-piece tables and final five-piece positive certificates',flush=True)
 if a.stage in ('wdl','full'):
  py(ver/'check_wdl.py',ROOT)
  # Exhaustive absolute predecessor flags from <=4. Output is regenerated in work/four.
  with open(w/'position_stats.csv','w') as out:run([build(wdl,'posbar.cpp')],four,out)
  py(ver/'check_positional.py',ROOT,four/'position_barriers.tsv',w/'position_stats.csv')
 print('Completed stage:',a.stage,flush=True)
if __name__=='__main__':main()
