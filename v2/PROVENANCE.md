# Provenance and licensing evidence

Own source: `https://github.com/almatkai/latex-math-symbols` at
`a7429d60fca9a8943c61372a73fbedade03c30c4`. A completed HTTPS filtered clone was
verified clean at that root, origin fetched, then `feat/native-v2-rust` created
from fresh origin/main. No additional clone/worktree was used. `fixtures/own/`
contains every original tracked file byte-for-byte, including README, TS source,
manifest, lock, license and icon. The root remains V1; only its README gains the
V2 discovery link. Audit scripts check tracked V1 files against the source commit
and assert that the Git index is empty.

Original Raycast pin: `6734d85992290066fd31a7f5bee3cca3d3545a1a`, path
`extensions/latex-math-symbols`, fetched directly via pinned raw GitHub URLs.
`fixtures/upstream/` includes that package.json, both source files, icon and the
repository LICENSE. Its author is JeffersonDing and it lists no contributors.
The own package names almatkai as author; this is a fork attribution difference,
so the original credit is retained in NOTICE and the V2 description. The schema
forbids a root author field; no such field is added.

The source `src/commands.ts` is byte-identical between own and pinned upstream:
SHA256 `1cd0d57a58a5b0703c1a5afff9e00132ecc1534a8306be6e41ce04738d1b271b`.
`data/commands.json` is produced by executing the unchanged own TS export with
`oracle/extract.ts` (validation only), not by parsing strings or inventing rows.
It retains all 131 records, original descriptions, examples, aliases, escapes,
case, newlines and three variant groups. Category/group labels are absent; source
order is the grouping/order. Variants are preserved as data and unused in UI,
matching actual source. No commented-out piecewise-function draft is activated.

`assets/icon.png`, own V1 icon and pinned upstream icon are all 7,516 bytes:
SHA256 `e245364b6c13c1c70abf5a6e9255442477639e18526f857d086b5d611ca24191`.
There are no preview images, amsmath binary files, fonts or other essential
rendering assets in this extension. Its examples are raw text list accessories.
The MIT license declaration is supported by the pinned Raycast repository MIT
license (Copyright 2021 Raycast); no separate asset/data license is present in the
inspected extension tree. This evidence is stated without inferring a distinct
amsmath license merely from the manifest description.

The own LICENSE claims MIT and Copyright 2026 almatkai but is stored with literal
backslash-n escapes. It is preserved exactly, and the valid original upstream MIT
text is also retained as LICENSE-MIT-UPSTREAM. No source license is rewritten.

The exact own package-lock resolves Fuse.js **6.6.2**. Its locked registry tarball
is retained at `fixtures/npm/fuse.js-6.6.2.tgz`; the audit checks its SHA512 SRI from
the original lock and exact archive members against `libraries/fuse.js/`.
`fuse.common.js`, package.json and LICENSE are byte-exact. Fuse is **Apache-2.0**,
not MIT. The package includes no NOTICE. Both its 2022 source header and its 2017
license attribution remain. `src/search.rs` prominently labels the modified Rust
translation. Original algorithm code executes only in validation, never in Rust
product runtime. The aggregate Cargo/source-package SPDX is therefore
**MIT AND Apache-2.0**. The own MIT-only package field cannot replace Apache's
requirements. NOTICE and both full license texts ship with the package.

Host reference: **fd300e276356587726566026f072563eb9c34cb1**, read only using
`git -C /Users/almat/Desktop/code/Tezbar\ APP/Tezbar show <pin>:<path>`.
`fixtures/beta/` captures unchanged docs, schema, common/SDK/NativeSessions,
dispatch/catalog/module, platform/clipboard, renderer/reconciler sources, package
and lock files, and the beta Apache-2.0 LICENSE. The Rust test fixtures use small
locked harness dependency graphs rather than rebuilding all Tauri dependencies
from beta Cargo.lock. The byte-exact beta Cargo.toml uses a .fixture suffix with its original sourcePath
to prevent Cargo from excluding that whole nested fixture tree. Harness templates
and complete Cargo.lock files ship so an
extracted Cargo package can materialize them offline. Renderer tests use beta's
locked **React 18.3.1** through validation-only dependency pins. Original own hooks
and source behavior are tested using actual beta React shim/reconciler AST
declarations and the actually locked Fuse library.

`provenance.json` inventories every fixture, vendored library, generated data,
icon and full license with length/SHA256. `scripts/audit.py` checks all inventory
entries and Git visibility, including files affected by ignore rules. `v2/.gitignore`
explicitly unignores the library subtree; the actual locked library is stored
outside a root-ignored dist directory. No dependency file is silently hidden.
No remote, ledger, host, profile or OS effect is changed by these checks.

XERJ used canonical-root prefix **ax-54e6325d2e37**, isolated state at
`~/.local/share/xerj/workspaces/ax-54e6325d2e37`. Initial indexing completed with
all 4 source code files covered (10 searchable files, 73 records; binary icon
junk/omitted). Search located FuseOptions in src/index.tsx. The bounded post-edit
update aborted on the service's frozen schema (“no frozen dataset accepts family
docs” for v2/Cargo.toml). No service restart, schema change, prefix change or shared
process termination was attempted. Thus new V2 XERJ coverage is incomplete;
current files, full inventories and exact exhaustive checks use rg/direct reads.
