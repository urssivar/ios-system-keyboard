# Altai language (Алтай тил) — `alt`

Keyboard layout for the **Altai (Southern Altai) language** (ISO 639-3: `alt`), Turkic language family.

**Language codes**:

* **ISO 639-3**: `alt`
* **ISO 15924**: `Cyrl`

```
displayNames:
  en: Altai
  ru: Алтайский
  alt: Алтай
```

## Altai iOS

Versions sorting for iPhone:

* alt-3-rows.yaml
* alt-4-rows.yaml

## Altai macOS

Keyboard uses swapping/replacing less frequent Russian letters (ЦФЖЩ) to Altai-specific letters (ӰӦЈҤ), making original Russian letters accessible via `Option` (aka `ALT`).

## Details

### Алфавит / Alphabet

37 letters: 33 Russian + 4 Altai-specific (Ј, Ҥ, Ӧ, Ӱ).

```
'а' CYRILLIC SMALL LETTER A
'б' CYRILLIC SMALL LETTER BE
'в' CYRILLIC SMALL LETTER VE
'г' CYRILLIC SMALL LETTER GHE
'д' CYRILLIC SMALL LETTER DE
'е' CYRILLIC SMALL LETTER IE
'ё' CYRILLIC SMALL LETTER IO
'ж' CYRILLIC SMALL LETTER ZHE
'з' CYRILLIC SMALL LETTER ZE
'и' CYRILLIC SMALL LETTER I
'й' CYRILLIC SMALL LETTER SHORT I
'ј' CYRILLIC SMALL LETTER JE
'к' CYRILLIC SMALL LETTER KA
'л' CYRILLIC SMALL LETTER EL
'м' CYRILLIC SMALL LETTER EM
'н' CYRILLIC SMALL LETTER EN
'ҥ' CYRILLIC SMALL LETTER EN WITH DESCENDER
'о' CYRILLIC SMALL LETTER O
'ӧ' CYRILLIC SMALL LETTER O WITH DIAERESIS
'п' CYRILLIC SMALL LETTER PE
'р' CYRILLIC SMALL LETTER ER
'с' CYRILLIC SMALL LETTER ES
'т' CYRILLIC SMALL LETTER TE
'у' CYRILLIC SMALL LETTER U
'ӱ' CYRILLIC SMALL LETTER U WITH DIAERESIS
'ф' CYRILLIC SMALL LETTER EF
'х' CYRILLIC SMALL LETTER HA
'ц' CYRILLIC SMALL LETTER TSE
'ч' CYRILLIC SMALL LETTER CHE
'ш' CYRILLIC SMALL LETTER SHA
'щ' CYRILLIC SMALL LETTER SHCHA
'ъ' CYRILLIC SMALL LETTER HARD SIGN
'ы' CYRILLIC SMALL LETTER YERU
'ь' CYRILLIC SMALL LETTER SOFT SIGN
'э' CYRILLIC SMALL LETTER E
'ю' CYRILLIC SMALL LETTER YU
'я' CYRILLIC SMALL LETTER YA
```

### Названия клавиш / Key names

```
keyNames:
  space: Кеч
  return: Кир
  return-alts:
    search: Бедире
    go: Кӧч
    send: Аткар
    join: Кош
    route: Орык
    next: Анаң ары
    continue: Улалтар
    done: Белен
  emergency: Болуш (СОС)
  cancel: Токто
  undo: Jоголт
  redo: Катап
```

### Предпочтительный вариант / Preferred option

`alt-3-rows.yaml`:

```
й ӱ у к е н ҥ г ш з х
ӧ ы в а п р о л д ј э
  я ч с м и т ь б ю
```

`alt-longpress.yaml`:

```
ӱ: ц
е: ё
ҥ: щ
ш: щ
ӧ: ф
ј: ж
д: '-'
т: –
ь: ъ
```

### На основе русской раскладки / Based on Russian layout

`alt-4-rows.yaml`:

```
- – ? ё ӧ ҥ ӱ ј ъ , .
й ц у к е н г ш щ з х
ф ы в а п р о л д ж э
  я ч с м и т ь б ю
```

Head row contains Altai-specific letters and punctuation. The main 3 rows follow the standard Russian ЙЦУКЕН layout. Longpress is minimal (symbols only), since all letters are on the keyboard.

## Разработчик / Developer

* Али Кужугет / Ali Kuzhuget

## Ссылки / References

- [Altai language — Wikipedia](https://en.wikipedia.org/wiki/Altai_language)
- [Алтайский язык — Википедия](https://ru.wikipedia.org/wiki/Алтайский_язык)
- [Алтайская письменность — Википедия](https://ru.wikipedia.org/wiki/Алтайская_письменность)
- [Алфавит алтайского языка](https://altaitil.ru/docs/alfavit-sovremennogo-altajskogo-yazyka/)
