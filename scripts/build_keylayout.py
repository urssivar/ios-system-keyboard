#!/usr/bin/env python3
"""
build_keylayout.py — конвертирует layout/**/*-macos*.yaml → dist/*.keylayout

Использование:
  python scripts/build_keylayout.py                # генерирует все .keylayout
  python scripts/build_keylayout.py --check        # только проверяет YAML
  python scripts/build_keylayout.py --lang tyv     # только один язык

Результат: dist/<name>.keylayout для каждого *-macos*.yaml

Формат macOS .keylayout описан в:
  /System/Library/DTDs/KeyboardLayout.dtd
"""

import os, re, sys, hashlib, html
from pathlib import Path
from xml.sax.saxutils import quoteattr

try:
    import yaml
except ImportError:
    os.system("pip install pyyaml --break-system-packages -q")
    import yaml

ROOT   = Path(__file__).resolve().parent.parent
LAYOUT = ROOT / "layout"
DIST   = ROOT / "dist" / "keylayout"

# ── macOS keycodes for physical key positions ────────────────────────────────
# ANSI layout: row sizes 13, 13, 11, 10
ANSI_KEYCODES = [
    [50, 18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24],       # row 0: ` 1 2 ... =
    [12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30, 42],       # row 1: q w e ... \ (ё)
    [0,  1,  2,  3,  5,  4, 38, 40, 37, 41, 39],                 # row 2: a s d ... '
    [6,  7,  8,  9, 11, 45, 46, 43, 47, 44],                     # row 3: z x c ... /
]

# ISO layout: row sizes 13, 12, 12, 10 or 11
ISO_KEYCODES = [
    [50, 18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24],       # row 0: same
    [12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30],           # row 1: no backslash
    [0,  1,  2,  3,  5,  4, 38, 40, 37, 41, 39, 42],            # row 2: + key 42
    [10,  6,  7,  8,  9, 11, 45, 46, 43, 47, 44],               # row 3: + key 10
]

# Special keys that must be present in every keyMap
SPECIAL_KEYS = {
    36: "\u000D",   # Return
    48: "\u0009",   # Tab
    49: " ",        # Space — will be set to \u0020
    51: "\u0008",   # Delete (Backspace)
    53: "\u001B",   # Escape
    64: "\u0010",   # F5
    71: "\u001B",   # Clear (Esc)
    76: "\u0003",   # Enter (numpad)
    96: "\u0010",   # F5
    97: "\u0010",   # F6
    98: "\u0010",   # F7
    99: "\u0010",   # F3
   100: "\u0010",   # F8
   101: "\u0010",   # F9
   103: "\u0010",   # F11
   105: "\u0010",   # F13
   107: "\u0010",   # F14
   109: "\u0010",   # F10
   111: "\u0010",   # F12
   113: "\u0010",   # F15
   114: "\u0010",   # Help/Insert
   115: "\u0001",   # Home
   116: "\u000B",   # Page Up
   117: "\u007F",   # Forward Delete
   118: "\u0010",   # F4
   119: "\u0004",   # End
   120: "\u0010",   # F2
   121: "\u000C",   # Page Down
   122: "\u0010",   # F1
   123: "\u001C",   # Left Arrow
   124: "\u001D",   # Right Arrow
   125: "\u001F",   # Down Arrow
   126: "\u001E",   # Up Arrow
}

# Numpad keys
NUMPAD_KEYS = {
    65: ".",    # Numpad Decimal
    67: "*",    # Numpad Multiply
    69: "+",    # Numpad Add
    75: "/",    # Numpad Divide
    78: "-",    # Numpad Subtract
    81: "=",    # Numpad Equal
    82: "0", 83: "1", 84: "2", 85: "3",
    86: "4", 87: "5", 88: "6", 89: "7",
    91: "8", 92: "9",
}

