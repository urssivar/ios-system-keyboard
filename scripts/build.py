#!/usr/bin/env python3
"""
build.py — читает layout/**/*.yaml и генерирует dist/ios-keyboards.html

Использование:
  python build.py                   # генерирует из scripts/template.html
  python build.py --check           # только проверяет YAML без генерации

Структура репозитория:
  layout/
    tyv/  tyv-3-rows.yaml, tyv-4-rows.yaml, tyv-longpress.yaml ...
    bak/  bak-3-rows.yaml, bak-4-rows.yaml ...
  scripts/
    build.py
    template.html
  dist/
    ios-keyboards.html   ← результат
"""

import os, re, json, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Installing pyyaml...")
    os.system("pip install pyyaml --break-system-packages -q")
    import yaml

ROOT     = Path(__file__).parent.parent
LAYOUT   = ROOT / "layout"
SCRIPTS  = ROOT / "scripts"
DIST     = ROOT / "dist"
TEMPLATE = SCRIPTS / "template.html"

# ── Language family mapping ───────────────────────────────────────────────────
FAMILY = {
    "tyv": ("Тюркские",   "#FF6B35"),
    "bak": ("Тюркские",   "#FF6B35"),
    "tat": ("Тюркские",   "#FF6B35"),
    "kjh": ("Тюркские",   "#FF6B35"),
    "chv": ("Тюркские",   "#FF6B35"),
    "xal": ("Тюркские",   "#FF6B35"),
    "ava": ("Кавказские", "#30B850"),
    "xdq": ("Кавказские", "#30B850"),
    "oss": ("Иранские",   "#FF9500"),
    "kom": ("Уральские",  "#5856D6"),
    "rus": ("Славянские", "#007aff"),
}
FAMILY_ORDER = ["Тюркские", "Кавказские", "Иранские", "Уральские", "Славянские", "Другие"]

# Display names in Russian for language codes
LANG_NAMES_RU = {
    "tyv": "Тувинский", "bak": "Башкирский", "tat": "Татарский",
    "kjh": "Хакасский", "chv": "Чувашский",  "xal": "Калмыцкий",
    "ava": "Аварский",  "xdq": "Кайтагский", "oss": "Осетинский",
    "kom": "Коми",      "rus": "Русский",
}

# ── YAML helpers ─────────────────────────────────────────────────────────────
def load_yaml(path):
    # Handle !include tags by ignoring them (we resolve longpress separately)
    class IgnoreInclude(yaml.SafeLoader):
        pass
    def ignore_include(loader, node):
        return None
    IgnoreInclude.add_constructor("!include", ignore_include)
    with open(path, encoding="utf-8") as f:
        return yaml.load(f, Loader=IgnoreInclude) or {}

def parse_rows(layer_str):
    """Parse YAML layer string → list of rows (skip \\s{} tokens, skip empty)."""
    rows = []
    for line in layer_str.strip().splitlines():
        keys = [t for t in line.split() if not t.startswith("\\s{") and t]
        if keys:
            rows.append(keys)
    return rows

def get_display_name(data, lang):
    names = data.get("displayNames") or data.get("displaynames") or {}
    return (names.get(lang) or names.get("ru") or names.get("en")
            or names.get("eng") or next(iter(names.values()), ""))

def parse_longpress(lp_data):
    """Flatten longpress YAML → {char: 'alt1 alt2 ...'}"""
    if not lp_data or not isinstance(lp_data, dict):
        return {}
    result = {}
    for k, v in lp_data.items():
        if v is not None:
            result[str(k)] = str(v).strip()
    return result

