"""Minimal fontTools WOFF2 compressor adapter for local Homebrew Brotli CLI 1.2.1.
Build-only dependency; use no network service, no system/global Python package install.
Requires /opt/homebrew/bin/brotli (or brotli on PATH). RFC 7932 Brotli bitstream.
"""
import subprocess,shutil
MODE_GENERIC=0
MODE_TEXT=1
MODE_FONT=2
class error(Exception):pass
def call(data,decompress=False):
    exe=shutil.which('brotli')
    if not exe:raise error('brotli CLI not installed')
    opts=[exe,'-d','-c'] if decompress else [exe,'-c','--quality=11']
    p=subprocess.run(opts,input=data,capture_output=True)
    if p.returncode:raise error(p.stderr.decode(errors='replace'))
    return p.stdout
def compress(data,mode=MODE_GENERIC,**kwargs):
    if mode not in (MODE_GENERIC,MODE_TEXT,MODE_FONT):raise ValueError(mode)
    return call(data)
def decompress(data):return call(data,True)
