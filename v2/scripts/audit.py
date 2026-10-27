#!/usr/bin/env python3
"""Verify pinned bytes, locked npm SRI and Git visibility; never edits the host."""
from pathlib import Path
import base64, hashlib, io, json, subprocess, tarfile
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root/'provenance.json').read_text())
for entry in manifest['files']:
    p = root/entry['path']
    b = p.read_bytes()
    assert len(b) == entry['bytes'], p
    assert hashlib.sha256(b).hexdigest() == entry['sha256'], p
assert manifest['sourceCommit'] == 'a7429d60fca9a8943c61372a73fbedade03c30c4'
icon = (root/'assets/icon.png').read_bytes()
assert len(icon) == 7516
assert hashlib.sha256(icon).hexdigest() == 'e245364b6c13c1c70abf5a6e9255442477639e18526f857d086b5d611ca24191'
assert icon == (root/'fixtures/own/assets/icon.png').read_bytes() == (root/'fixtures/upstream/extensions/latex-math-symbols/assets/icon.png').read_bytes()
assert (root/'fixtures/own/src/commands.ts').read_bytes() == (root/'fixtures/upstream/extensions/latex-math-symbols/src/commands.ts').read_bytes()
lock = json.loads((root/'fixtures/own/package-lock.json').read_text())
pkg = lock['packages']['node_modules/fuse.js']
archive = (root/'fixtures/npm/fuse.js-6.6.2.tgz').read_bytes()
assert pkg['version'] == '6.6.2'
assert pkg['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode()
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    for name, local in [('dist/fuse.common.js','fuse.common.js'),('LICENSE','LICENSE'),('package.json','package.json')]:
        assert tar.extractfile('package/'+name).read() == (root/'libraries/fuse.js'/local).read_bytes()
    assert not any('NOTICE' in n.upper() for n in tar.getnames())
# A fresh extracted package need not be inside any Git repository.
repo = subprocess.run(['git','-C',str(root),'rev-parse','--show-toplevel'],capture_output=True,text=True)
if repo.returncode == 0 and Path(repo.stdout.strip()).resolve() == root.parent:
    top = root.parent
    names = subprocess.check_output(['git','-C',str(top),'ls-files','-z']).decode().split('\0')
    for name in filter(None,names):
        if name.startswith('v2/') or name == 'README.md': continue
        assert (top/name).read_bytes() == subprocess.check_output(['git','-C',str(top),'show',manifest['sourceCommit']+':'+name]), name
    baseline = (root/'fixtures/own/README.md').read_bytes()
    assert (top/'README.md').read_bytes() == baseline+b'\n\n[Native V2 (Rust) implementation and integration](v2/README.md)\n'
    assert not subprocess.check_output(['git','-C',str(top),'diff','--cached','--name-only']).strip(), 'Nothing may be staged by this task'
    paths = [str((root/e['path']).relative_to(top)) for e in manifest['files']]
    check = subprocess.run(['git','-C',str(top),'check-ignore','--no-index','--stdin'],input='\n'.join(paths)+'\n',capture_output=True,text=True)
    assert check.returncode in [0,1], check.stderr
    assert not check.stdout.strip(), 'Provenance files hidden by Git ignore: '+check.stdout
    visible = set(subprocess.check_output(['git','-C',str(top),'ls-files','--cached','--others','--exclude-standard','-z','v2']).decode().split('\0'))
    for path in paths: assert path in visible, 'Not Git-visible: '+path
    print('V1 tracked files byte-exact except README discovery link; index empty; every provenance path Git-visible.')
print(f"Pinned SHA256 inventory: {len(manifest['files'])} files; exact icon/data and locked npm tarball SRI passed.")
