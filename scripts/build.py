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
    "alt": ("Тюркские",   "#FF6B35"),
    "bak": ("Тюркские",   "#FF6B35"),
    "tat": ("Тюркские",   "#FF6B35"),
    "kjh": ("Тюркские",   "#FF6B35"),
    "chv": ("Тюркские",   "#FF6B35"),
    "xal": ("Монгольские", "#AF52DE"),
    "ykt": ("Тюркские",   "#FF6B35"),
    "ava": ("Кавказские", "#30B850"),
    "xdq": ("Кавказские", "#30B850"),
    "oss": ("Иранские",   "#FF9500"),
    "kom": ("Уральские",  "#5856D6"),
    "rus": ("Славянские", "#007aff"),
}
FAMILY_ORDER = ["Тюркские", "Монгольские", "Кавказские", "Иранские", "Уральские", "Славянские", "Другие"]

# Display names in Russian for language codes
LANG_NAMES_RU = {
    "tyv": "Тувинский", "alt": "Алтайский", "bak": "Башкирский", "tat": "Татарский",
    "kjh": "Хакасский", "chv": "Чувашский",  "xal": "Калмыцкий",
    "ava": "Аварский",  "xdq": "Кайтагский", "oss": "Осетинский",
    "kom": "Коми",      "rus": "Русский",
    "ykt": "Саха",
}

# ── YAML helpers ─────────────────────────────────────────────────────────────
def normalize_block_scalars(text):
    """
    In YAML literal block scalars (|), indentation is set by the FIRST non-empty line.
    Some files have the first row more-indented than the rest (for visual symmetry).
    This causes YAML parse errors. Fix: find the minimum indentation across all
    non-empty lines of each block and reduce deeper lines to that minimum.
    """
    lines = text.splitlines(keepends=True)
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r':\s*\|\s*$', line.rstrip()):
            # Collect the entire block
            result.append(line)
            i += 1
            block_lines = []
            # Determine the parent key's indentation to know when block ends
            parent_indent = len(line) - len(line.lstrip())
            while i < len(lines):
                bl = lines[i]
                stripped = bl.rstrip('\n\r')
                if stripped.strip() == '':
                    block_lines.append(bl)
                    i += 1
                    continue
                indent = len(stripped) - len(stripped.lstrip(' '))
                if indent <= parent_indent:
                    break  # out of block
                block_lines.append(bl)
                i += 1
            # Find minimum indent of non-empty lines in block
            indents = [len(l.rstrip('\n\r')) - len(l.rstrip('\n\r').lstrip(' '))
                       for l in block_lines if l.strip()]
            if indents:
                min_indent = min(indents)
                for bl in block_lines:
                    if bl.strip() == '':
                        result.append(bl)
                    else:
                        indent = len(bl.rstrip('\n\r')) - len(bl.rstrip('\n\r').lstrip(' '))
                        if indent > min_indent:
                            # trim extra leading spaces
                            result.append(' ' * min_indent + bl.lstrip(' '))
                        else:
                            result.append(bl)
            else:
                result.extend(block_lines)
        else:
            result.append(line)
            i += 1
    return ''.join(result)


def load_yaml(path):
    path = Path(path)

    def make_loader(base_path):
        class Loader(yaml.SafeLoader):
            pass

        def include_constructor(loader, node):
            include_str = loader.construct_scalar(node).strip()
            if "#" in include_str:
                inc_file, anchor = include_str.split("#", 1)
            else:
                inc_file, anchor = include_str, None
            inc_path = base_path.parent / inc_file
            if not inc_path.exists():
                return None
            try:
                inc_data = load_yaml(inc_path)
                if anchor and isinstance(inc_data, dict):
                    return inc_data.get(anchor)
                return inc_data
            except Exception:
                return None

        Loader.add_constructor("!include", include_constructor)
        Loader.add_constructor(None, lambda l, n: None)
        return Loader

    with open(path, encoding="utf-8") as f:
        raw = f.read()

    normalized = normalize_block_scalars(raw)
    # Fix YAML anchor names containing '+' (not allowed by spec)
    normalized = re.sub(r'(&|\*)([A-Z]+)\+([A-Z]+)', r'\1\2_\3', normalized)
    return yaml.load(normalized, Loader=make_loader(path)) or {}

