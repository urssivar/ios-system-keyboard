# Kaitag (xdq) — iOS/macOS Keyboard

**Language**: Kaitag (_Хайдаҡӏла_)  
**ISO 639-3**: `xdq`  
**Script**: Cyrillic, v1.2 (May 2026)

**Script spec**: [Urssivar/Script](https://github.com/urssivar/script)

## Script Overview

The modern Kaitag alphabet consists of 30 unique characters: 24 Russian letters plus 6 extended Cyrillic — **ӕ** /æ/, **ғ** /ʁ/, **ҡ** /q/, **ҳ** /x/, **һ** /h/, **ӏ** /ʔ/ — totalling 42 letters when digraphs for geminates and ejectives are counted.

Nine Russian letters are absent from the core Kaitag alphabet: **ё щ ф ъ ы ь э ю я**. Six are replaced by extended Cyrillic characters; but any Russian letters appearing in loanwords remain accessible via long-press.

All layouts are built on the standard Russian ЙЦУКЕН to minimize disruption for existing keyboard users.

**Language switcher**: `ҡғҳ` (from _ҡҡуғадеҳ_ — "happiness")

## iOS

Two layout variants are available.

### 3-Row (`xdq-3-rows`)

The default variant. Six positions of excluded Russian letters are replaced by Kaitag-specific ones, placed roughly by frequency:

```text
й ц у к е н г ш ҡ з х
ҳ ғ в а п р о л д ж ӏ
   ӕ ч с м и т һ б
```

Excluded Russian letters and stressed vowels are accessible via long-press:

- `у` → `ю` `у́`
- `е` → `э` `е́` `ё`
- `ш` → `щ`
- `п` → `ф`
- `а` → `а́`
- `о` → `о́`
- `ӏ` → `ъ`
- `ӕ` → `я` `ӕ́`
- `и` → `ы` `и́`
- `һ` → `ь`

### 4-Row (`xdq-4-rows`)

An alternative for users who prefer not to long-press for Russian letters. Rows 2–4 are identical to the standard Russian ЙЦУКЕН; all Kaitag-specific characters appear in a dedicated top row:

```text
, ! ? ҳ ғ ӏ һ ҡ ӕ — .
й ц у к е н г ш щ з х
ф ы в а п р о л д ж э
  я ч с м и т ь б ю
```

Stressed vowels are accessible via long-press:

- `ӕ` → `ӕ́`
- `у` → `у́`
- `е` → `е́` `ё`
- `ы` → `ы́`
- `а` → `а́`
- `о` → `о́`
- `э` → `э́`
- `я` → `я́`
- `и` → `и́`
- `ь` → `ъ`
- `ю` → `ю́`

### iPad

Both variants share the same iPad layouts.

The **9-inch iPad** adds `ю` and `ъ` as direct keys in the third row, taking advantage of the extra width.

The **12-inch iPad** uses a full physical-keyboard-style layout with a number row. The third row is expanded to recover the most frequent displaced Russian letters: `я ы ь`.

## macOS

The layout follows ЙЦУКЕН with Kaitag substitutions in place. Displaced Russian letters are accessible via the `Option` (`⌥`) layer:

- `⌥` `ҡ` = `щ`
- `⌥` `ҳ` = `ф`
- `⌥` `ғ` = `ы`
- `⌥` `ӏ` = `ю`
- `⌥` `ӕ` = `я`
- `⌥` `һ` = `ь`

The alt layer also provides common typographic symbols: `№ ~ © ® ° · § « » – — ™ ∞ µ ≈ ≠ ≤ ≥ ‹ › ‚ „`.

A dead key `´` is available for stressed vowels: `⌥` `´` + `а` = `а́`.

## Contact

Magomed Magomedov, <alkaitagi@outlook.com>
