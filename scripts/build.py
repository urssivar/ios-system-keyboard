#!/usr/bin/env python3
"""
build.py — читает layout/**/*.yaml и генерирует dist/ios-keyboards.html
Запуск: python scripts/build.py
"""

import os, re, json, yaml
from pathlib import Path

ROOT   = Path(__file__).parent.parent
LAYOUT = ROOT / "layout"
DIST   = ROOT / "dist"
DIST.mkdir(exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def parse_rows(layer_str: str) -> list[list[str]]:
    """Turn a YAML layer string into a list of rows (skip special tokens)."""
    rows = []
    for line in layer_str.strip().splitlines():
        keys = []
        for token in line.split():
            if token.startswith("\\s{"):
                continue        # skip \s{shift}, \s{backspace}, etc.
            keys.append(token)
        if keys:
            rows.append(keys)
    return rows

def parse_longpress(lp_data: dict | None) -> dict:
    """Flatten longpress YAML into {char: 'alt1 alt2 ...'} mapping."""
    if not lp_data:
        return {}
    result = {}
    for k, v in lp_data.items():
        key = str(k)
        val = str(v).strip()
        result[key] = val
    return result

def display_name(data: dict, lang: str = "en") -> str:
    names = data.get("displayNames") or data.get("displaynames") or {}
    return names.get(lang) or names.get("en") or names.get("eng") or next(iter(names.values()), "")

# ── language family heuristics ────────────────────────────────────────────────

FAMILY = {
    "tyv": "Тюркские", "bak": "Тюркские", "tat": "Тюркские",
    "kjh": "Тюркские", "chv": "Тюркские", "xal": "Монгольские",
    "ava": "Кавказские", "xdq": "Кавказские", "oss": "Иранские",
    "kom": "Уральские", "rus": "Славянские",
}

def family_of(code: str) -> str:
    return FAMILY.get(code, "Другие")

# ── discover layouts ──────────────────────────────────────────────────────────

def discover() -> list[dict]:
    """
    Returns sorted list of language groups, each with a list of layouts.
    Each layout has: id, label, abc, rows, shift, space, ret, longpress
    """
    langs: dict[str, dict] = {}

    for yaml_file in sorted(LAYOUT.rglob("*.yaml")):
        # skip old/backup files and loose top-level yamls that aren't layouts
        if yaml_file.stem.endswith("-old"):
            continue
        # only process files that contain iOS keyboard data
        data = load_yaml(yaml_file)
        ios = data.get("iOS") or data.get("ios")
        if not ios:
            continue

        primary = ios.get("primary") or {}
        layers  = primary.get("layers") or {}
        default_str = layers.get("default") or ""
        shift_str   = layers.get("shift")   or ""
        if not default_str:
            continue

        rows_default = parse_rows(default_str)
        rows_shift   = parse_rows(shift_str) if shift_str else rows_default

        # language code = parent folder name
        code = yaml_file.parent.name  # e.g. "tyv", "chv"
        if code == "layout":           # loose yaml in root of layout/
            code = yaml_file.stem.split("-")[0]

        lang_name_en = display_name(data, "en")
        lang_name_ru = display_name(data, "ru") or display_name(data, "rus")
        native_name  = display_name(data, code)

        # layout variant label (from filename)
        stem = yaml_file.stem  # e.g. "chv-google", "tyv-3-rows"
        # strip lang prefix
        label_raw = stem[len(code):].lstrip("-").replace("-", " ").strip()
        if not label_raw or label_raw in ("3 rows", "4 rows"):
            label_raw = lang_name_en

        # longpress — try inline or included file
        lp_raw  = data.get("longpress") or {}
        if not lp_raw:
            # look for a dedicated longpress file
            lp_candidates = [
                yaml_file.parent / f"{stem}-longpress.yaml",
                yaml_file.parent / f"{code}-longpress.yaml",
                yaml_file.parent / f"{code}-3-rows-longpress.yaml",
            ]
            for lp_path in lp_candidates:
                if lp_path.exists():
                    lp_raw = load_yaml(lp_path)
                    break
        longpress = parse_longpress(lp_raw)

        layout_entry = {
            "id":        stem,
            "label":     label_raw,
            "abc":       data.get("ABC", "АБВ"),
            "rows":      rows_default,
            "shift":     rows_shift,
            "space":     (data.get("keyNames") or {}).get("space", "пробел"),
            "ret":       (data.get("keyNames") or {}).get("return", "return"),
            "longpress": longpress,
        }

        if code not in langs:
            langs[code] = {
                "code":    code,
                "name":    lang_name_ru or lang_name_en,
                "native":  native_name or lang_name_en,
                "family":  family_of(code),
                "layouts": [],
            }
        langs[code]["layouts"].append(layout_entry)

    # group by family
    families: dict[str, list] = {}
    for lang in langs.values():
        fam = lang["family"]
        families.setdefault(fam, []).append(lang)

    # stable family order
    ORDER = ["Тюркские", "Монгольские", "Кавказские", "Иранские", "Уральские", "Славянские", "Другие"]
    groups = []
    for fam in ORDER:
        if fam in families:
            groups.append({"name": fam, "langs": families[fam]})
    # append any unknown families
    for fam, langs_list in families.items():
        if fam not in ORDER:
            groups.append({"name": fam, "langs": langs_list})

    return groups

# ── build HTML ────────────────────────────────────────────────────────────────

TEMPLATE_PATH = ROOT / "scripts" / "template.html"

def build():
    groups = discover()
    data_json = json.dumps(groups, ensure_ascii=False, indent=2)

    # Read the HTML template (the keyboard explorer HTML with a placeholder)
    if TEMPLATE_PATH.exists():
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        print("⚠️  No template.html found in scripts/ — writing data JSON only")
        (DIST / "data.json").write_text(data_json, encoding="utf-8")
        print(f"✅  dist/data.json written ({len(groups)} groups)")
        return

    # Inject data into template
    html = re.sub(
        r"const DATA\s*=\s*\{.*?\};",
        f"const DATA = {data_json};",
        template,
        flags=re.DOTALL,
    )

    # Inject build metadata comment
    from datetime import datetime, timezone
    ts  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sha = os.environ.get("GITHUB_SHA", "local")[:7]
    html = html.replace(
        "<!-- BUILD_META -->",
        f"<!-- Built by scripts/build.py @ {ts} ({sha}) -->"
    )

    out = DIST / "ios-keyboards.html"
    out.write_text(html, encoding="utf-8")

    total_layouts = sum(len(l["layouts"]) for g in groups for l in g["langs"])
    total_langs   = sum(len(g["langs"]) for g in groups)
    print(f"✅  dist/ios-keyboards.html — {total_langs} languages, {total_layouts} layouts")

if __name__ == "__main__":
    build()