def parse_rows(layer_str):
    """
    Parse YAML layer string → list of rows.
    Skip \\s{} tokens. Groups separated by 2+ spaces get a None spacer between them.
    """
    rows = []
    for line in layer_str.strip().splitlines():
        clean = re.sub(r'\\s\{[^}]*\}', '', line).strip()
        if not clean:
            continue
        # Split on 2+ spaces — each separator = one invisible spacer key
        parts = re.split(r' {2,}', clean)
        keys = []
        for pi, part in enumerate(parts):
            if pi > 0:
                keys.append(None)  # spacer between groups
            for k in part.split():
                if k:
                    keys.append(k)
        # strip trailing None
        while keys and keys[-1] is None:
            keys.pop()
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
    base = LANG_NAMES_RU.get(code, "")

    # If the native displayName IS the base name (e.g. ykt: "Саха" == LANG_NAMES_RU "Саха"),
    # displayNames won't yield a useful distinguishing label — skip to stem suffix.
    native_key = [k for k in names if k not in ("en", "eng", "ru", "rus")]
    native_val = names.get(native_key[0], "") if native_key else ""
    skip_display = (native_val == base)

    if not skip_display:
        # Try language-native name first, then Russian, then English
        for lang in [code, "ru", "rus", "en", "eng"]:
            val = names.get(lang, "")
            if not val or val == base:
                continue
            # Strip the base language name prefix if present
            val_clean = re.sub(rf"^{re.escape(base)}\s*[\(·\-]?\s*", "", val)
            # strip matching closing paren only if we stripped an opening one
            if val_clean != val and val_clean.endswith(')') and '(' not in val_clean:
                val_clean = val_clean[:-1]
            val_clean = val_clean.strip()
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

    SKIP = {"macos", "longpress", "keyname", "readme", "old", "sjd"}

    for yaml_file in sorted(LAYOUT.rglob("*.yaml")):
        # Skip macos, longpress, keynames, readme etc
        name_lower = yaml_file.name.lower()
        if any(s in name_lower for s in SKIP):
            continue
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

        # Parse symbol layers (symbols-1 = numbers/punct, symbols-2 = extra)
        sym1_str = layers.get("symbols-1", "")
        sym2_str = layers.get("symbols-2", "")
        sym1 = parse_rows(sym1_str) if sym1_str else None
        sym2 = parse_rows(sym2_str) if sym2_str else None

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
            "_nrows": len(rows),  # internal: used for label dedup
        }
        if sym1: layout_entry["sym1"] = sym1
        if sym2: layout_entry["sym2"] = sym2

        if code not in langs_by_code:
            langs_by_code[code] = {
                "code": code, "name": name_ru, "native": native, "layouts": []
            }
        # avoid duplicate ids
        existing_ids = {l["id"] for l in langs_by_code[code]["layouts"]}
        if lid not in existing_ids:
            langs_by_code[code]["layouts"].append(layout_entry)

    # ── Post-process: disambiguate duplicate labels with row count ─────────
    ROW_SUFFIX = {3: "3 ряда", 4: "4 ряда", 5: "5 рядов"}
    for code, lang in langs_by_code.items():
        layouts = lang["layouts"]
        if len(layouts) < 2:
            continue
        # Find labels that appear more than once
        from collections import Counter
        label_counts = Counter(l["label"] for l in layouts)
        for lay in layouts:
            if label_counts[lay["label"]] > 1:
                nr = lay.get("_nrows", 0)
                suffix = ROW_SUFFIX.get(nr, f"{nr} рядов")
                lay["label"] = f"{lay['label']} · {suffix}"
    # Remove internal _nrows field
    for code, lang in langs_by_code.items():
        for lay in lang["layouts"]:
            lay.pop("_nrows", None)

    # Group by family
    families = {}
    for code, lang in langs_by_code.items():
        fam, color = FAMILY.get(code, ("Другие", "#8e8e93"))
        if fam not in families:
            families[fam] = {"group": fam, "color": color, "langs": []}
        families[fam]["langs"].append(lang)

    # ── Discover macOS layouts ────────────────────────────────────────────────
    macos_by_code = {}  # code → [{file: "tyv.keylayout", name: "Тыва — Тувинский"}]
    for yaml_file in sorted(LAYOUT.rglob("*-macos*.yaml")):
        code = yaml_file.parent.name
        if code == "layout":
            code = yaml_file.stem.split("-")[0]
        stem = yaml_file.stem.replace("-macos", "")
        keylayout_name = f"{stem}.keylayout"
        # Try to get display name
        try:
            data = load_yaml(yaml_file)
            names = data.get("displayNames") or {}
            native_keys = [k for k in names if k not in ("en", "eng", "ru", "rus")]
            native = names.get(native_keys[0], "") if native_keys else ""
            ru_name = names.get("ru") or names.get("rus", "")
            display = f"{native} — {ru_name}" if native and ru_name and native != ru_name else (ru_name or native or stem)
        except Exception:
            display = stem
        if code not in macos_by_code:
            macos_by_code[code] = []
        macos_by_code[code].append({"file": keylayout_name, "name": display})

    # Inject macOS info into lang entries
    for code, lang in langs_by_code.items():
        if code in macos_by_code:
            lang["macos"] = macos_by_code[code]

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