# Dead key compositions (for ´, ¨, ¯)
DEAD_KEY_COMPOSITIONS = {
    "\u00B4": {  # ´ acute
        "a": "\u00E1", "e": "\u00E9", "i": "\u00ED", "o": "\u00F3",
        "u": "\u00FA", "y": "\u00FD", "c": "\u0107", "n": "\u0144",
        "s": "\u015B", "z": "\u017A",
        "A": "\u00C1", "E": "\u00C9", "I": "\u00CD", "O": "\u00D3",
        "U": "\u00DA", "Y": "\u00DD", "C": "\u0106", "N": "\u0143",
        "S": "\u015A", "Z": "\u0179",
    },
    "\u00A8": {  # ¨ diaeresis
        "a": "\u00E4", "e": "\u00EB", "i": "\u00EF", "o": "\u00F6",
        "u": "\u00FC", "y": "\u00FF",
        "A": "\u00C4", "E": "\u00CB", "I": "\u00CF", "O": "\u00D6",
        "U": "\u00DC", "Y": "\u0178",
    },
    "\u00AF": {  # ¯ macron
        "a": "\u0101", "e": "\u0113", "i": "\u012B", "o": "\u014D",
        "u": "\u016B",
        "A": "\u0100", "E": "\u0112", "I": "\u012A", "O": "\u014C",
        "U": "\u016A",
    },
}


# ── YAML loading ─────────────────────────────────────────────────────────────

def preprocess_yaml(text):
    """Fix YAML anchor names containing '+' (not allowed by spec)."""
    text = re.sub(r'(&|\*)([A-Z]+)\+([A-Z]+)', r'\1\2_\3', text)
    return text


def make_loader(base_path):
    """Create a YAML loader that handles !include directives."""
    class Loader(yaml.SafeLoader):
        pass

    def include_constructor(loader, node):
        val = loader.construct_scalar(node).strip()
        if "#" in val:
            inc_file, anchor_path = val.split("#", 1)
        else:
            inc_file, anchor_path = val, None

        inc_path = base_path / inc_file
        if not inc_path.exists():
            return None
        try:
            data = load_yaml(inc_path)
            if anchor_path and isinstance(data, dict):
                for key in anchor_path.split("#"):
                    if isinstance(data, dict):
                        data = data.get(key)
                    else:
                        return None
            return data
        except Exception:
            return None

    Loader.add_constructor("!include", include_constructor)
    return Loader


def normalize_block_scalars(text):
    """Fix indentation in YAML literal block scalars (|)."""
    lines = text.splitlines(keepends=True)
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r':\s*\|\s*$', line.rstrip()):
            result.append(line)
            i += 1
            block_lines = []
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
                    break
                block_lines.append(bl)
                i += 1
            indents = [len(l.rstrip('\n\r')) - len(l.rstrip('\n\r').lstrip(' '))
                       for l in block_lines if l.strip()]
            if indents:
                min_indent = min(indents)
                for bl in block_lines:
                    if bl.strip() == '':
                        result.append(bl)
                    else:
                        cur_indent = len(bl.rstrip('\n\r')) - len(bl.rstrip('\n\r').lstrip(' '))
                        if cur_indent > min_indent:
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
    raw = path.read_text(encoding="utf-8")
    normalized = normalize_block_scalars(raw)
    preprocessed = preprocess_yaml(normalized)
    return yaml.load(preprocessed, Loader=make_loader(path.parent)) or {}


# ── Layout parsing ───────────────────────────────────────────────────────────

def parse_layer(layer_str):
    """Parse a layer string → list of rows, each a list of characters."""
    if not layer_str:
        return []
    rows = []
    for line in layer_str.strip().splitlines():
        keys = line.split()
        if keys:
            rows.append(keys)
    return rows


