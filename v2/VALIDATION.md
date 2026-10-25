# Executed validation and honest limits

Source SHA `a7429d60fca9a8943c61372a73fbedade03c30c4`; branch
`feat/native-v2-rust`. Headless execution on macOS arm64. Tool versions and
machine-readable oracle results are in `validation/`. Nothing was staged,
committed or pushed, and no PR was created. The clone is retained for parent review.

## Passing gates

- Stable Rust **1.98.0** and MSRV **1.85.0**: formatting; **4 engine + 13 adapter/
  lifecycle + 5 unchanged beta common/SDK tests = 22 Rust tests per toolchain**.
  Strict `clippy --all-targets -- -D warnings` for the engine, local concrete
  adapter/harness and SDK/common fixture. The unchanged NativeSessions compiles
  as the real dependency and is also linted with `--lib -D warnings`.
- **Windows GNU x86_64** `check --all-targets` and strict all-target Clippy for
  engine, adapter harness and SDK/common with **both stable and 1.85.0**.
  These are cross-compilation checks, not execution or desktop verification.
- The actual own TS data export and component execute with exact beta
  React-hook/reconciliation/action AST declarations and the locked Fuse.js
  **6.6.2** library. **2,492 deterministic queries**, **37,745 exact records in
  exact order**, **37,614 bit-exact scores** on each checked macOS toolchain.
  The gate now requires exact score equality, with zero tolerance/differences.
  The corpus spans every command/example/description, upper case, aliases,
  edits/prefixes, whitespace, escaped/multiline matrices, 31/32/33+ chunk lengths,
  Unicode UTF-16 and deterministic fuzzy inputs through the 4,096-unit bound.
- **131 actual own TS Copy actions** execute through beta registerAction with
  effects recorded only; every Rust production-adapter copy also checks all
  **131 canonical records**, including escapes/newlines. No expected algorithm
  or expected action text is reimplemented in handwritten JavaScript.
- Real pinned beta List parser and ListRuntime execute under **React 18.3.1**,
  beta's locked renderer version. Tests cover text accessories, ordered IDs,
  no double filtering, click/Enter/ArrowDown/action-panel selection, search
  callback, result reconciliation and empty-list Enter. The presentational UI
  primitives/Markdown/details/color converter boundaries are labelled stubs.
  AST helper exports are appended in memory; fixture files remain byte-exact.
- Full pinned **draft 2020-12** schema validated with Ajv 2020: **1 positive +
  22 negative manifests**, including root author rejection. Manifest/catalog/
  dispatch command parity is asserted. The concrete integration patch applies
  to a disposable copy of the pinned file fixtures and appends exactly the new
  manifest; it does not touch the real host.
- Every own and beta fixture independently rechecked with `git show <pin>:<path>`.
  **66 provenance files** pass exact byte length/SHA256 and Git visibility audit.
  Original icon: 7,516 bytes and exact prescribed SHA256. Own/upstream symbol
  source bytes match. Locked npm tarball SHA512 SRI and exact Fuse archive members
  match; license texts/notices are retained. No archive NOTICE was omitted.
- Disposable V1 fixture: `npm ci --ignore-scripts`, **1 original test**, and
  `tsc --noEmit` all pass. Root package/source/lock/license/icon remain unchanged;
  root README contains only the requested V2 discovery addition.
- Cargo package/verification and extracted offline checks: all fixtures, source,
  locks, adapter, data, icon, notices, oracle and test templates are present;
  node_modules and build/work caches are excluded. Extracted package materializes
  self-contained Rust test crates and runs stable/MSRV tests, strict Clippy and
  both Windows GNU gates without a host checkout or JS runtime.

The original beta `native_tests.rs` is preserved as evidence but its unrelated
perplexity/ExtensionsCore tests are not claimed as this extension's tests. The
unchanged `NativeSessions` production body is compiled and exercised directly by
our 13 contract tests. Tauri AppHandle/Emitter, package installation/registry and
runtime registration are explicit test stubs. The actual common/SDK source tests
run unchanged, including atomic persistence, unknown-key preservation, malformed
JSON, concurrent writes and propagation of routed failures. This extension itself
has no persistent settings, history or forms, so no synthetic data migration,
typed source settings or draft features are added.

The lifecycle/effect suite checks stale/forged/cross-session bindings, malformed
payloads without consumption, discarded staged-search generations, unchanged
refresh clones, session capacity, disposal, uninstall, concurrent searches,
serialized duplicate actions, in-flight refresh/disposal cancellation, pre-await
Pending and post-ack Acknowledged checkpoints, sanitized failures, all strict ack
negative cases, explicit uncertainty recovery, and no automatic duplicate write.
All OS effects are recording/blocking/error stubs. No clipboard, selection,
window, browser, focus or paste operation reaches the real desktop.

## Reproduce

From `v2/`, with stable and 1.85.0 toolchains and Windows GNU standard libraries
installed:

```sh
python3 scripts/validate.py --offline
python3 scripts/package-check.py
```

`--offline` locks Cargo registry access; npm validation requires the exact locked
packages already cached or network access on first setup. Product runtime uses
neither npm nor Node. Rust checks on a previously extracted Cargo package can run
with `python3 scripts/validate.py --rust-only --offline` and need only pre-cached
Cargo dependencies plus installed toolchains/targets. “Offline extracted checks”
is not a claim that the archive bundles Rust toolchains or the entire crates.io
registry. Manifests and locks for nested test crates use `.in` templates because
Cargo excludes nested packages. The pinned beta Cargo.toml fixture likewise uses
`.fixture` suffix, retaining its exact original bytes and original sourcePath.

Raw local gate transcripts remain in ignored `.work/validation.txt` and
`.work/package-validation.txt` for parent review. No npm lifecycle scripts run.
`oracle/extract.ts` can regenerate the data export with the actually locked tsx;
the executable parity gate independently compares it with the untouched TS data.

## Not run / limitations

Host registration, host rebuild/link, full real installer/CLI catalog coverage,
real macOS and Windows desktop UI, font/accessory appearance, clipboard and focus
QA remain **not-run**. Neither platform verification is marked pass. The source
has no TeX/image preview or paste feature; none is claimed. The renderer's existing
CSS truncates long text visually without changing data/copy bytes. No Grid, Detail,
Form or draft callbacks are emitted because the actual command uses none.

Search above 4,096 UTF-16 units is an explicit resource error, not truncation.
No guarantee is asserted for every possible Unicode query beyond the broad
executed oracle corpus. Exact floating scores are demonstrated for these checked
macOS toolchains; Windows execution is still unverified. No private router error
strings reach user-facing failures.

Initial XERJ source indexing covered all four code files. Its post-edit update
failed on frozen dataset schema; new V2 search coverage is incomplete. No shared
service/schema was changed. `rg`, current source reads and exact exhaustive
file/hash/visibility checks supplied the final coverage instead.
