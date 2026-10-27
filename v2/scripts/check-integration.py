#!/usr/bin/env python3
"""Apply the reference registration patch only to disposable pinned file fixtures."""
from pathlib import Path
import json, os, shutil, subprocess
root=Path(__file__).resolve().parents[1]
target=root/'.work/integration'
paths=['src-tauri/Cargo.toml','src-tauri/src/native_core/extensions/mod.rs',
       'src-tauri/src/native_core/extensions/v2_runtime.rs','src-tauri/src/native_core/extensions/v2_catalog.json']
for p in paths:
    dest=target/p;dest.parent.mkdir(parents=True,exist_ok=True)
    source = root/'fixtures/beta'/p
    if p.endswith('Cargo.toml'): source=source.with_name('Cargo.toml.fixture')
    shutil.copyfile(source,dest)
env={**os.environ,'GIT_CEILING_DIRECTORIES':str(target.parent)}
subprocess.run(['git','apply','--check',str(root/'integration/host-registration.patch')],cwd=target,env=env,check=True)
subprocess.run(['git','apply',str(root/'integration/host-registration.patch')],cwd=target,env=env,check=True)
original=json.loads((root/'fixtures/beta'/paths[3]).read_text())
changed=json.loads((target/paths[3]).read_text())
manifest=json.loads((root/'manifest.json').read_text())
assert changed == original+[manifest]
mod=(target/paths[1]).read_text()
assert '#[path = "../../../native-extensions/latex-math-symbols/adapter/v2_latex_math_symbols.rs"]\nmod v2_latex_math_symbols;' in mod
runtime=(target/paths[2]).read_text()
assert '"latex-math-symbols" => super::v2_latex_math_symbols::commands()' in runtime
assert 'super::v2_latex_math_symbols::handle(ctx, command, operation, payload, state).await' in runtime
assert '"latex-math-symbols" | "amphetamine"' in runtime
assert 'latex-math-symbols-native = { path = "native-extensions/latex-math-symbols" }' in (target/paths[0]).read_text()
print('Reference patch applies to pinned fixtures; catalog appends exactly the approved manifest and dispatch/path/command coverage agree. Host was not modified or built.')
