# Avar (ava) native iOS/macOS keyboards

## Avar iOS

Two Avar keyboard layouts are provided:
 * ava-3-rows (default)
 * ava-4-rows

These layouts support different typing preferences:
 * The 3-row layout is more compact and closely follows the geometry of the standard Russian keyboard.
 * The 4-row layout places all Avar letters directly on the primary layer without letter replacement.

Long-press

Long-press is used to access:
 * stress marks
 * secondary symbols

### iPhone Versions

The layouts are provided in the following files:
 * ava-3-rows.yaml
 * ava-4-rows.yaml

### iPad Versions

Two layouts are available for iPad:
 * 3-row layout
 * 4-row layout

The 3-row layout is recommended as the default, as it is closer to the geometry of the standard Russian keyboard and provides a more familiar typing experience.

## Avar macOS

Avar-specific letters (including ӏ) – 43 – are placed directly on the primary layer using standard ANSI keyboard geometry.

No letter replacement is used.

Stress marks are available via dead keys.

The Option (ALT) layer contains extended system symbols, similar to other macOS Cyrillic layouts.


## Avar keyNames

Key names are translated into Avar using natural interface phrasing.

### Stress marks

Stress marks (combining acute accent U+0301) are optional and are primarily used for:
 * educational purposes
 * disambiguation

They should be ignored during:
 * autocorrection
 * search
 * tokenization
 * frequency analysis

#### Recommended preprocessing:

For linguistic processing (such as search, tokenization, or frequency analysis), it is recommended to:
 1. apply Unicode NFD normalization
 2. remove combining diacritical marks

This ensures that words are processed identically regardless of whether stress marks are present.
