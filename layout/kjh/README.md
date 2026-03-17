# Хакасские раскладки / Khakas layouts

**Язык / Language**:
```
en: Khakas
ru: Хакасский
kjh: Хакас
 ```

**Language codes**:

- **ISO 639-3**: `kjh`
- **ISO 15924**: `Cyrl`
- **Glottocode**: `khak1248`

### Алфавит / Alphabet

`а б в г ғ д е ё ж з и і й к л м н ң о ӧ п р с т у ӱ ф х ц ч ҷ ш щ ъ ы ь э ю я`

```
'а' CYRILLIC SMALL LETTER A
'б' CYRILLIC SMALL LETTER BE
'в' CYRILLIC SMALL LETTER VE
'г' CYRILLIC SMALL LETTER GHE
'ғ' CYRILLIC SMALL LETTER GHE WITH STROKE
'д' CYRILLIC SMALL LETTER DE
'е' CYRILLIC SMALL LETTER IE
'ё' CYRILLIC SMALL LETTER IO
'ж' CYRILLIC SMALL LETTER ZHE
'з' CYRILLIC SMALL LETTER ZE
'и' CYRILLIC SMALL LETTER I
'і' CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
'й' CYRILLIC SMALL LETTER SHORT I
'к' CYRILLIC SMALL LETTER KA
'л' CYRILLIC SMALL LETTER EL
'м' CYRILLIC SMALL LETTER EM
'н' CYRILLIC SMALL LETTER EN
'ң' CYRILLIC SMALL LETTER EN WITH DESCENDER
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
'ҷ' CYRILLIC SMALL LETTER CHE WITH DESCENDER
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
  space: Ара # Пробел
  return: Кир # Ввод
  return-alts:
    search: Тап # Найти
    go: Пар # Перейти
    send: Ыс # Отправить
    join: Хозыл # Подкл.
    continue: Узарат # Продолжить
    done: Тимде # Готово
    next: Пазағы # Далее
    route: Чол # Маршрут
  emergency: SOS # SOS
  cancel: Тохтат # Отменить
  undo: Нандыра # Не применять
  redo: Хатап # Повторить
```

### Предпочтительный вариант / Preferred option

`kjh-4-rows.yaml`:

```
    ҷ ӱ і   ң ӧ ғ 
й ц у к е н г ш щ з х
ф ы в а п р о л д ж э
  я ч с м и т ь б ю
```

### По частоте букв / Based on letter frequency

`kjh-3-rows.yaml`:

```
й ҷ у к е н г ш ң з х
ғ ы в а п р о л д ж ӧ
  я ч с м и т і б ӱ
```

`kjh-3-rows-longpress.yaml`:

```
ҷ: ц
ӱ: ю
ӧ: э
і: 'ь ъ'
ш: щ
в: ф
е: ё
```

### На основе русской раскладки / Based on Russian layout

`kjh-3-rows-rus.yaml`:

```
й ц у к е н г ш щ з х
ф ы в а п р о л д ж э
  я ч с м и т ь б ю
```

`kjh-3-rows-rus-longpress.yaml`:

```
и: і
г: ғ
н: ң
ч: ҷ
о: ӧ
у: ӱ
е: ё
ь: ъ
```

### Яндекс Клавиатура - слишком узкие клавиши / Yandex Keyboard - too narrow keys

```
й ц у к е ғ ң н г ш щ з х
ф ы в а п ӧ ӱ р о л д ж э
  я ч с м и ҷ і т ь б ю
```

## Разработчик / Developer

- Василий Адешкин / Vasily Adeshkin, научный сотрудник ХакНИИЯЛИ / researcher at KhRILLH — почта / email:
  translate.khakas@gmail.com