def find_longpress_file(yaml_file, code, stem):
    """Try to find a dedicated longpress file for this layout."""
    candidates = [
        yaml_file.parent / f"{stem}-longpress.yaml",
        yaml_file.parent / f"{code}-longpress.yaml",
        yaml_file.parent / f"{code}-3-rows-longpress.yaml",
        yaml_file.parent / f"{stem.replace(code+'-','')}-longpress.yaml",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def make_layout_id(code, stem):
    """Turn 'tyv-3-rows' → 'tyv', 'tyv-4-rows' → 'tyv-4', 'bak-3-rows-rus' → 'bak-rus'"""
    # Remove the language code prefix
    suffix = stem[len(code):].lstrip("-")
    # Normalise common suffixes
    suffix = re.sub(r"^3-rows?$",    "",     suffix)
    suffix = re.sub(r"^3-rows?-",    "",     suffix)
    suffix = re.sub(r"^4-rows?$",    "4",    suffix)
    suffix = re.sub(r"^4-rows?-",    "4-",   suffix)
    return f"{code}-{suffix}".rstrip("-") if suffix else code

def make_label(data, code, stem, lid):
    """Human-readable variant label from displayNames or stem."""
    names = data.get("displayNames") or data.get("displaynames") or {}
    # Try language-native name first, then Russian, then English
    for lang in [code, "ru", "rus", "en", "eng"]:
        val = names.get(lang, "")
        if val:
            # Strip the base language name prefix if present
            base = LANG_NAMES_RU.get(code, "")
            val_clean = re.sub(rf"^{re.escape(base)}\s*[\(·\-]?\s*", "", val).strip(")")
            if val_clean and val_clean != base:
                return val_clean
    # Fallback: derive from stem
    suffix = stem[len(code):].lstrip("-")
    mapping = {
        "3-rows": "3 ряда", "3rows": "3 ряда",
        "4-rows": "4 ряда", "4rows": "4 ряда",
        "3-rows-rus": "На основе русской", "rus": "На основе русской",
        "macos": "macOS", "macos-pc": "macOS PC",
    }
    return mapping.get(suffix, suffix.replace("-", " ").title() or "Стандарт")

# ── Discovery ─────────────────────────────────────────────────────────────────
def discover():
    """
    Returns:
      data   — list of {group, color, langs:[{code,name,native,layouts:[...]}]}
      lp_map — {layout_id: {char: 'alts...'}}
    """
    langs_by_code = {}   # code → {name, native, layouts:[]}
    lp_map = {}          # layout_id → {char: alts}

    for yaml_file in sorted(LAYOUT.rglob("*-rows*.yaml")):
        try:
            data = load_yaml(yaml_file)
        except Exception as e:
            print(f"  ⚠️  Skip {yaml_file.name}: {e}")
            continue
        ios  = data.get("iOS") or data.get("ios") or {}
        primary = ios.get("primary") or {}
        layers  = primary.get("layers") or {}
        default_str = layers.get("default", "")
        shift_str   = layers.get("shift", "")
        if not default_str:
            continue

        rows  = parse_rows(default_str)
        shift = parse_rows(shift_str) if shift_str else rows
        if not rows:
            continue

        # code = parent folder name
        code = yaml_file.parent.name
        if code == "layout":
            code = yaml_file.stem.split("-")[0]

        stem = yaml_file.stem
        lid  = make_layout_id(code, stem)
        label = make_label(data, code, stem, lid)

        native = get_display_name(data, code)
        name_ru = LANG_NAMES_RU.get(code) or get_display_name(data, "ru") or get_display_name(data, "en")

        key_names = data.get("keyNames") or {}
        space = key_names.get("space", "Space")
        ret   = key_names.get("return", "Return")
        abc   = data.get("ABC", "АБВ")

        # Longpress — try inline then dedicated file
        lp_raw = data.get("longpress") or {}
        if not lp_raw:
            lp_path = find_longpress_file(yaml_file, code, stem)
            if lp_path:
                try:
                    lp_raw = load_yaml(lp_path)
                except Exception:
                    lp_raw = {}
        lp = parse_longpress(lp_raw)
        if lp:
            lp_map[lid] = lp

        layout_entry = {
            "id": lid, "label": label, "abc": abc,
            "rows": rows, "shift": shift,
            "space": space, "ret": ret,
        }

        if code not in langs_by_code:
            langs_by_code[code] = {
                "code": code, "name": name_ru, "native": native, "layouts": []
            }
        # avoid duplicate ids
        existing_ids = {l["id"] for l in langs_by_code[code]["layouts"]}
        if lid not in existing_ids:
            langs_by_code[code]["layouts"].append(layout_entry)

    # Group by family
    families = {}
    for code, lang in langs_by_code.items():
        fam, color = FAMILY.get(code, ("Другие", "#8e8e93"))
        if fam not in families:
            families[fam] = {"group": fam, "color": color, "langs": []}
        families[fam]["langs"].append(lang)

    groups = []
    for fam in FAMILY_ORDER:
        if fam in families:
            groups.append(families[fam])
    for fam, g in families.items():
        if fam not in FAMILY_ORDER:
            groups.append(g)

    return groups, lp_map

# ── Generate JS strings ───────────────────────────────────────────────────────
def js(obj):
    return json.dumps(obj, ensure_ascii=False)

def build_lp_js(lp_map):
    lines = []
    for lid, mapping in sorted(lp_map.items()):
        inner = ",".join(f"{js(k)}:{js(v)}" for k, v in mapping.items())
        lines.append(f"  {js(lid)}:{{{inner}}}")
    return "{\n" + ",\n".join(lines) + "\n}"

def build_data_js(groups):
    return js(groups)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    check_only = "--check" in sys.argv

    print("📂 Scanning layout/ ...")
    groups, lp_map = discover()

    total_langs   = sum(len(g["langs"]) for g in groups)
    total_layouts = sum(len(l["layouts"]) for g in groups for l in g["langs"])
    print(f"✅ Found {total_langs} languages, {total_layouts} layouts, {len(lp_map)} longpress maps")

    for g in groups:
        print(f"\n  {g['group']}:")
        for lang in g["langs"]:
            labels = [l["label"] for l in lang["layouts"]]
            print(f"    {lang['code']:6s} {lang['name']:20s} → {', '.join(labels)}")

    if check_only:
        print("\n✅ Check complete (no files written)")
        return

    if not TEMPLATE.exists():
        print(f"\n❌ Template not found: {TEMPLATE}")
        print("   Put scripts/template.html (the HTML with /*BUILD_LP*/ and /*BUILD_DATA*/ markers)")
        sys.exit(1)

    DIST.mkdir(exist_ok=True)

    template = TEMPLATE.read_text(encoding="utf-8")

    lp_js   = build_lp_js(lp_map)
    data_js = build_data_js(groups)

    html = template.replace("/*BUILD_LP*/{}",   f"/*BUILD_LP*/{lp_js}")
    html = html.replace("/*BUILD_DATA*/[]", f"/*BUILD_DATA*/{data_js}")

    if "/*BUILD_LP*/" not in template or "/*BUILD_DATA*/" not in template:
        print("❌ Template is missing /*BUILD_LP*/ or /*BUILD_DATA*/ markers!")
        sys.exit(1)

    out = DIST / "ios-keyboards.html"
    out.write_text(html, encoding="utf-8")
    print(f"\n✅ Written → {out}  ({out.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
