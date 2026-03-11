# 🇷🇺 Датасет клавиатур для iOS/macOS

Этот репозиторий содержит данные для системной клавиатуры на iOS/macOS. Например, **Тувинский (Тыва дыл)**.  
Датасет подготовлен для использования в системах ввода (например, Apple Keyboard, Unicode CLDR и других).

## 📘 Описание
Датасет для расскладки клавиатуры основана на современном дизайне, используемой в iOS и macOS.

Раскладки соответствуют унифицированной схеме клавиатуры, и совместимы с инструментами генерации раскладок для конкретных платформ.

Вы можете использовать подход как я сделал на примере ``tyv – Тыва дыл`` (Тувинский язык), слегка модифицируя ряды расскладки, включив все символы, используемые в современном письме выбранного языка.

Цель — предоставить корректную и удобную раскладку для носителей языка, включая поддержку автокоррекции, предсказаний и локализованных символов.

Минимально нужно описать файлы ``lang-3-rows.yaml`` и ``lang-longpress.yaml``, где вместо lang – код вашего языка.

### Знакомый пример
Большинство из вас хорошо знакомы с системной клавиатурой для Русского языка. Она описана [тут (тык сюда)](https://github.com/Agisight/ios-system-keyboard/tree/main/layout/rus).

## 🧩 Структура репозитория
```
ios-system-keyboard/
 ├── layout/tyv/
 │   ├── tyv-3-rows.yaml
 │   ├── tyv-4-rows.yaml
 │   ├── tyv-longpress.yaml
 │   ├── tyv-macos.yaml
 │   └── tyv-3-rows.png
 └── README.md
```

## 🗝️ Пример (фрагмент)
```
iOS:
  primary:
    layers:
      default: |
        й ү у к е н ң г ш з х
        ө ы в а п р о л д ж э
        \s{shift} я ч с м и т ь б ю \s{backspace}
      shift: |
        Й Ү У К Е Н Ң Г Ш З Х
        Ө Ы В А П Р О Л Д Ж Э
        \s{shift} Я Ч С М И Т Ь Б Ю \s{backspace}
```

## Переводы системных команд
Особое внимание уделяем системным командам типа "Отмена", "Ввод", "Маршрут" и т.д.

Есть особый гайд – [keyNames.md](https://github.com/Agisight/ios-system-keyboard/blob/main/keyNames.md). Изучите обязательно, есть наглядные примеры с картинками.

## 🌍 Контакт
Автор: Али Кужугет (Али Күжүгет)  
Проект: *Apple системные кириллические клавиатуры для всех*  

---

# 🇺🇸 Dataset for iOS/macOS Keyboards

This repository contains layout data for any languages. For example, the **Tuvan Cyrillic keyboard**,
designed for integration with Apple Keyboard, Unicode CLDR, and related input systems.

## 📘 Description
The keyboard layout dataset is based on the modern design used in iOS and macOS.

The layouts conform to a unified keyboard scheme and are compatible with layout generation tools for specific platforms.

You can use the approach I used in the example of "tyv – Тыва дыл" (Tuvan language), slightly modifying the layout rows to include all the characters used in the modern writing system of the selected language.

Its goal is to provide native users with a convenient, accurate, and inclusive typing experience.

At a minimum, you need to describe the files ``lang-3-rows.yaml`` and ``lang-longpress.yaml``, where lang is the code of your language.

### A familiar example
Most of you are familiar with the system keyboard for Russian. It's described [here (click here)](https://github.com/Agisight/ios-system-keyboard/tree/main/layout/rus).

## 🧩 Repository Structure
```
ios-system-keyboard/
 ├── layout/tyv/
 │   ├── tyv-3-rows.yaml
 │   ├── tyv-4-rows.yaml
 │   ├── tyv-longpress.yaml
 │   ├── tyv-macos.yaml
 │   └── tyv-3-rows.png
 └── README.md
```

## 🗝️ Example (fragment)
```
iOS:
  primary:
    layers:
      default: |
        й ү у к е н ң г ш з х
        ө ы в а п р о л д ж э
        \s{shift} я ч с м и т ь б ю \s{backspace}
      shift: |
        Й Ү У К Е Н Ң Г Ш З Х
        Ө Ы В А П Р О Л Д Ж Э
        \s{shift} Я Ч С М И Т Ь Б Ю \s{backspace}
```

## Translations of system commands
We pay special attention to system commands such as "Cancel," "Enter," "Route," and so on.

There's a special guide – [keyNames.md](https://github.com/Agisight/ios-system-keyboard/blob/main/keyNames.md). Be sure to check it out; there are illustrative examples with pictures.

## 🌍 Contact
Author: **Ali Kuzhuget**  
Project: *Apple Keyboards for All*
