import zipfile
import xml.etree.ElementTree as ET
import os

def read_xlsx(file_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        # Read shared strings
        with z.open('xl/sharedStrings.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            shared_strings = []
            for si in root.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                t = si.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                if t is not None:
                    shared_strings.append(t.text)
                else:
                    # Handle rich text
                    text = ""
                    for r in si.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}r'):
                        rt = r.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                        if rt is not None:
                            text += rt.text
                    shared_strings.append(text)

        # Read workbook to get sheet names
        with z.open('xl/workbook.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            sheets = []
            for sheet in root.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheets').findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
                sheets.append(sheet.get('name'))

        # Read each sheet
        for i, sheet_name in enumerate(sheets):
            print(f"\n--- Sheet: {sheet_name} ---")
            with z.open(f'xl/worksheets/sheet{i+1}.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                sheet_data = root.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheetData')
                
                # Get max column
                max_col = 0
                for row in sheet_data.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                    for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                        ref = c.get('r')
                        col_str = "".join([char for char in ref if char.isalpha()])
                        col_idx = 0
                        for char in col_str:
                            col_idx = col_idx * 26 + (ord(char) - ord('A') + 1)
                        max_col = max(max_col, col_idx)
                
                for row in sheet_data.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                    row_idx = row.get('r')
                    cells = {}
                    for c in row.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                        ref = c.get('r')
                        col_str = "".join([char for char in ref if char.isalpha()])
                        col_idx = 0
                        for char in col_str:
                            col_idx = col_idx * 26 + (ord(char) - ord('A') + 1)
                        
                        cell_type = c.get('t')
                        v = c.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
                        val = ""
                        if v is not None:
                            val = v.text
                            if cell_type == 's':
                                val = shared_strings[int(val)]
                        cells[col_idx] = val
                    
                    row_vals = [cells.get(c, "") for c in range(1, max_col + 1)]
                    print("| " + " | ".join([str(v) if v is not None else "" for v in row_vals]) + " |")

if __name__ == "__main__":
    read_xlsx("/Users/ali/Documents/Science/ios-system/transfer-temp/Ulci_compact_cyrillic_layout (V Kh).xlsx")
