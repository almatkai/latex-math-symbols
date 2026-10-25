# LateX Math Symbols — Native V2

Standalone offline Rust library and concrete compiled-in Tezbar beta adapter.
V1 remains beside it. The original 7,516-byte icon is retained exactly:
`e245364b6c13c1c70abf5a6e9255442477639e18526f857d086b5d611ca24191`.

The `index` command (“Search LateX Symbols”) searches 131 original records using
the actual V1 Fuse.js 6.6.2 options. Titles, aliases, case, escapes, descriptions,
examples, source order and all three variant groups are retained. Only base
records are shown/copyable, as in V1; variants are unused source data. The list
has one Copy to Clipboard action per result. Its examples are text accessories.
The actual source has no categories, preferences, arguments, favorites, history,
storage, forms, image thumbnails, TeX preview, paste or browser actions. No such
features are invented. No JS/Bun, process, network or conversion fallback runs in
the product. Node exists only for validation of the original executable source.

Original extension by **JeffersonDing**, own V1 port by almatkai. See [NOTICE](NOTICE),
[provenance](PROVENANCE.md) and exact [hash inventory](provenance.json).
The aggregate license is **MIT AND Apache-2.0**: upstream data/icon are covered by
the pinned MIT evidence; the translated Fuse algorithm and beta fixtures require
Apache-2.0. The own MIT-only package declaration does not cover away those notices.

Use [INTEGRATION.md](INTEGRATION.md) to vendor, register and rebuild the host.
JSON cannot install executable Rust. [VALIDATION.md](VALIDATION.md) records the
checks, stubs and limits; `scripts/validate.py` reproduces them. Cargo 1.85+ and
stable are checked. `scripts/materialize-checks.py` restores the nested test crates
from packaged templates, including from an extracted `.crate`, without the host.

Both macOS and Windows desktop verification remain **not-run**. Headless tests and
Windows GNU cross compilation do not verify UI, font rendering, real clipboard or
launcher integration. No real desktop effects were performed during this work.
