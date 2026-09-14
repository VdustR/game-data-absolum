"""Generate a deliberately patterned Absolum battle-history save.

Usage: python gen.py INPUT_SAVE_BIN OUTPUT_DIRECTORY
The input is never modified. Output files are Save.bin and Save.temp.bin.
"""

import argparse
from pathlib import Path
from collections import defaultdict
from proto_wire import fields,encode_fields
import hashlib

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('input',type=Path)
parser.add_argument('output',type=Path)
args=parser.parse_args()
src=args.input
out=args.output
if not src.is_file():parser.error(f'input not found: {src}')
if out.resolve()==src.resolve().parent:parser.error('output directory must differ from input directory')
out.mkdir(parents=True,exist_ok=True)
if (out/'Save.bin').exists() or (out/'Save.temp.bin').exists():parser.error('output save already exists')
order=['BRO','HORDE','CLASHHERO','MANIA','RAGE','MAGIC','PANDEMONIUM','BOSS','ONEPUNCH','STEELAGE','SOULRUN','VAMPIRE','RIFTWAR','LOOT','HONOR','STARVING','GROUNDHOG']
stats={
 'Run.Tracking.FixRaw.Kills',
 'Run.Tracking.FixRaw.HighestComboDamage',
 'Run.Tracking.FixRaw.TotalDamage',
 'Run.Tracking.FixRaw.CriticalHits',
}
medal_keys={
 'Run.Tracking.FixRaw.ShopItemsBought',
 'Run.Badge_UltimateUses',
 'Run.Badge_MercenariesBought',
 'Run.Badge_ThrowableUses',
 'Run.Tracking.FixRaw.LifeHealed',
}
def plain(data):return [(n,w,v) for n,w,v,*_ in fields(data)]
def key(payload):return next((x.decode() for n,w,x in plain(payload) if n==1),'')
def value(payload):return next(x for n,w,x in plain(next(x for n,w,x in plain(payload) if n==2)) if n==1)
def entry(k,val):return encode_fields([(1,2,k.encode()),(2,2,encode_fields([(1,0,val)]))])
def special_path(payload):
 if b'/Specials/' not in payload:return ''
 return key(payload)
def is_selected(payload):return any(n==3 and w==0 and v==9 for n,w,v in plain(payload))
def nines(v):return int('9'*len(str(v)))

top=plain(src.read_bytes());si=next(i for i,(n,w,v) in enumerate(top) if n==17)
slot=plain(top[si][2]);indices=[i for i,(n,w,v) in enumerate(slot) if n==2]
assert len(indices)>=118
pool=defaultdict(dict)
for i in indices[:50]:
 rec=plain(slot[i][2]);inner=plain(rec[0][2]);char=next(v for n,w,v in inner if n==23)
 for n,w,v in inner:
  if n==43 and special_path(v) and is_selected(v):
   pool[char][special_path(v)]=v
assert {char:len(p) for char,p in pool.items()}=={1:5,2:5,3:5,4:5}
choices={char:sorted(p) for char,p in pool.items()}
changed_stats=0;changed_skills=0
for histnum,i in enumerate(indices):
 rec=plain(slot[i][2]);inner=plain(rec[0][2]);char=next(v for n,w,v in inner if n==23)
 dodge={key(v):value(v) for n,w,v in inner if n==50 and key(v) in ('Run.Tracking.FixRaw.SideStepDodge','Run.Tracking.FixRaw.JumpDodge')}
 dodge_keeper='Run.Tracking.FixRaw.JumpDodge' if 'Run.Tracking.FixRaw.JumpDodge' in dodge else 'Run.Tracking.FixRaw.SideStepDodge'
 if not dodge:dodge_keeper='Run.Tracking.FixRaw.JumpDodge'
 fixed={'Run.Tracking.FixRaw.Clash':999,'Run.Tracking.FixRaw.Deflect':999,'Run.Tracking.FixRaw.LifeLost':0}
 seen_fixed=set();seen_duration=False;seen_medals=set()
 for j,(n,w,v) in enumerate(inner):
  if n==6 and w==0:inner[j]=(6,0,nines(v))
  elif n==50:
   k=key(v)
   if k in dodge:
    new=999 if k==dodge_keeper else 0
    inner[j]=(50,2,entry(k,new));changed_stats+=1
   elif k in fixed:
    inner[j]=(50,2,entry(k,fixed[k]));seen_fixed.add(k);changed_stats+=1
   elif k in medal_keys:
    inner[j]=(50,2,entry(k,0));seen_medals.add(k);changed_stats+=1
   elif k in stats:
    old=value(v)
    if old>0:inner[j]=(50,2,entry(k,nines(old)));changed_stats+=1
   elif k=='Run.FixRaw.gameDuration':
    inner[j]=(50,2,entry(k,35999));seen_duration=True
 missing=[]
 if not dodge:missing.append((50,2,entry('Run.Tracking.FixRaw.JumpDodge',999)))
 if not seen_duration:missing.append((50,2,entry('Run.FixRaw.gameDuration',35999)))
 for k in sorted(fixed.keys()-seen_fixed):missing.append((50,2,entry(k,fixed[k])))
 for k in sorted(medal_keys-seen_medals):missing.append((50,2,entry(k,0)))
 if missing:
  # Keep tracking variables together; the game drops them if appended after later fields.
  insert_at=max(j for j,(n,w,v) in enumerate(inner) if n==50)+1
  inner[insert_at:insert_at]=missing
 if 50<=histnum<118:
  name=next((name for name in order if f'Run.CO_Preset_SUCCESS_ORDEAL_{name}'.encode() in rec[0][2]),None)
  assert name,name
  chosen=choices[char][order.index(name)%5]
  payload=pool[char][chosen]
  selected=[j for j,(n,w,v) in enumerate(inner) if n==43 and special_path(v) and is_selected(v)]
  assert len(selected)==1,(histnum,selected)
  oldpos=selected[0]
  inner=[(n,w,v) for j,(n,w,v) in enumerate(inner) if j==oldpos or not(n==43 and special_path(v)==chosen)]
  oldpos=next(j for j,(n,w,v) in enumerate(inner) if n==43 and special_path(v) and is_selected(v))
  inner[oldpos]=(43,2,payload)
  assert sum(bool(n==43 and special_path(v) and is_selected(v)) for n,w,v in inner)==1
  assert sum(n==43 and special_path(v)==chosen for n,w,v in inner)==1
  changed_skills+=1
 rec[0]=(1,2,encode_fields(inner));slot[i]=(2,2,encode_fields(rec))
assert changed_skills==68,changed_skills
top[si]=(17,2,encode_fields(slot));result=encode_fields(top)
for name in ('Save.bin','Save.temp.bin'):(out/name).write_bytes(result)
print('stats',changed_stats,'skills',changed_skills,'sha256',hashlib.sha256(result).hexdigest(),'bytes',len(result))
print('skill choices per character:',{char:[path.split('/')[-1] for path in paths] for char,paths in choices.items()})