def detect_layout_type(rows):
    """Detect ANSI vs ISO vs NO_NUMROW from row key counts."""
    lens = [len(r) for r in rows]
    if len(rows) == 4:
        if lens == [13, 13, 11, 10]:
            return "ANSI"
        if lens[0] == 13 and lens[1] == 12 and lens[2] == 12:
            return "ISO"
    if len(rows) == 3 and lens[0] == 13 and lens[1] == 11 and lens[2] == 10:
        return "NO_NUMROW"  # e.g. Ossetic: only letter rows, no number row
    return None


# Default number row (used when layout has no number row)
DEFAULT_NUMROW = list("] 1 2 3 4 5 6 7 8 9 0 - =".split())
DEFAULT_NUMROW_SHIFT = list("[ ! \" № % : , . ; ( ) _ +".split())


def get_keycodes(layout_type, rows):
    """Map each row/col position to a macOS keycode."""
    if layout_type == "NO_NUMROW":
        # 3-row layout: map to letter rows only, number row is unset
        template = ANSI_KEYCODES[1:]  # skip number row keycodes
    elif layout_type == "ISO":
        template = ISO_KEYCODES
    else:
        template = ANSI_KEYCODES

    mapping = {}
    for row_idx, row in enumerate(rows):
        if row_idx >= len(template):
            break
        codes = template[row_idx]
        for col_idx, char in enumerate(row):
            if col_idx < len(codes):
                mapping[codes[col_idx]] = char
    return mapping


# ── XML generation ───────────────────────────────────────────────────────────

def xml_escape_output(char):
    """Escape a character for use in .keylayout output attribute."""
    if char is None:
        return ""
    cp = ord(char) if len(char) == 1 else None
    if cp is not None and (cp < 0x20 or cp == 0x7F):
        return f"&#x{cp:04X};"
    # XML special chars
    return html.escape(char, quote=True)


def build_key_element(code, char, dead_keys=None, state_prefix=""):
    """Build a <key> XML element."""
    if dead_keys and char in dead_keys:
        state_name = f"state_{state_prefix}_{ord(char):04X}"
        return f'      <key code="{code}" action="{state_name}"/>'
    out = xml_escape_output(char)
    return f'      <key code="{code}" output="{out}"/>'


