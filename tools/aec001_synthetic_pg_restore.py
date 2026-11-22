#!/usr/bin/env python3
"""Local PostgreSQL synthetic-only logical restore drill; no production connections.

Creates a temporary PostgreSQL cluster under an owner-only audit directory;
TCP listen_addresses is EMPTY, all clients use one private Unix socket.
Never accepts user database, host, dump, credentials, arbitrary SQL or container.
Cleanup includes stopping the temporary server. It does not test real backups.
"""
import argparse
from datetime import datetime, timezone
import getpass
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

from aec001_service_catalog import write_private_output

SCHEMA="aec001-synthetic-pg-restore-v1"
PORT=54879
N=42
EXPECTED_SUM=N*(N+1)//2
SOURCE_DB="aec001_fixture_source"
TARGET_DB="aec001_fixture_restored"

def fixture_environment(sock):
    # Do not inherit PGHOST, PGPORT, PGSERVICE, PGOPTIONS or credentials.
    return {"PATH":os.environ.get("PATH","/usr/bin:/bin"),
            "HOME":str(Path.home()),"LANG":"C","LC_ALL":"C",
            "PGHOST":str(sock),"PGPORT":str(PORT),
            "PGUSER":getpass.getuser(),"PGDATABASE":"postgres",
            "PGCONNECT_TIMEOUT":"3"}

def private_audit_root(output):
    if not output.is_absolute() or output.name in ("",".",".."):
        raise ValueError("must choose an absolute output filename")
    parent=output.parent
    for ancestor in (parent,*parent.parents):
        if (ancestor/".git").exists():
            raise ValueError("fixture output inside Git checkout is forbidden")
    if parent.is_symlink() or not parent.is_dir() or parent.stat().st_mode & 0o077:
        raise ValueError("output parent is not private")
    if output.is_symlink() or (output.exists() and not output.is_file()):
        raise ValueError("unsafe output")
    if shutil.which("initdb") is None:
        raise ValueError("PostgreSQL fixture binaries unavailable")
    for binary in ("pg_ctl","createdb","psql","pg_dump","pg_restore"):
        if shutil.which(binary) is None:
            raise ValueError("PostgreSQL fixture binaries unavailable")
    return parent

def run(args,env,timeout=28):
    x=subprocess.run(args,env=env,capture_output=True,text=True,timeout=timeout,check=False)
    if x.returncode:
        raise RuntimeError("isolated PostgreSQL fixture command failed")
    return x.stdout.strip()

def inspect_settings(env):
    host=run(["psql","-X","-q","-tA","-d","postgres",
              "-v","ON_ERROR_STOP=1","-c","SHOW listen_addresses"],env)
    socket=run(["psql","-X","-q","-tA","-d","postgres",
                "-v","ON_ERROR_STOP=1","-c","SHOW unix_socket_directories"],env)
    if host!="" or socket!=env["PGHOST"]:
        raise RuntimeError("fixture server is not socket-only")
    return True

def restore_fixture(parent):
    # macOS Unix sockets have short sockaddr_un path limits: use a private,
    # auto-removed system temp directory. Never use an existing PG data path.
    with tempfile.TemporaryDirectory(prefix="aec001-pg-",dir=tempfile.gettempdir()) as tmp:
        work=Path(tmp)
        cluster=work/"cluster"
        socket=work/"socket"
        socket.mkdir(mode=0o700)
        log=work/"startup.log"
        dump=work/"fixture.dump"
        env=fixture_environment(socket)
        # PG directory, PG socket and fixture dump are entirely within this temp root.
        run(["initdb","-D",str(cluster),"--no-instructions","--auth=trust"],env,timeout=35)
        started=False
        try:
            options=(" -c listen_addresses='' "
                     "-c unix_socket_directories="+str(socket)+
                     " -c unix_socket_permissions=0700"+
                     " -p "+str(PORT))
            run(["pg_ctl","-D",str(cluster),"-o",options,
                 "-l",str(log),"-w","-t","15","start"],env,timeout=30)
            started=True
            inspect_settings(env)
            run(["createdb","-T","template0",SOURCE_DB],env)
            create_sql=("CREATE TABLE aec001_records (id INTEGER PRIMARY KEY, "
                        "value TEXT NOT NULL); "
                        "INSERT INTO aec001_records "
                        "SELECT i, 'fixture-' || i::text FROM generate_series(1,42) AS i;")
            run(["psql","-X","-q","-d",SOURCE_DB,
                 "-v","ON_ERROR_STOP=1","-c",create_sql],env)
            run(["pg_dump","-Fc","--no-owner","--no-acl",
                 "-f",str(dump),SOURCE_DB],env)
            if not dump.is_file() or dump.stat().st_size<=0:
                raise RuntimeError("fixture archive missing")
            run(["createdb","-T","template0",TARGET_DB],env)
            run(["pg_restore","--exit-on-error","--no-owner","--no-acl",
                 "-d",TARGET_DB,str(dump)],env)
            actual=run(["psql","-X","-q","-tA","-d",TARGET_DB,
                        "-v","ON_ERROR_STOP=1","-c",
                        "SELECT count(*)::text || '|' || sum(id)::text "
                        "FROM aec001_records"],env)
            if actual!=f"{N}|{EXPECTED_SUM}":
                raise RuntimeError("fixture record-count/checksum mismatch")
            return {
                "schema":SCHEMA,
                "status":"SYNTHETIC_LOGICAL_RESTORE_PASS",
                "observed_utc":datetime.now(timezone.utc).isoformat(),
                "postgres_version":run(["psql","--version"],env),
                "fixture_rows_expected":N,
                "fixture_rows_restored":N,
                "fixture_primary_key_sum_expected":EXPECTED_SUM,
                "fixture_primary_key_sum_observed":EXPECTED_SUM,
                "socket_only_listen_addresses_verified":True,
                "private_temporary_cluster":True,
                "fixture_dump_generated_in_temporary_cluster":True,
                "production_database_or_backup_accessed":False,
                "production_mutation":False,
                "real_backup_restore_tested":False,
                "real_backup_digest_verified":False,
                "customer_tenant_recovery_tested":False,
                "rpo_rto_approved":False,
                "pitr_tested":False,
            }
        finally:
            if started:
                try:
                    run(["pg_ctl","-D",str(cluster),"-m","immediate",
                         "-w","-t","10","stop"],env,timeout=18)
                except (OSError,RuntimeError,subprocess.TimeoutExpired):
                    raise RuntimeError("fixture server STOP not confirmed; manual review needed")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--synthetic-only",action="store_true",required=True)
    args=p.parse_args()
    try:
        root=private_audit_root(args.output)
        report=restore_fixture(root)
        write_private_output(args.output,json.dumps(report,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as e:
        print("SYNTHETIC_RESTORE_UNVERIFIED",type(e).__name__,file=sys.stderr)
        return 2
    print(report["status"],"rows",report["fixture_rows_restored"],
          "real_backup_restore_tested",report["real_backup_restore_tested"])
    return 0

if __name__=="__main__":
    raise SystemExit(main())
