#!/usr/bin/env python3
"""
build.py — читает layout/**/*.yaml и генерирует dist/ios-keyboards.html
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
    "bua": ("Монгольские", "#AF52DE"),
    "ykt": ("Тюркские",   "#FF6B35"),
    "tle": ("Тюркские",   "#FF6B35"),
    "gag": ("Тюркские",   "#FF6B35"),
    "ava": ("Кавказские", "#30B850"),
    "xdq": ("Кавказские", "#30B850"),
    "oss": ("Иранские",   "#FF9500"),
    "kom": ("Уральские",  "#5856D6"),
    "rus": ("Славянские", "#007aff"),
}
FAMILY_ORDER = ["Тюркские", "Монгольские", "Кавказские", "Иранские", "Уральские", "Славянские", "Другие"]

LANG_NAMES_RU = {
    "tyv": "Тувинский", "alt": "Алтайский", "bak": "Башкирский", "tat": "Татарский",
    "kjh": "Хакасский", "chv": "Чувашский",  "xal": "Калмыцкий", "bua": "Бурятский",
    "ava": "Аварский",  "xdq": "Кайтагский", "oss": "Осетинский",
    "kom": "Коми",      "rus": "Русский",
    "ykt": "Саха",      "tle": "Телеутский",
    "gag": "Гагаузский",
}

# ── YAML helpers ─────────────────────────────────────────────────────────────
def normalize_block_scalars(text):
    """
    Injects indentation indicators (|2, |4 etc) to block scalars if the first line
    is more indented than the minimum. This prevents YAML parse errors while
    preserving all spaces.
    """
    lines = text.splitlines(keepends=True)
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r':\s*\|\s*$', line.rstrip()):
            hdr_idx = len(result)
            result.append(line)
            parent_indent = len(line) - len(line.lstrip())
            i += 1
            block_lines = []
            while i < len(lines):
                bl = lines[i]
                if bl.strip() == '':
                    block_lines.append(bl); i += 1; continue
                indent = len(bl) - len(bl.lstrip(' '))
                if indent <= parent_indent: break
                block_lines.append(bl); i += 1
            
            indents = [len(l) - len(l.lstrip(' ')) for l in block_lines if l.strip()]
            if indents:
                min_indent = min(indents)
                rel = min_indent - parent_indent
                if rel > 0:
                    result[hdr_idx] = result[hdr_idx].replace('|', f'|{rel}')
            result.extend(block_lines)
        else:
            result.append(line); i += 1
    return ''.join(result)

def load_yaml(path):
    path = Path(path)
    def make_loader(base_path):
        class Loader(yaml.SafeLoader): pass
        def include_constructor(loader, node):
            include_str = loader.construct_scalar(node).strip()
            inc_file = include_str.split("#")[0]
            inc_path = base_path.parent / inc_file
            if not inc_path.exists(): return None
            return load_yaml(inc_path)
        Loader.add_constructor("!include", include_constructor)
        return Loader
    with open(path, encoding="utf-8") as f: raw = f.read()
    normalized = normalize_block_scalars(raw)
    normalized = re.sub(r'(&|\*)([A-Z]+)\+([A-Z]+)', r'\1\2_\3', normalized)
    return yaml.load(normalized, Loader=make_loader(path)) or {}

def parse_rows(layer_str, smart_spaces=False):
    rows = []
    for line in layer_str.splitlines():
        if not line.strip(): continue
        if smart_spaces:
            parts = re.findall(r'\\s\{[^}]*\}| {2,}|[^\s]+', line)
            tokens = []
            for p in parts:
                if p.startswith(' '):
                    for _ in range(len(p)//2): tokens.append('\\s{spacer:1}')
                else: tokens.append(p)
            if tokens: rows.append(tokens)
        else:
            keys = re.findall(r'\\s\{[^}]*\}|[^\s]+', line)
            if keys: rows.append(keys)
    return rows

def get_display_name(data, lang):
    names = data.get("displayNames") or data.get("displaynames") or {}
    if names.get(lang): return names[lang]
    native_keys = [k for k in names if k not in ("en","eng","ru","rus") and (k==lang or (k not in FAMILY and k not in LANG_NAMES_RU))]
    for nk in native_keys:
        if names.get(nk): return names[nk]
    return names.get("ru") or names.get("en") or next(iter(names.values()), "")

def parse_longpress(lp_data):
    if not lp_data or not isinstance(lp_data, dict): return {}
    res = {}
    for k, v in lp_data.items():
        if isinstance(v, list): res[str(k)] = ' '.join(map(str, v))
        else: res[str(k)] = str(v)
    return res

def make_layout_id(code, stem):
    if stem == code or stem == f"{code}-3-rows": return code
    return stem

def make_label(data, code, stem, lid):
    if lid == code: return "Стандартная"
    label = data.get("label") or stem.replace(f"{code}-", "").replace("-", " ").title()
    return label

# ── Discovery ─────────────────────────────────────────────────────────────────
def discover():
    langs_by_code = {}
    lp_map = {}
    SKIP = {"macos", "longpress", "keyname", "readme", "old", "sjd"}

    for yaml_file in sorted(LAYOUT.rglob("*.yaml")):
        if any(s in yaml_file.name.lower() for s in SKIP): continue
        try:
            data = load_yaml(yaml_file)
        except Exception as e:
            print(f"  ⚠️  Skip {yaml_file.name}: {e}"); continue
        
        ios = data.get("iOS") or data.get("ios") or {}
        primary = ios.get("primary") or {}
        layers = primary.get("layers") or {}
        default_str = layers.get("default", "")
        shift_str = layers.get("shift", "")
        if not default_str: continue

        code = yaml_file.parent.name
        if code == "layout": code = yaml_file.stem.split("-")[0]
        
        is_smart = (code == 'kjh')
        rows = parse_rows(default_str, smart_spaces=is_smart)
        shift = parse_rows(shift_str, smart_spaces=is_smart) if shift_str else rows
        
        sym1_str = layers.get("symbols-1", "")
        sym2_str = layers.get("symbols-2", "")
        sym1 = parse_rows(sym1_str, smart_spaces=is_smart) if sym1_str else None
        sym2 = parse_rows(sym2_str, smart_spaces=is_smart) if sym2_str else None

        stem = yaml_file.stem
        lid = make_layout_id(code, stem)
        label = make_label(data, code, stem, lid)
        native = get_display_name(data, code)
        name_ru = LANG_NAMES_RU.get(code) or get_display_name(data, "ru")
        key_names = data.get("keyNames") or {}
        space = key_names.get("space", "Space")
        ret = key_names.get("return", "Return")
        abc = data.get("ABC", "АБВ")

        lp_raw = data.get("longpress") or {}
        lp = parse_longpress(lp_raw)
        if lp: lp_map[lid] = lp

        layout_entry = {
            "id": lid, "label": label, "abc": abc,
            "rows": rows, "shift": shift,
            "space": space, "ret": ret,
            "_nrows": len(rows)
        }
        if sym1: layout_entry["sym1"] = sym1
        if sym2: layout_entry["sym2"] = sym2

        if code not in langs_by_code:
            langs_by_code[code] = {"code":code, "name":native, "native":name_ru, "layouts":[], "keyNames":key_names}
        else:
            if key_names: langs_by_code[code]["keyNames"].update(key_names)
            existing = langs_by_code[code]["name"]
            if native and ('(' not in native) and ('(' in existing or len(native) < len(existing)):
                langs_by_code[code]["name"] = native
        
        if lid not in {l["id"] for l in langs_by_code[code]["layouts"]}:
            langs_by_code[code]["layouts"].append(layout_entry)

    # Post-process labels
    ROW_SUFFIX = {3: "3 ряда", 4: "4 ряда", 5: "5 рядов"}
    for code, lang in langs_by_code.items():
        lang["layouts"].sort(key=lambda l: (len(l["id"]), l["id"]))
        from collections import Counter
        label_counts = Counter(l["label"] for l in lang["layouts"])
        for lay in lang["layouts"]:
            if label_counts[lay["label"]] > 1:
                nr = lay.pop("_nrows", 0)
                lay["label"] = f"{lay['label']} · {ROW_SUFFIX.get(nr, f'{nr} рядов')}"
            else:
                lay.pop("_nrows", None)

    # Group by family
    res = []
    for fam in FAMILY_ORDER:
        langs = [l for c, l in langs_by_code.items() if FAMILY.get(c, ("Другие",""))[0] == fam]
        if langs:
            try:
                color = next(f[1] for c, f in FAMILY.items() if f[0]==fam)
            except StopIteration:
                color = "#8e8e93" # Default color for 'Other'
            res.append({"group":fam, "color":color, "langs":sorted(langs, key=lambda x: x["name"])})
    return res, lp_map

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    data, lp_map = discover()
    with open(TEMPLATE, encoding="utf-8") as f: html = f.read()
    html = html.replace("/*BUILD_DATA*/[]", json.dumps(data, ensure_ascii=False))
    html = html.replace("/*BUILD_LP*/{}", json.dumps(lp_map, ensure_ascii=False))
    
    DIST.mkdir(exist_ok=True)
    with open(DIST / "ios-keyboards.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Written → {DIST / 'ios-keyboards.html'}  ({len(html)//1024} KB)")
