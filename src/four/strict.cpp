#define main oldmain
#include "solve.cpp"
#undef main
using D=uint16_t; const D INF=65535; vector<vector<D>> ds;
D getd(int id,Pos p){return ds[id][enc(ts[id],p)];}
void loadD(){ds.resize(ts.size());for(int i=0;i<(int)ts.size();i++){auto&t=ts[i];ds[i].resize(t.sz);ifstream f("dist_"+t.name+".bin",ios::binary);f.read((char*)ds[i].data(),2ull*t.sz);assert(f.gcount()==2ull*t.sz);}}
void calc(int id){auto&t=ts[id];auto&d=ds[id];d.assign(t.sz,INF);vector<uint8_t> pending(t.sz);vector<D> mx(t.sz);vector<vector<U>> buckets(512);auto push=[&](U a,int k){assert(k<INF);if(k>=int(buckets.size()))buckets.resize(k+1);d[a]=k;buckets[k].push_back(a);};
for(U a=0;a<(U)t.sz;a++){int z=t.v[a];if(z==INV)continue;if(z==DEAD){push(a,0);continue;}Pos p=dec(t,a);bool loser=z!=0&&z!=(p.turn?-1:1);int total=0,best=INF,worst=0,nn=0;moves(t,p,[&](Move m,Pos v){total++;auto[j,q]=child(t,p,m,v);int y=pc(ts[j].v[enc(ts[j],q)])*(q.turn!=1-p.turn?-1:1);if(y!=z){assert(!loser);return;}if(j==id&&m.cap<0&&!m.pr){if(loser)nn++;return;}D x=getd(j,q);if(loser){assert(x!=INF);worst=max(worst,int(x)+1);}else if(x!=INF)best=min(best,int(x)+1);});if(!total){push(a,0);continue;}if(loser){pending[a]=nn;mx[a]=worst;if(!nn)push(a,worst);}else if(best<INF)push(a,best);}
for(int k=0;k<(int)buckets.size();k++){for(size_t ix=0;ix<buckets[k].size();ix++){U a=buckets[k][ix];if(d[a]!=k)continue;int z=pc(t.v[a]);Pos p=dec(t,a);preds(t,p,[&](U b){if(t.v[b]!=z||(d[b]!=INF && d[b]<=k+1))return;Pos q=dec(t,b);bool loser=z!=0&&z!=(q.turn?-1:1);if(loser){assert(pending[b]);mx[b]=max(mx[b],D(k+1));if(--pending[b]==0)push(b,mx[b]);}else push(b,k+1);});}vector<U>().swap(buckets[k]);}
long long counts[3]={},inf[3]={};int mi[3]={INF,INF,INF},ma[3]={};for(U a=0;a<(U)t.sz;a++){if(t.v[a]==INV)continue;int z=pc(t.v[a])+1;counts[z]++;if(d[a]==INF){inf[z]++;assert(z==1);}else{mi[z]=min(mi[z],int(d[a]));ma[z]=max(ma[z],int(d[a]));}}
ofstream f("dist_"+t.name+".bin",ios::binary);f.write((char*)d.data(),2ull*d.size());lock_guard<mutex>lk(outmu);ofstream o("dist_stats.tsv",ios::app);for(int z=0;z<3;z++)if(counts[z])o<<t.name<<'\t'<<z-1<<'\t'<<counts[z]<<'\t'<<inf[z]<<'\t'<<mi[z]<<'\t'<<ma[z]<<'\n';cerr<<t.name<<" DTM/DTD done "<<counts[0]+counts[1]+counts[2]<<" inf "<<inf[1]<<" max "<<ma[0]<<','<<ma[1]<<','<<ma[2]<<endl;}
void dist_main(){init();setup();load();ds.resize(ts.size());remove("dist_stats.tsv");for(int i=0;i<6;i++)calc(i);for(int np=0;np<=2;np++){vector<int> jobs;for(int i=6;i<(int)ts.size();i++)if((ts[i].t[2]==P)+(ts[i].t[3]==P)==np)jobs.push_back(i);atomic<int> j{0};vector<thread> th;for(int w=0;w<4;w++)th.emplace_back([&]{for(;;){int x=j++;if(x>=(int)jobs.size())break;calc(jobs[x]);}});for(auto&x:th)x.join();}}

#ifndef STRICT_LIBRARY
int main(){dist_main();return 0;}
#endif
