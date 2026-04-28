# Language Integration Guide / Руководство по интеграции языков

This guide explains how to add and configure a new language in the `ios-system` keyboard project.
Это руководство объясняет, как добавлять и настраивать новые языки в проекте клавиатур `ios-system`.

---

## 1. File Naming Conventions / Именование файлов

Each language should have its own folder in `layout/{iso_code}/`. Standard file names are:
Каждый язык должен иметь свою папку в `layout/{iso_code}/`. Стандартные имена файлов:

- `{iso}-3-rows.yaml`: Main 3-row layout for iPhone/iPad. / Основная 3-рядная раскладка.
- `{iso}-4-rows.yaml`: 4-row layout with extra characters. / 4-рядная раскладка с доп. символами.
- `{iso}-macos.yaml`: Physical keyboard layout for macOS. / Раскладка для физических клавиатур macOS.
- `{iso}-keynames.yaml`: Translations for UI keys (Space, Return, etc.). / Переводы системных клавиш.
- `{iso}-longpress.yaml`: Definitions for held keys. / Настройки для зажатия клавиш (лонгпрессов).

---

## 2. Layout Structure / Структура раскладки

### Metadata / Метаданные
At the top of the YAML file, define the language names:
В начале YAML-файла определите названия языка:
```yaml
displayNames:
  en: English Name
  ru: Русское название
  iso: Native Name / Самоназвание
ABC: Label for the language switch key / Метка для кнопки переключения
abc: Lowercase version / Строчная версия
```

### iOS Layers / Слои iOS
The `iOS` section contains definitions for different devices:
Секция `iOS` содержит определения для разных устройств:
- `primary`: Default for iPhone. / По умолчанию для iPhone.
- `iPad-9in`: Optimized for standard iPads. / Оптимизировано для обычных iPad.
- `iPad-12in`: Optimized for large iPads (usually 5 rows). / Для больших iPad (обычно 5 рядов).

Each device has `layers` such as `default`, `shift`, `symbols-1`, and `symbols-2`.
У каждого устройства есть слои: `default` (строчные), `shift` (заглавные), `symbols-1` (цифры) и `symbols-2` (спецсимволы).

---

## 3. Special Keys and Spacers / Спецклавиши и отступы

Use the following syntax for system keys:
Используйте следующий синтаксис для системных клавиш:
- `\s{shift}`: Shift key.
- `\s{backspace}`: Delete key.
- `\s{return}`: Enter key.
- `\s{spacer:N}`: Empty space with width N. / Пустое пространство шириной N.

**Important for iPad / Важно для iPad**:
To balance the layout, the sum of widths in one row should be constant (usually 13 units).
Для балансировки ряда сумма ширин всех клавиш должна быть константой (обычно 13 единиц).
Example: `\s{spacer:0.3} ...keys... \s{spacer:1.7}` = 2 units of spacers + 11 keys = 13.

---

## 4. Key Names and Longpress / Имена клавиш и Лонгпрессы

These should be defined in separate files and included at the end of the layout file:
Они должны быть определены в отдельных файлах и подключены в конце основного файла:

```yaml
keyNames: !include iso-keynames.yaml
longpress: !include iso-longpress.yaml
```

- **keyNames**: Maps system IDs (`space`, `return`) to translated labels. / Сопоставляет ID системных клавиш с их переводами.
- **longpress**: Maps a base character to a string of alternatives. / Сопоставляет базовый символ со строкой альтернатив при зажатии.
  Example / Пример: `а: "а̄ а́"`

---

## 5. Character Codes / Коды символов

Always prefer standard Unicode characters. If a character looks similar to another, verify the codepoint.
Всегда используйте стандартные символы Unicode. Если символы выглядят похоже, проверяйте их код (Codepoint).
- **Combining Macron / Комбинируемый макрон**: `U+0304` ( ̄ )
- **Modifier Letter Apostrophe / Апостроф**: `U+02BC` ( ’ )

---

## 6. Build and Verification / Сборка и проверка

After making changes, run the build scripts:
После внесения изменений запустите скрипты сборки:
1. `python3 scripts/build.py`: Generates the HTML preview. / Генерирует HTML-превью.
2. `python3 scripts/gen_svg.py`: Updates SVG statistics. / Обновляет SVG-статистику.

Check `dist/ios-keyboards.html` to verify the visual layout.
Проверьте файл `dist/ios-keyboards.html`, чтобы убедиться в правильности верстки.
