"""Check a generated Absolum save against its untouched source.

Usage: python test.py INPUT_SAVE_BIN OUTPUT_SAVE_BIN
This is a structural and preservation check; the final check is loading the save in game.
"""

import argparse
from collections import Counter,defaultdict
from pathlib import Path
from proto_wire import fields

STATS={
 'Run.Tracking.FixRaw.Kills',
 'Run.Tracking.FixRaw.HighestComboDamage',
 'Run.Tracking.FixRaw.TotalDamage',
 'Run.Tracking.FixRaw.CriticalHits',
}
MEDAL_KEYS={
 'Run.Tracking.FixRaw.ShopItemsBought',
 'Run.Badge_UltimateUses',
 'Run.Badge_MercenariesBought',
 'Run.Badge_ThrowableUses',
 'Run.Tracking.FixRaw.LifeHealed',
}
CHAR_CLASS={1:'Dwarf',2:'Rogue',3:'Sorcerer',4:'Warrior'}
ORDEALS=('BRO','HORDE','CLASHHERO','MANIA','RAGE','MAGIC','PANDEMONIUM','BOSS','ONEPUNCH','STEELAGE','SOULRUN','VAMPIRE','RIFTWAR','LOOT','HONOR','STARVING','GROUNDHOG')

def plain(data):return [(n,w,v) for n,w,v,*_ in fields(data)]
def key(payload):return next((v.decode() for n,w,v in plain(payload) if n==1),'')
def val(payload):return next(v for n,w,v in plain(next(v for n,w,v in plain(payload) if n==2)) if n==1)
def special(payload):
 if b'/Specials/' not in payload:return None
 # The pickup path is wrapped in a nested field 1.
 return next((v.decode() for n,w,v in plain(next(v for n,w,v in plain(payload) if n==1)) if n==1),None)
def selected(payload):return any(n==3 and w==0 and v==9 for n,w,v in plain(payload))
def all_nines(value):return value>=0 and set(str(value))=={'9'}
def unpack(data):
 top=plain(data);slot=next(v for n,w,v in top if n==17);slot=plain(slot)
 histories=[plain(next(v for n,w,v in plain(h) if n==1)) for n,w,h in slot if n==2]
 return top,slot,histories

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('source',type=Path)
parser.add_argument('candidate',type=Path)
args=parser.parse_args()
source=args.source.read_bytes();candidate=args.candidate.read_bytes()
src_top,src_slot,src_hist=unpack(source)
dst_top,dst_slot,dst_hist=unpack(candidate)
assert len(src_hist)==len(dst_hist)>=118
assert [(n,w,v) for n,w,v in src_top if n!=17]==[(n,w,v) for n,w,v in dst_top if n!=17]
assert [(n,w,v) for n,w,v in src_slot if n!=2]==[(n,w,v) for n,w,v in dst_slot if n!=2]

per_preset=defaultdict(set)
skill_cycle=defaultdict(set)
modified_stats=0
for index,(before,after) in enumerate(zip(src_hist,dst_hist)):
 assert next(v for n,w,v in before if n==23)==next(v for n,w,v in after if n==23)
 character=next(v for n,w,v in after if n==23)
 assert character in CHAR_CLASS
 assert [(n,w,v) for n,w,v in before if n not in (6,43,50)]==[(n,w,v) for n,w,v in after if n not in (6,43,50)]
 scores=[v for n,w,v in after if n==6 and w==0]
 assert len(scores)==1 and all_nines(scores[0]) and len(str(scores[0]))==len(str(next(v for n,w,v in before if n==6)))
 old_vars={key(v):val(v) for n,w,v in before if n==50}
 new_vars={key(v):val(v) for n,w,v in after if n==50}
 assert old_vars.keys()<=new_vars.keys()
 assert new_vars.get('Run.FixRaw.gameDuration')==35999,(index,old_vars.get('Run.FixRaw.gameDuration'))
 assert new_vars['Run.Tracking.FixRaw.Clash']==999
 assert new_vars['Run.Tracking.FixRaw.Deflect']==999
 assert new_vars['Run.Tracking.FixRaw.LifeLost']==0
 assert new_vars.get('Run.Tracking.FixRaw.SideStepDodge',0)+new_vars.get('Run.Tracking.FixRaw.JumpDodge',0)==999
 assert all(new_vars.get(name)==0 for name in MEDAL_KEYS),(index,{name:new_vars.get(name) for name in MEDAL_KEYS})
 assert sum(n==50 for n,w,v in after)==len(new_vars),index
 for name in old_vars:
  if name in STATS and old_vars[name]>0:
   assert all_nines(new_vars[name]) and len(str(new_vars[name]))==len(str(old_vars[name]))
   modified_stats+=1
  elif name not in MEDAL_KEYS|{'Run.FixRaw.gameDuration','Run.Tracking.FixRaw.Clash','Run.Tracking.FixRaw.Deflect','Run.Tracking.FixRaw.LifeLost','Run.Tracking.FixRaw.SideStepDodge','Run.Tracking.FixRaw.JumpDodge'}:
   assert new_vars[name]==old_vars[name],(index,name)
 old_pickups=[v for n,w,v in before if n==43]
 new_pickups=[v for n,w,v in after if n==43]
 if index<50 or index>=118:
  assert old_pickups==new_pickups
 else:
  old_other=[v for v in old_pickups if special(v) is None]
  new_other=[v for v in new_pickups if special(v) is None]
  assert old_other==new_other
  chosen=[special(v) for v in new_pickups if special(v) is not None and selected(v)]
  assert len(chosen)==1 and f'/Specials/{CHAR_CLASS[character]}_' in chosen[0]
  assert len(set(special(v) for v in new_pickups if special(v) is not None))==len([v for v in new_pickups if special(v) is not None])
  name=next((name for name in ORDEALS if f'Run.CO_Preset_SUCCESS_ORDEAL_{name}' in new_vars),None)
  assert name is not None
  per_preset[name].add(character)
  skill_cycle[character].add(chosen[0])

assert set(per_preset)==set(ORDEALS)
assert all(chars==set(CHAR_CLASS) for chars in per_preset.values())
assert all(len(skills)==5 for skills in skill_cycle.values())
assert modified_stats>300,modified_stats
print(f'PASS: {len(dst_hist)} histories, {modified_stats} patterned stats, 17 ordeals x 4 characters, 5 authentic skills per character')
