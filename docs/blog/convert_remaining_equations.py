#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert remaining mathematical equations to LaTeX format
"""

import re
import sys

# Set UTF-8 encoding for stdout
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def convert_pengukuran_suhu():
    """Convert equations in 20031028-pengukuran-suhu.qmd"""
    filepath = r'C:\Users\benny\OneDrive\Documents\Github\site\docs\blog\20031028-pengukuran-suhu.qmd'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Equation 4.2 - handle with regex to catch any ellipsis variation
    content = re.sub(
        r'RT = Ro\[1\+ a \(T-To\)\] [.…]+\(4\.2\)',
        r'$$R_T = R_o[1+ a (T-T_o)] \\tag{4.2}$$',
        content
    )

    # Update variable descriptions after 4.2
    content = re.sub(
        r'dimana \(t-To\) kecil',
        r'dimana $(t-T_o)$ kecil',
        content
    )
    content = re.sub(
        r'RT adalah hambatan logam',
        r'$R_T$ adalah hambatan logam',
        content
    )
    content = re.sub(
        r'Ro adalah koefisin suhu referensi To',
        r'$R_o$ adalah koefisin suhu referensi $T_o$',
        content
    )
    content = re.sub(
        r'a adalah koefisien suhu dari hambatan disekitar To\.',
        r'$a$ adalah koefisien suhu dari hambatan disekitar $T_o$.',
        content
    )

    # Equation 4.3
    content = re.sub(
        r'RT = Ro \[1 \+ a \(t-To\) \+ b \(T-To\)2\] [.…]+\(4\.3\)',
        r'$$R_T = R_o [1 + a (t-T_o) + b (T-T_o)^2] \\tag{4.3}$$',
        content
    )
    content = re.sub(
        r'Jadi nilai koefisien a dan b dapat dicari',
        r'Jadi nilai koefisien $a$ dan $b$ dapat dicari',
        content
    )

    # Equation 4.5
    content = re.sub(
        r'Jika  suhu referensi, To digunakan',
        r'Jika  suhu referensi, $T_o$ digunakan',
        content
    )
    content = re.sub(
        r'R = Ro exp \[b/T-b/To\] [.…]+\(4\.5\)',
        r'$$R = R_o \\exp\\left[\\frac{b}{T}-\\frac{b}{T_o}\\right] \\tag{4.5}$$',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Converted equations in 20031028-pengukuran-suhu.qmd')
        return True
    else:
        print('No changes in 20031028-pengukuran-suhu.qmd')
        return False

def convert_biomassa_padi():
    """Convert equations in 20040427-model-pendugaan-biomassa-tanaman-padi.qmd"""
    filepath = r'C:\Users\benny\OneDrive\Documents\Github\site\docs\blog\20040427-model-pendugaan-biomassa-tanaman-padi.qmd'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # These equations were attempted before, verify they're converted
    conversions = [
        (r'Qint = Qs \(1 – exp -k LAI\)',
         r'$$Q_{\\text{int}} = Q_s (1 - \\exp(-k \\cdot LAI))$$'),
        (r'Qint = Radiasi diintersepsi',
         r'$Q_{\\text{int}}$ = Radiasi diintersepsi'),
        (r'Qs = Radiasi surya',
         r'$Q_s$ = Radiasi surya'),
        (r'k = koefisien pemadaman',
         r'$k$ = koefisien pemadaman'),
        (r'LAI = indek luas daun',
         r'$LAI$ = indek luas daun'),
        (r'dW = LUE \. Qint',
         r'$$dW = LUE \\cdot Q_{\\text{int}}$$'),
        (r'dW = pertambahan berat total',
         r'$dW$ = pertambahan berat total'),
        (r'LUE = efisiensi penggunaan',
         r'$LUE$ = efisiensi penggunaan'),
        (r'Rm = km \* Wx \* Q10',
         r'$$R_m = k_m \\times W_x \\times Q_{10}$$'),
        (r'Rm = Kehilangan biomassa',
         r'$R_m$ = Kehilangan biomassa'),
        (r'km = koefisensi respirasi',
         r'$k_m$ = koefisensi respirasi'),
        (r'Wx = biomassa organ x',
         r'$W_x$ = biomassa organ x'),
        (r'Q10 = temperature quotient',
         r'$Q_{10}$ = temperature quotient'),
    ]

    for old, new in conversions:
        content = re.sub(old, new, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Verified/converted equations in 20040427-model-pendugaan-biomassa-tanaman-padi.qmd')
        return True
    else:
        print('Already converted: 20040427-model-pendugaan-biomassa-tanaman-padi.qmd')
        return False

def convert_deret_hari_kering():
    """Convert equations in 20040522-pendugaan-deret-hari-kering.qmd"""
    filepath = r'C:\Users\benny\OneDrive\Documents\Github\site\docs\blog\20040522-pendugaan-deret-hari-kering.qmd'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Verify these equations are converted
    conversions = [
        (r'Prerata = 0,051 p\(DHK ≤10\) \+0,041 p\(DHK ≥ 15\) \+ 0,97 p\(DHK ≥ 10\)',
         r'$$P_{\\text{rerata}} = 0.051 \\cdot p(DHK \\leq 10) + 0.041 \\cdot p(DHK \\geq 15) + 0.97 \\cdot p(DHK \\geq 10)$$'),
        (r'Y = 0,407 – 0,00259 X1 – 0,009X2 \+ 0,0426X3',
         r'$$Y = 0.407 - 0.00259 X_1 - 0.009X_2 + 0.0426X_3$$'),
    ]

    for old, new in conversions:
        content = re.sub(old, new, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Verified/converted equations in 20040522-pendugaan-deret-hari-kering.qmd')
        return True
    else:
        print('Already converted: 20040522-pendugaan-deret-hari-kering.qmd')
        return False

if __name__ == '__main__':
    print("Converting remaining equations to LaTeX format...\n")
    convert_pengukuran_suhu()
    convert_biomassa_padi()
    convert_deret_hari_kering()
    print("\nCompleted conversion of partially finished files")
