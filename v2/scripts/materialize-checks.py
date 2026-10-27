#!/usr/bin/env python3
"""Self-contained test crates (Cargo omits nested manifests from packages).
Only v2/.work/checks is written. No host paths or desktop effects are used.
"""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
work = root / '.work/checks'
for name in ['sdk', 'beta', 'runner']:
    dst = work / name
    (dst / 'src').mkdir(parents=True, exist_ok=True)
    shutil.copyfile(root / f'checks/{name}.Cargo.toml.in', dst / 'Cargo.toml')
    if name != 'runner':
        shutil.copyfile(root / f'checks/{name}.lib.rs.in', dst / 'src/lib.rs')
    else:
        shutil.copyfile(root / 'checks/runner.lib.rs.in', dst / 'src/lib.rs')
        (dst / 'examples').mkdir(exist_ok=True)
        shutil.copyfile(root / 'checks/dump.rs.in', dst / 'examples/dump.rs')
        (dst / 'tests').mkdir(exist_ok=True)
        shutil.copyfile(root / 'checks/adapter-tests.rs', dst / 'tests/contracts.rs')
    lock = root / f'checks/{name}.Cargo.lock.in'
    if lock.exists(): shutil.copyfile(lock, dst / 'Cargo.lock')
    if name == 'sdk':
        files = {'common.rs':'common.rs', 'extensions/v2_sdk.rs':'extensions/v2_sdk.rs'}
    elif name == 'beta':
        files = {'extensions/native.rs':'extensions/native.rs'}
    else: files = {}
    for source, target in files.items():
        path = dst / 'src/native_core' / target
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / 'fixtures/beta/src-tauri/src/native_core' / source, path)
    if name in ['beta', 'runner']:
        (dst / 'src/native_core/extensions').mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / 'adapter/v2_latex_math_symbols.rs', dst / 'src/native_core/extensions/v2_latex_math_symbols.rs')
print('Materialized SDK, NativeSessions and adapter contracts in v2/.work/checks')
