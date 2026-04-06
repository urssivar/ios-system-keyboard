# Nanai language (На̄ни хэсэни) — `gld`

Keyboard layout for the **Nanai language** (ISO 639-3: `gld`), Tungusic language family.

Layout author: **Vasily Kharitonov** (Василий Харитонов)

## Description

Nanai is a critically endangered Tungusic language spoken by the Nanai people along the Amur River in the Russian Far East and in northeastern China. It uses a Cyrillic alphabet based on Russian with one additional letter **Ӈ ӈ** (eng). In educational and linguistic publications, a **macron** (◌̄) is used to indicate long vowels.

This layout includes the full Nanai alphabet along with special characters used in linguistic and educational texts: ӡ, ᵸ, ʼ (modifier letter), і, ө, њ, and others.

## Files

| File | Description |
|------|-------------|
| `gld-3-rows.yaml` | Primary 3-row layout (iPhone + iPad 9" + iPad 12") |
| `gld-4-rows.yaml` | Extended 4-row layout (iPhone + iPad 9" + iPad 12") |
| `gld-longpress.yaml` | Full longpress mappings (for 3-row layout) |
| `gld-longpress-short.yaml` | Short longpress mappings (for 4-row layout) |
| `gld-macos.yaml` | macOS keyboard layout |

## Nanai iOS

Versions sorting for iPhone:

* gld-3-rows.yaml
* gld-4-rows.yaml

## Nanai macOS

Keyboard uses swapping/replacing less frequent Russian letters (ЦЩФЖ) to Nanai-specific letters (ӠᵸӇʼ), making original Russian letters accessible via `Option` (aka `ALT`).

## 3-row layout (iPhone)

```
Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г
-  И  О  А  Р  Л  М  Н  ᵸ  Ӈ
,  .  Я  Ю  Х  С  П  Т  Ч  К
```

### Longpress (3-row)

| Key | Longpress | | Key | Longpress |
|-----|-----------|---|-----|-----------|
| ё | ё̄ | | й | ы |
| е | е̄ | | в | ў |
| у | ӯ | | б | ъ |
| э | э̄ | | д | дʼ |
| и | ӣ | | ӡ | з |
| о | о̄ | | г | ж |
| а | а̄ | | н | нʼ |
| я | я̄ | | ᵸ | ԩ |
| ю | ю̄ | | х | ш |
| - | — | | с | щ |
| , | ? | | п | ф |
| . | ! | | т | ь |
| | | | ч | ц |
| | | | к | ' |

### iPad 9-inch (3-row)

```
Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г  Ӈ
-  И  О  А  Р  Л  М  Н  ᵸ  ʼ
,  .  Я  Ю  Х  С  П  Т  Ч  К
```

Extra keys vs iPhone: **Ӈ** and **ʼ** get their own keys instead of being longpress-only.

### iPad 12-inch (3-row)

```
]  Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г  Ӈ  [
-  И  О  А  Р  Л  М  Н  ᵸ  ʼ  Ъ
,  .  Я  Ю  Х  С  П  Т  Ч  К  /
```

Extra keys vs iPad 9": **Ъ** and punctuation brackets.

## 4-row layout (iPhone)

```
̄   І  Ө  Ы  Ь  Ш  Ф  ᵸ  З  ʼ     ← Head (extra row)
Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г
-  И  О  А  Р  Л  М  Н  Њ  Ӈ
,  .  Я  Ю  Х  С  П  Т  Ч  К
```

The head row provides direct access to characters that are only available via longpress in the 3-row layout: macron (◌̄), і, ө, ы, ь, ш, ф, ᵸ, з, ʼ. This frees up longpress slots in the 4-row layout for additional characters (г→ҕ, к→ӄ, ӡ→ǯ, х→ӽ, ӈ→ң, etc.).

### iPad 9-inch (4-row)

```
̄   І  Ө  Ы  Ь  Ш  Ф  ᵸ  З  ʼ  Ъ
Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г  Ӈ
-  И  О  А  Р  Л  М  Н  Њ  Ԩ
,  .  Я  Ю  Х  С  П  Т  Ч  К
```

### iPad 12-inch (4-row)

```
]  ̄   І  Ө  Ы  Ь  Ш  Ф  ᵸ  З  ʼ  Ъ  [
Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г  Ӈ  Ԩ
-  И  О  А  Р  Л  М  Н  Њ  Ж  Ц
,  .  Я  Ю  Х  С  П  Т  Ч  К  /
```

On iPad 12" almost all characters are available as direct keys — minimal longpress needed.

## macOS layout

