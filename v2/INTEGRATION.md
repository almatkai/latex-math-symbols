# Compiled host integration (not applied)

Baseline: Tezbar beta `fd300e276356587726566026f072563eb9c34cb1`. The existing
`fix/deep-search-state` host checkout is outside this task and was not modified.
The production adapter imports the unchanged host CoreContext and sibling v2_sdk.
It is compiled and exercised with byte-exact pinned common/SDK/NativeSessions
fixtures. Registry, installation metadata and Tauri AppHandle/Emitter are labelled
test stubs; these tests do not certify a complete host build or installer.

1. Vendor the contents of `v2/` (excluding `.work/`, `target/`, `node_modules/`) at
   `src-tauri/native-extensions/latex-math-symbols/`. Keep Cargo.lock, src/, data/,
   adapter/, exact icon and notices there. This is the stable vendoring path.
2. In `src-tauri/Cargo.toml`, add
   `latex-math-symbols-native = { path = "native-extensions/latex-math-symbols" }`.
   The adapter uses serde derive and serde_json already present in beta.
3. In `src-tauri/src/native_core/extensions/mod.rs`, register:

   ```rust
   #[path = "../../../native-extensions/latex-math-symbols/adapter/v2_latex_math_symbols.rs"]
   mod v2_latex_math_symbols;
   ```

   This path is relative to the extensions directory; the adapter uses the host's
   `crate::native_core::extensions::v2_sdk` and common, not a substitute SDK.
4. Extend `v2_runtime.rs` slug matching to `latex-math-symbols` for bare,
   `raycast.latex-math-symbols`, and `com.tezbar.native.latex-math-symbols` IDs.
   Add `commands` -> `v2_latex_math_symbols::commands()` and `handle` ->
   `v2_latex_math_symbols::handle(ctx, command, operation, payload, state).await`.
   These must all agree on `index`. Append `manifest.json` to the V2 catalog.
   `integration/host-registration.patch` contains concrete additions against the
   pinned beta (review/rebase it before applying to a different host revision).
   The pinned catalog has unrelated root `author` fields that conflict with its
   schema; this new manifest has no root author and passes the full schema.
5. Copy `assets/icon.png` byte-for-byte to the actual renderer path
   `src/renderer/public/extensions/icons/latex-math-symbols.png` (7,516 bytes,
   SHA256 `e245364b6c13c1c70abf5a6e9255442477639e18526f857d086b5d611ca24191`).
   Manifest icon/iconUrl is `/extensions/icons/latex-math-symbols.png`. Do not
   substitute a generated image or remove V1.
6. Rebuild/relink the Rust host and renderer with the project's normal pinned
   dependency setup. Inspect compiled CLI/catalog coverage on macOS and Windows:
   exactly one added command `index`, canonical ID, replaces ID, runtime Rust,
   independent not-run verification entries. Only then install the compiled
   NativeV2 package using the host installer. A marker or JSON edit alone cannot
   make the command executable. Test fallback to unchanged V1 separately.

The reference registration is **not applied**, and host rebuild, installation,
full CLI/catalog coverage and real macOS/Windows QA remain not-run. The supplied
contract test asserts manifest/dispatch command parity in the labelled stub.

## Payloads, view and effects

Operations are `extension:run-command`, `extension:invoke-action`,
`extension:search-text-changed`, `extension:refresh-session`, `extension:load-more`,
`extension:dispose-session`. The host attaches sessionId and installed
`payload.preferences`. This command has no arguments/preferences. If supplied,
`argumentValues` must be an empty object, preferences an object, formValues an
object. No unknown legacy storage migration is performed.

The adapter returns the real List/List.Item parser props, string row IDs,
accessories, ordered actionIds, `filtering:false`, `__hasServerSearch:true` and
searchText. All 131 results fit; no pagination/truncation is used. Refresh and
load-more return unchanged without issuing new IDs or modifying cloned state.
The source's case-insensitive fuzzy search uses title/subtitle only, not example
or variants. It preserves whitespace (empty query alone bypasses Fuse). UTF-16
queries above 4,096 units return an explicit resource error, without changing
committed state. Parser/renderer selection and keyboard Enter routes are tested;
no custom hotkeys are advertised. The renderer truncates long/multiline text
accessories visually according to its existing CSS; their data/copy text stay exact.
No mathematical font/TeX renderer is invoked or claimed. No essential image preview
is lost: there is no such renderer, thumbnail asset or preview in the actual source.

Only `v2_sdk::copy(ctx, canonical_record.command)` -> `clipboard:write [text]` is
used. That beta route genuinely returns an object acknowledgement. Success
requires object `ok:true`, error absent/null, success absent/true, and a string
message when supplied. Null/boolean/malformed/contradictory responses and transport
errors are rejected with sanitized public messages. Before await, the selected
record and Pending stage are checkpointed. Acknowledged is checkpointed before
render. Failed or cancelled copies remain uncertain and require a newly visible
“Retry Copy to Clipboard” action; repeated old IDs cannot silently replay a write.
Action text never comes from event content/formValues. Session bindings are opaque,
process-nonce/monotonic-generation scoped; discarded staged search IDs never revive.

The copied result is shown as the supported native view message. No fake HUD,
toast or pop-to-root SDK call is used. The actual beta CopyToClipboard handler
copies without hiding/pasting, which is preserved. In beta, `window:hide []`
hides and returns null, so any future strict-ack use would need a host fix returning
an object `{ok:true}`; this adapter never calls or normalizes that route. It also
never reads clipboard/selection, opens URLs, modifies focus or sends paste keys.
If paste is added later, beta `core:platform:paste-text [text]` already writes,
hides/restores focus, waits and pastes; chaining another paste would duplicate it.

There is no source persistence or Form/Back draft model to port. The real SDK
atomic storage/common tests are retained and run (unknown keys, corruption,
concurrent updates); this adapter never reads/writes storage or the profile.