def generate_keylayout(name, display_name, layers, dead_keys_by_layer=None, layout_type="ANSI"):
    """Generate a complete .keylayout XML string."""

    # Unique negative ID from name hash
    kb_id = -(abs(int(hashlib.md5(name.encode()).hexdigest()[:8], 16)) % 90000 + 10000)

    dead_keys_by_layer = dead_keys_by_layer or {}

    # ── Determine which layers are identical (via YAML anchors) ──
    # Map layer name → canonical index
    LAYER_NAMES = [
        "default", "shift", "caps", "caps+shift",
        "alt", "alt+shift", "alt+caps",
        "cmd", "cmd+shift", "cmd+alt", "cmd+alt+shift",
    ]

    available_layers = {}
    for ln in LAYER_NAMES:
        if ln in layers and layers[ln] is not None:
            available_layers[ln] = layers[ln]
        elif ln == "caps+shift" and "shift" in layers:
            available_layers[ln] = layers["shift"]
        elif ln == "alt+caps" and "alt" in layers:
            available_layers[ln] = layers["alt"]
        elif ln == "cmd+alt" and "cmd" in layers:
            available_layers[ln] = layers["cmd"]
        elif ln == "cmd+alt+shift" and "cmd+shift" in layers:
            available_layers[ln] = layers["cmd+shift"]
        elif "default" in layers:
            available_layers[ln] = layers["default"]

    # Deduplicate: group layers that have identical content
    unique_layers = []
    layer_to_index = {}
    for ln in LAYER_NAMES:
        content = available_layers.get(ln, "")
        found = False
        for idx, (_, existing_content) in enumerate(unique_layers):
            if content == existing_content:
                layer_to_index[ln] = idx
                found = True
                break
        if not found:
            layer_to_index[ln] = len(unique_layers)
            unique_layers.append((ln, content))

    # ── XML generation ──
    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append('<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">')
    xml.append(f'<keyboard group="126" id="{kb_id}" name="{html.escape(display_name)}" maxout="2">')
    xml.append('  <layouts>')
    xml.append(f'    <layout first="0" last="0" mapSet="ANSI" modifiers="Modifiers"/>')
    xml.append('  </layouts>')

    # ── Modifier map ──
    xml.append('  <modifierMap id="Modifiers" defaultIndex="0">')

    modifier_specs = [
        ("default",        ['']),
        ("shift",          ['anyShift']),
        ("caps",           ['caps']),
        ("caps+shift",     ['caps anyShift']),
        ("alt",            ['anyOption']),
        ("alt+shift",      ['anyOption anyShift']),
        ("alt+caps",       ['caps anyOption']),
        ("cmd",            ['command']),
        ("cmd+shift",      ['command anyShift']),
        ("cmd+alt",        ['command anyOption']),
        ("cmd+alt+shift",  ['command anyOption anyShift']),
    ]

    for layer_name, mod_keys_list in modifier_specs:
        idx = layer_to_index.get(layer_name, 0)
        xml.append(f'    <keyMapSelect mapIndex="{idx}">')
        for mk in mod_keys_list:
            xml.append(f'      <modifier keys="{mk}"/>')
        xml.append('    </keyMapSelect>')

    xml.append('  </modifierMap>')

    # ── Key map set ──
    xml.append('  <keyMapSet id="ANSI">')

    all_dead_chars = set()
    for idx, (layer_name, layer_content) in enumerate(unique_layers):
        rows = parse_layer(layer_content)
        lt = detect_layout_type(rows) or layout_type
        key_mapping = get_keycodes(lt, rows)
        dk = dead_keys_by_layer.get(layer_name, set())

        xml.append(f'    <keyMap index="{idx}">')

        # Character keys from layout
        for code, char in sorted(key_mapping.items()):
            xml.append(build_key_element(code, char, dk, layer_name))
            if dk and char in dk:
                all_dead_chars.add(char)

        # Special keys
        for code, out in sorted(SPECIAL_KEYS.items()):
            if code not in key_mapping:
                out_esc = xml_escape_output(out)
                xml.append(f'      <key code="{code}" output="{out_esc}"/>')

        # Numpad keys
        for code, out in sorted(NUMPAD_KEYS.items()):
            if code not in key_mapping:
                out_esc = xml_escape_output(out)
                xml.append(f'      <key code="{code}" output="{out_esc}"/>')

        xml.append('    </keyMap>')

    xml.append('  </keyMapSet>')

    # ── Dead key actions ──
    if all_dead_chars:
        xml.append('  <actions>')
        for dc in sorted(all_dead_chars):
            compositions = DEAD_KEY_COMPOSITIONS.get(dc, {})
            for layer_name in LAYER_NAMES:
                dk = dead_keys_by_layer.get(layer_name, set())
                if dc in dk:
                    state_name = f"state_{layer_name}_{ord(dc):04X}"
                    xml.append(f'    <action id="{state_name}">')
                    xml.append(f'      <when state="none" next="{state_name}"/>')
                    for trigger, result in sorted(compositions.items()):
                        out = xml_escape_output(result)
                        xml.append(f'      <when state="{state_name}" output="{out}"/>')
                    xml.append('    </action>')
        xml.append('  </actions>')

        xml.append('  <terminators>')
        for dc in sorted(all_dead_chars):
            for layer_name in LAYER_NAMES:
                dk = dead_keys_by_layer.get(layer_name, set())
                if dc in dk:
                    state_name = f"state_{layer_name}_{ord(dc):04X}"
                    out = xml_escape_output(dc)
                    xml.append(f'    <when state="{state_name}" output="{out}"/>')
        xml.append('  </terminators>')

    xml.append('</keyboard>')
    return "\n".join(xml) + "\n"


