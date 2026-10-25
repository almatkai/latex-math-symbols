#!/usr/bin/env python3
"""Reproducible headless gates. Writes build outputs under v2/.work, v2/target and ignored oracle/node_modules.
Requires installed stable/1.85.0 toolchains + Windows GNU std targets, npm/Node.
Use --rust-only --offline for self-contained extracted-package Rust checks.
"""
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys
p = argparse.ArgumentParser()
p.add_argument('--rust-only',action='store_true')
p.add_argument('--offline',action='store_true')
p.add_argument('--skip-windows',action='store_true')
args = p.parse_args()
root = Path(__file__).resolve().parents[1]
os.chdir(root)
work = root/'.work'; work.mkdir(exist_ok=True)
def run(command, env=None):
    print('+ '+' '.join(map(str,command)),flush=True)
    subprocess.run(list(map(str,command)),check=True,env=env)
run([sys.executable,root/'scripts/audit.py'])
run([sys.executable,root/'scripts/check-integration.py'])
run([sys.executable,root/'scripts/materialize-checks.py'])
for format_chain in ['stable','1.85.0']:
    run(['cargo','+'+format_chain,'fmt','--check'])
    run(['rustfmt','+'+format_chain,'--edition','2021','--config','skip_children=true','--check',
         'adapter/v2_latex_math_symbols.rs','checks/adapter-tests.rs','checks/sdk.lib.rs.in',
         'checks/beta.lib.rs.in','checks/runner.lib.rs.in','checks/dump.rs.in'])
crates = [root/'Cargo.toml',work/'checks/sdk/Cargo.toml',work/'checks/runner/Cargo.toml']
for toolchain in ['stable','1.85.0']:
    env = {**os.environ,'CARGO_TARGET_DIR':str(work/f'cargo-{toolchain}')}
    tail = ['--locked'] + (['--offline'] if args.offline else [])
    for crate in crates:
        run(['cargo','+'+toolchain,'test','--manifest-path',crate,*tail],env)
        run(['cargo','+'+toolchain,'clippy','--manifest-path',crate,*tail,'--all-targets','--','-D','warnings'],env)
    # The unchanged NativeSessions' own test module targets unrelated ExtensionsCore.
    # It compiles as the real production dependency; our local adapter is all-targets above.
    run(['cargo','+'+toolchain,'clippy','--manifest-path',work/'checks/beta/Cargo.toml',*tail,'--lib','--','-D','warnings'],env)
    if not args.skip_windows:
        for crate in crates:
            for gate in ['check','clippy']:
                cmd=['cargo','+'+toolchain,gate,'--manifest-path',crate,*tail,'--all-targets','--target','x86_64-pc-windows-gnu']
                if gate == 'clippy':cmd+=['--','-D','warnings']
                run(cmd,env)
    run(['cargo','+'+toolchain,'build','--example','search',*tail],env)
    run(['cargo','+'+toolchain,'build','--manifest-path',work/'checks/runner/Cargo.toml','--example','dump',*tail],env)
    if not args.rust_only:
        own = work/'v1'
        own.mkdir(exist_ok=True)
        for name in ['package.json','package-lock.json','tsconfig.json','raycast-env.d.ts']:
            shutil.copyfile(root/'fixtures/own'/name,own/name)
        for name in ['src','test']:
            shutil.copytree(root/'fixtures/own'/name,own/name,dirs_exist_ok=True)
        if toolchain == 'stable':
            run(['npm','ci','--prefix',own,'--ignore-scripts','--no-audit','--no-fund'])
            run(['npm','ci','--prefix',root/'oracle','--ignore-scripts','--no-audit','--no-fund'])
            run(['npm','test','--prefix',own])
            run(['npm','run','typecheck','--prefix',own])
        oracle_env={**env,'LATEX_ENGINE_BIN':str(work/f'cargo-{toolchain}/debug/examples/search'),'LATEX_ADAPTER_BIN':str(work/f'cargo-{toolchain}/debug/examples/dump')}
        run(['node','oracle/parity.mjs'],oracle_env)
        shutil.copyfile(work/'oracle/summary.json',work/f'oracle/summary-{toolchain}.json')
if not args.rust_only:
    run(['node','oracle/renderer.mjs'])
    run(['node','oracle/schema.mjs'])
run([sys.executable,root/'scripts/audit.py'])
print('All requested headless gates passed. Real host/desktop QA remains not-run.',flush=True)
