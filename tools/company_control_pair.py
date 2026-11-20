"""One local append to a private primary/backup pair.

Caller must hold operational maintenance, validate actual authorization and
verify the backup volume. No approval, access grant or service created here.
Preserve exact candidate bytes for forward recovery. No rollback by truncation.
"""
import json
from pathlib import Path
from .company_control_register import require

def append_pair(*,company,source,backup,predecessor,successor,check_authority,check_destination):
    source,backup=Path(source),Path(backup)
    require(source!=backup and source.parent!=backup.parent,"separate destinations")
    old,new=map(json.loads,(predecessor,successor))
    for doc,raw in ((old,predecessor),(new,successor)):
        company.replay(doc);require(company.canonical(doc)==raw,"canonical bytes")
    require(len(new["events"])==len(old["events"])+1 and new["events"][:-1]==old["events"],"one append only")
    pin=company.digest(old)
    def check():
        check_authority();check_destination()
    def observe():
        check()
        return (company.canonical(company.load(source)),company.canonical(company.load(backup)))
    check()
    with company.locked_snapshot_writer(source) as primary:
        with company.locked_snapshot_writer(backup) as replica:
            states=[(predecessor,predecessor),(successor,predecessor),(successor,successor)]
            pair=observe()
            require(pair in states,"unexpected pair; preserve history and reconcile")
            phase=states.index(pair)
            if phase==0:
                check();primary(new,expected_digest=pin)
                require(observe()==states[1],"primary verification")
            if phase<=1:
                check();replica(new,expected_digest=pin)
            require(observe()==states[2],"backup verification")
            return "already-completed" if phase==2 else "completed"
