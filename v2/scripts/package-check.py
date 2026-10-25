#!/usr/bin/env python3
"""Package + extracted offline checks; extraction stays inside v2/.work."""
from pathlib import Path
import os, subprocess, sys, tarfile
root=Path(__file__).resolve().parents[1]
os.chdir(root)
def run(c): subprocess.run(c,check=True)
run(['cargo','+stable','package','--locked','--offline','--allow-dirty'])
archive=root/'target/package/latex-math-symbols-native-0.1.0.crate'
with tarfile.open(archive) as tar:
    names=tar.getnames()
    assert not any('/node_modules/' in n or '/.work/' in n for n in names)
    for name in ['Cargo.lock','adapter/v2_latex_math_symbols.rs','libraries/fuse.js/fuse.common.js','checks/runner.Cargo.toml.in','checks/runner.Cargo.lock.in','scripts/materialize-checks.py','fixtures/own/src/index.tsx']:
        assert f'latex-math-symbols-native-0.1.0/{name}' in names,name
    dest=root/'.work/extracted';dest.mkdir(parents=True,exist_ok=True)
    assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names)
    tar.extractall(dest)
extracted=dest/'latex-math-symbols-native-0.1.0'
run([sys.executable,str(extracted/'scripts/validate.py'),'--rust-only','--offline'])
print(f'Package contains {len(names)} paths; extracted offline stable/MSRV/Windows contracts passed.')