# ── Main ─────────────────────────────────────────────────────────────────────

def process_file(yaml_path, check_only=False):
    """Process a single *-macos*.yaml file → .keylayout"""
    data = load_yaml(yaml_path)
    if not data or "macOS" not in data:
        print(f"  SKIP {yaml_path.name}: no macOS section")
        return None

    macos = data["macOS"]
    layers = macos.get("primary", {}).get("layers", {})
    if not layers or "default" not in layers:
        print(f"  SKIP {yaml_path.name}: no default layer")
        return None

    # Validate row structure
    default_rows = parse_layer(layers["default"])
    lt = detect_layout_type(default_rows)
    if lt is None:
        lens = [len(r) for r in default_rows]
        print(f"  WARN {yaml_path.name}: unusual row structure {lens}")
        lt = "ANSI"  # fallback

    # Display name
    names = data.get("displayNames", {})
    # Try native → Russian → English
    native_key = [k for k in names if k not in ("en", "eng", "ru", "rus")]
    if native_key:
        display_name = names.get(native_key[0], "")
    else:
        display_name = ""
    ru_name = names.get("ru") or names.get("rus", "")
    en_name = names.get("en") or names.get("eng", "")

    # Format: "Native (Russian)" or just the name
    if display_name and ru_name and display_name != ru_name:
        full_name = f"{display_name} — {ru_name}"
    elif ru_name:
        full_name = ru_name
    elif en_name:
        full_name = en_name
    else:
        full_name = yaml_path.stem

    # Dead keys
    dead_keys_cfg = macos.get("deadKeys", {})
    dead_keys_by_layer = {}
    for dk_layer, dk_chars in (dead_keys_cfg or {}).items():
        if dk_chars:
            dead_keys_by_layer[dk_layer] = set(dk_chars)

    # File stem for output name
    stem = yaml_path.stem.replace("-macos", "")
    output_name = f"{stem}.keylayout"

    row_lens = [len(r) for r in default_rows]
    status = f"OK ({lt}, rows: {row_lens})"

    if check_only:
        print(f"  CHECK {yaml_path.name}: {status} → {output_name}")
        return None

    print(f"  BUILD {yaml_path.name}: {status} → {output_name}")
    xml_content = generate_keylayout(
        name=stem,
        display_name=full_name,
        layers=layers,
        dead_keys_by_layer=dead_keys_by_layer,
        layout_type=lt,
    )

    return (output_name, xml_content)


def main():
    check_only = "--check" in sys.argv
    lang_filter = None
    if "--lang" in sys.argv:
        idx = sys.argv.index("--lang")
        if idx + 1 < len(sys.argv):
            lang_filter = sys.argv[idx + 1]

    if not LAYOUT.exists():
        print(f"ERROR: {LAYOUT} not found")
        sys.exit(1)

    if not check_only:
        DIST.mkdir(parents=True, exist_ok=True)

    yaml_files = sorted(LAYOUT.glob("*/*-macos*.yaml"))
    if lang_filter:
        yaml_files = [f for f in yaml_files if f.parent.name == lang_filter]

    if not yaml_files:
        print("No macOS YAML files found")
        sys.exit(1)

    print(f"Found {len(yaml_files)} macOS layout(s):\n")
    results = []
    errors = []

    for yf in yaml_files:
        try:
            result = process_file(yf, check_only)
            if result:
                results.append(result)
        except Exception as e:
            print(f"  ERROR {yf.name}: {e}")
            errors.append((yf.name, str(e)))

    if not check_only and results:
        print(f"\nWriting {len(results)} .keylayout file(s) to {DIST}/")
        for filename, content in results:
            out_path = DIST / filename
            out_path.write_text(content, encoding="utf-8")
            print(f"  → {out_path.relative_to(ROOT)}")

    print(f"\nDone: {len(results)} built, {len(errors)} errors")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
