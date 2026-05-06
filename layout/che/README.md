# Chechen (che) native iOS/macOS keyboards

## Language

Chechen (Нохчийн, Noxçiyŋ, [ˈnɔxt͡ʃĩː])[a] is a Northeast Caucasian language spoken primarily by the Chechen people, who are native to the Chechen Republic and neighboring regions. With approximately 1.8 million speakers, it is also used by Chechen diaspora communities across Russia and around the world.

Self-name:
**Нохчийн мотт / Noxçiyŋ mott**

Language codes:
- ISO 639-1: `ce`
- ISO 639-2: `che`
- ISO 639-3: `che`

## Project

This Chechen keyboard work is part of a broader effort to define a practical and consistent Chechen keyboard standard for Apple platforms.

Project website:
- https://ios.chechenlanguage.dev

Chechen corpus used for frequency-based layout decisions:
- https://corpora.dosham.info

## Chechen iOS

Two iOS layouts are currently provided:

- `che-3-rows.yaml` — primary layout
- `che-3-rows-ycuken.yaml` — Russian-based ЙЦУКЕН variant

The primary layout is based on frequency analysis of the Chechen corpus at https://corpora.dosham.info.

The Russian-based ЙЦУКЕН variant is intended for users who prefer minimal deviation from the familiar Russian layout.

## Chechen macOS

Two macOS layouts are provided:

- `che-macos.yaml` — primary
- `che-macos-pc.yaml` — PC

Both macOS layouts preserve the familiar Russian ЙЦУКЕН structure as closely as possible. On the visible layer, the only change is the replacement of `Щ/щ` with `Ӏ/ӏ`.

On macOS, `Ъ` is already directly available on the visible layer, so no broader structural changes are necessary. This allows the layout to preserve the familiar ЙЦУКЕН structure more faithfully than on mobile keyboards.

This is especially important on physical keyboards. Unlike mobile keyboards, hardware keycaps cannot visually reflect system-level remapping. Larger visible changes would make typing more difficult for ordinary users because the legends printed on the keyboard would no longer match the characters produced by the system layout.

## Long-press and Chechen-specific forms

Chechen-specific digraphs and related forms are accessed through parent-key long-press mappings.

Examples:
- `а → аь`
- `о → оь`
- `г → гӏ`
- `к → кӏ кх къ`
- `т → тӏ`
- `х → хӏ хь`
- `ц → цӏ`
- `ч → чӏ`

The Chechen palochka must use the correct Unicode forms:
- lowercase: `ӏ`
- uppercase: `Ӏ`
