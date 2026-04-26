import sys
from pathlib import Path
sys.path.append('scripts')
import build

# Reliable English names and families
ENG_DATA = {
    "alt": ("Altai", "Turkic"),
    "ava": ("Avar", "Caucasian"),
    "bak": ("Bashkir", "Turkic"),
    "bua": ("Buryat", "Mongolic"),
    "chv": ("Chuvash", "Turkic"),
    "gag": ("Gagauz", "Turkic"),
    "gld": ("Nanai", "Tungusic"),
    "kjh": ("Khakas", "Turkic"),
    "kom": ("Komi", "Uralic"),
    "oss": ("Ossetian", "Iranian"),
    "rus": ("Russian", "Slavic"),
    "tat": ("Tatar", "Turkic"),
    "tle": ("Teleut", "Turkic"),
    "tyv": ("Tuvan", "Turkic"),
    "xal": ("Kalmyk", "Mongolic"),
    "xdq": ("Kaitag", "Caucasian"),
    "ykt": ("Yakut", "Turkic"),
}

def generate_svg(lang_data, lp_map, output_path, lang='ru'):
    # Header and basic styles
    width = 680
    row_height = 42
    header_height = 86
    total_height = header_height + len(lang_data) * row_height + 20
    
    title = "Языки в репозитории ios-system-keyboard" if lang == 'ru' else "Languages in ios-system-keyboard repository"
    headers = ["Код ISO", "Язык", "Самоназвание", "Дизайн"] if lang == 'ru' else ["ISO Code", "Language", "Native Name", "Design"]
    
    svg = [f'<svg width="100%" viewBox="0 0 {width} {total_height}" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">']
    svg.append(f'<text font-size="16" font-weight="500" fill="#1a1a1a" x="{width//2}" y="36" text-anchor="middle">{title}</text>')
    
    # Header row
    y = 52
    cols = [
        (24, 76, headers[0]),
        (108, 180, headers[1]),
        (296, 180, headers[2]),
        (484, 172, headers[3])
    ]
    for x, w, label in cols:
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="4" fill="#D3D1C7" stroke="#5F5E5A" stroke-width="0.5"/>')
        svg.append(f'<text font-size="12" fill="#444441" x="{x + w//2}" y="{y + 19}" text-anchor="middle">{label}</text>')
    
    # Colors for rows (rotating)
    colors = [
        ("#E1F5EE", "#0F6E56", "#085041"), # Green
        ("#E6F1FB", "#185FA5", "#0C447C"), # Blue
        ("#EEEDFE", "#534AB7", "#3C3489"), # Purple
        ("#FAEEDA", "#854F0B", "#633806"), # Orange
        ("#FAECE7", "#993C1D", "#712B13"), # Pinkish
        ("#EAF3DE", "#3B6D11", "#27500A"), # Light Green
        ("#FBEAF0", "#993556", "#72243E"), # Pink
        ("#F1EFE8", "#5F5E5A", "#444441"), # Grey
    ]
    
    y = 86
    for i, lang_obj in enumerate(lang_data):
        c_bg, c_stroke, c_text = colors[i % len(colors)]
        
        code = lang_obj["code"]
        ru_name = lang_obj["native"]
        native_name = lang_obj["name"]
        en_name, en_family = ENG_DATA.get(code, (code.capitalize(), "Other"))
        
        col1_text = ru_name if lang == 'ru' else en_name
        col2_text = native_name
        family = build.FAMILY.get(code, ("Другие", "#888"))[0] if lang == 'ru' else en_family
        
        # ISO Code
        svg.append(f'<!-- {code} -->')
        svg.append(f'<rect x="24" y="{y}" width="76" height="38" rx="4" fill="{c_bg}" stroke="{c_stroke}" stroke-width="0.5"/>')
        svg.append(f'<text font-size="14" font-weight="500" fill="{c_text}" x="62" y="{y + 24}" text-anchor="middle">{code}</text>')
        
        # Language Name
        svg.append(f'<rect x="108" y="{y}" width="180" height="38" rx="4" fill="{c_bg}" stroke="{c_stroke}" stroke-width="0.5"/>')
        svg.append(f'<text font-size="14" font-weight="500" fill="{c_text}" x="198" y="{y + 17}" text-anchor="middle">{col1_text}</text>')
        svg.append(f'<text font-size="11" fill="{c_text}" x="198" y="{y + 31}" text-anchor="middle">{family}</text>')
        
        # Native Name
        svg.append(f'<rect x="296" y="{y}" width="180" height="38" rx="4" fill="{c_bg}" stroke="{c_stroke}" stroke-width="0.5"/>')
        svg.append(f'<text font-size="12" fill="{c_text}" x="386" y="{y + 23}" text-anchor="middle">{col2_text}</text>')
        
        # Design
        svg.append(f'<rect x="484" y="{y}" width="172" height="38" rx="4" fill="{c_bg}" stroke="{c_stroke}" stroke-width="0.5"/>')
        
        features = []
        lids = [l["id"] for l in lang_obj["layouts"]]
        if any("3-rows" in lid or lid == code for lid in lids): features.append("3-rows" if lang == 'en' else "3-ряда")
        if any("4-rows" in lid for lid in lids): features.append("4-rows" if lang == 'en' else "4-ряда")
        if any("longpress" in lid.lower() for lid in lids) or (code in lp_map): features.append("longpress" if lang == 'en' else "лонгпресс")
        
        # Check for macOS
        macos_dir = Path(f'layout/{code}')
        if any("macos" in f.name.lower() for f in macos_dir.glob("*.yaml")):
            features.append("macOS" if lang == 'en' else "МакОС")
            
        f_text = ", ".join(features)
        if len(f_text) > 25:
            mid = f_text.find(", ", len(f_text)//2 - 5)
            if mid != -1:
                svg.append(f'<text font-size="11" fill="{c_text}" x="570" y="{y + 17}" text-anchor="middle">{f_text[:mid+1]}</text>')
                svg.append(f'<text font-size="11" fill="{c_text}" x="570" y="{y + 31}" text-anchor="middle">{f_text[mid+2:]}</text>')
            else:
                svg.append(f'<text font-size="11" fill="{c_text}" x="570" y="{y + 23}" text-anchor="middle">{f_text}</text>')
        else:
            svg.append(f'<text font-size="11" fill="{c_text}" x="570" y="{y + 23}" text-anchor="middle">{f_text}</text>')
            
        y += row_height

    svg.append('</svg>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))

if __name__ == "__main__":
    data, lp_map = build.discover()
    all_langs = []
    for group in data:
        all_langs.extend(group["langs"])
    
    # Sort by ISO code for consistency in both versions
    all_langs.sort(key=lambda x: x["code"])
    
    generate_svg(all_langs, lp_map, "assets/gif/languages-ru.svg", lang='ru')
    generate_svg(all_langs, lp_map, "assets/gif/languages-en.svg", lang='en')
    
    print(f"✅ Generated SVGs (RU/EN) with {len(all_langs)} languages")