Based on Russian ЙЦУКЕН with Nanai-specific replacements:

| Position | Russian | → Nanai | Available in alt |
|----------|---------|---------|-----------------|
| Row 1, pos 2 | ц | **ӡ** | ц |
| Row 1, pos 9 | щ | **ᵸ** | щ |
| Row 2, pos 1 | ф | **ӈ** | ф |
| Row 2, pos 10 | ж | **ʼ** | ж |

```
Default:
]  1  2  3  4  5  6  7  8  9  0  -  =
   Й  Ӡ  У  К  Е  Н  Г  Ш  ᵸ  З  Х  Ъ  Ё
   Ӈ  Ы  В  А  П  Р  О  Л  Д  ʼ  Э
   Я  Ч  С  М  И  Т  Ь  Б  Ю  /

Alt (⌥):
]  !  @  #  $  %  ^  &  *  {  }  –  »
   І  Ц  Ӯ  Ӄ  Е̄  Њ  Ҕ  ̄   Щ  Ǯ  Ӽ  Ң  Ё̄
   Ф  Ԩ  Ў  А̄  ©  ₽  О̄  ∂  ∆  Ж  Э̄
   Я̄  ≈  ≠  µ  Ю̄  ™  ~  ≤  ≥  "
```

**Alt layer logic:** replaced Russian letters (ц, щ, ф, ж) are at their original positions. Vowels with macron are at the same positions as their base vowels. Remaining positions contain additional Nanai characters (і, ө, њ, ҕ, ӄ, ǯ, ӽ, ң, ԩ, ў) and standard symbols.

**Cmd layer:** standard QWERTY for keyboard shortcuts.

## Layout design notes

- **Compact Cyrillic layout** — not based on the standard Russian ЙЦУКЕН; optimized for Nanai phonology
- **macOS layout** — based on Russian ЙЦУКЕН for familiarity with physical keyboards; Nanai-specific letters replace rarely-used Russian ones
- **Macron** (◌̄) — the key diacritic of Nanai, marks vowel length (а̄, о̄, э̄, ӣ, ӯ, ё̄, е̄, я̄, ю̄)
- **Ӡ ӡ** (U+04E0/U+04E1) — Nanai-specific Cyrillic letter (voiced alveolar affricate)
- **ᵸ** (U+1D78) — modifier letter
- **ʼ** (U+02BC) — modifier letter apostrophe, used in дʼ, нʼ
- **Ԩ ԩ** (U+0528/U+0529) — Cyrillic letter en with left hook

## System button labels (keyNames)

System button translations use Russian, consistent with the established bilingual practice among Nanai speakers. All Nanai speakers are fluent in Russian.


## Dead keys

**macOS:** The macron key (◌̄) in the Alt layer acts as a dead key — press Alt+Ш, then any vowel to produce a vowel with macron (e.g. Alt+Ш → а → а̄). The tilde key (◌̃) in Alt+Shift works the same way for nasalized vowels.

**iOS 4-row:** The macron key (◌̄) in the Head row acts as a dead key — tap it, then tap a vowel to get the long vowel.

**iOS 3-row:** No dead keys. Long vowels are accessed via longpress on the base vowel.

---

# Нанайский язык (На̄ни хэсэни) — `gld`

Раскладка клавиатуры для **нанайского языка** (ISO 639-3: `gld`), тунгусо-маньчжурская семья.

Автор раскладки: **Василий Харитонов**

## Описание

Нанайский язык — исчезающий тунгусо-маньчжурский язык нанайцев, проживающих по берегам Амура в Хабаровском крае и на северо-востоке Китая. Используется кириллический алфавит на основе русского с добавлением буквы **Ӈ ӈ**. В учебной и научной литературе для обозначения долгих гласных применяется **макрон** (◌̄).

## Нанайский iOS

Сортировка раскладок для iPhone:

* gld-3-rows.yaml
* gld-4-rows.yaml

## Нанайский macOS

Раскладка на основе ЙЦУКЕН. Менее частотные русские буквы (ЦЩФЖ) заменены на нанайские (ӠᵸӇʼ), оригиналы доступны через `Option` (aka `ALT`).

## Ссылки / References

- [Nanai writing system — Wikipedia](https://en.wikipedia.org/wiki/Nanai_language)
- [Нанайская письменность — Википедия](https://ru.wikipedia.org/wiki/Нанайская_письменность)
- [Нанайский язык — Википедия](https://ru.wikipedia.org/wiki/Нанайский_язык)
- [Nanai–Russian dictionary (online)](https://www.webonary.org/nanai/)
