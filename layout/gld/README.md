# Nanai language (На̄ни хэсэни) — `gld`

Keyboard layout for the **Nanai language** (ISO 639-3: `gld`), Tungusic language family.

Layout author: **Vasily Kharitonov** (Василий Харитонов)

## Description

Nanai is a critically endangered Tungusic language spoken by the Nanai people along the Amur River in the Russian Far East and in northeastern China. It uses a Cyrillic alphabet based on Russian with one additional letter **Ӈ ӈ** (eng). In educational and linguistic publications, a **macron** (◌̄) is used to indicate long vowels.

This layout includes the full Nanai alphabet along with special characters used in linguistic and educational texts: ӡ, ᵸ, ʼ (modifier letter), і, ө, њ, and others.

## Files

| File | Description |
|------|-------------|
| `gld-3-rows.yaml` | Primary 3-row layout for iPhone |
| `gld-4-rows.yaml` | Extended 4-row layout with an additional head row |
| `gld-longpress.yaml` | Full longpress mappings (for 3-row layout) |
| `gld-longpress-short.yaml` | Short longpress mappings (for 4-row layout) |

## 3-row layout

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

## 4-row layout

```
̄   І  Ө  Ы  Ь  Ш  Ф  ᵸ  З  ʼ     ← Head (extra row)
Ё  Е  У  Э  Й  В  Б  Д  Ӡ  Г
-  И  О  А  Р  Л  М  Н  Њ  Ӈ
,  .  Я  Ю  Х  С  П  Т  Ч  К
```

The head row provides direct access to characters that are only available via longpress in the 3-row layout: macron (◌̄), і, ө, ы, ь, ш, ф, ᵸ, з, ʼ. This frees up longpress slots in the 4-row layout for additional characters (г→ҕ, к→ӄ, ӡ→ǯ, х→ӽ, ӈ→ң, etc.).

## Layout design notes

- **Compact Cyrillic layout** — not based on the standard Russian ЙЦУКЕН; optimized for Nanai phonology
- **Macron** (◌̄) — the key diacritic of Nanai, marks vowel length (а̄, о̄, э̄, ӣ, ӯ, ё̄, е̄, я̄, ю̄)
- **Ӡ ӡ** (U+04E0/U+04E1) — Nanai-specific Cyrillic letter (voiced alveolar affricate)
- **ᵸ** (U+1D78) — modifier letter
- **ʼ** (U+02BC) — modifier letter apostrophe, used in дʼ, нʼ
- **Ԩ ԩ** (U+0528/U+0529) — Cyrillic letter en with left hook

## System button labels (keyNames)

System button translations use Russian, consistent with the established bilingual practice among Nanai speakers. All Nanai speakers are fluent in Russian.

---

# Нанайский язык (На̄ни хэсэни) — `gld`

Раскладка клавиатуры для **нанайского языка** (ISO 639-3: `gld`), тунгусо-маньчжурская семья.

Автор раскладки: **Василий Харитонов**

## Описание

Нанайский язык — исчезающий тунгусо-маньчжурский язык нанайцев, проживающих по берегам Амура в Хабаровском крае и на северо-востоке Китая. Используется кириллический алфавит на основе русского с добавлением буквы **Ӈ ӈ**. В учебной и научной литературе для обозначения долгих гласных применяется **макрон** (◌̄).

Раскладка включает все буквы нанайского алфавита, а также специфические символы, используемые в лингвистических и учебных текстах: ӡ, ᵸ, ʼ (модификатор), і, ө, њ и другие.

## Особенности раскладки

- **Компактная кириллическая раскладка** — не на основе стандартной русской ЙЦУКЕН, а оптимизирована для нанайского языка
- **Макрон** (◌̄) — ключевой диакритик нанайского, обозначает долготу гласных
- **Ӡ ӡ** (U+04E0/U+04E1) — специфическая нанайская буква
- **ᵸ** (U+1D78) — модификаторная буква
- **ʼ** (U+02BC) — модификатор (апостроф), используется в дʼ, нʼ
- **Ԩ ԩ** (U+0528/U+0529) — дополнительная буква кириллицы

## Ссылки / References

- [Nanai writing system — Wikipedia](https://en.wikipedia.org/wiki/Nanai_language)
- [Нанайская письменность — Википедия](https://ru.wikipedia.org/wiki/Нанайская_письменность)
- [Нанайский язык — Википедия](https://ru.wikipedia.org/wiki/Нанайский_язык)
- [Nanai–Russian dictionary (online)](https://www.webonary.org/nanai/)
