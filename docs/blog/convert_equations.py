#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert mathematical equations to LaTeX format in blog posts
"""

import re
import os

def convert_file(filepath):
    """Convert equations in a single file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # File-specific conversions based on filename
    filename = os.path.basename(filepath)

    if filename == '20031028-pengukuran-suhu.qmd':
        # Equation 4.2
        content = content.replace(
            'RT = Ro[1+ a (T-To)] ……………….(4.2)',
            r'$$R_T = R_o[1+ a (T-T_o)] \tag{4.2}$$'
        )
        content = re.sub(
            r'dimana \(t-To\) kecil',
            r'dimana $(t-T_o)$ kecil',
            content
        )
        content = re.sub(
            r'RT adalah hambatan',
            r'$R_T$ adalah hambatan',
            content
        )
        content = re.sub(
            r'Ro adalah koefisin suhu referensi To',
            r'$R_o$ adalah koefisin suhu referensi $T_o$',
            content
        )
        content = re.sub(
            r'a adalah koefisien suhu dari hambatan disekitar To',
            r'$a$ adalah koefisien suhu dari hambatan disekitar $T_o$',
            content
        )
        # Equation 4.3
        content = content.replace(
            'RT = Ro [1 + a (t-To) + b (T-To)2] ….(4.3)',
            r'$$R_T = R_o [1 + a (t-T_o) + b (T-T_o)^2] \tag{4.3}$$'
        )
        content = re.sub(
            r'Jadi nilai koefisien a dan b dapat',
            r'Jadi nilai koefisien $a$ dan $b$ dapat',
            content
        )
        # Equation 4.4
        content = content.replace(
            'R = a exp (b/T)',
            r'$$R = a \exp(b/T) \tag{4.4}$$'
        )
        content = re.sub(
            r'dimana a dan b adalah konstan dan T adalah suhu',
            r'dimana $a$ dan $b$ adalah konstan dan $T$ adalah suhu',
            content
        )
        # Equation 4.5
        content = re.sub(
            r'R = Ro exp \[b/T-b/To\] ……………\.\(4\.5\)',
            r'$$R = R_o \exp\left[\\frac{b}{T}-\\frac{b}{T_o}\right] \\tag{4.5}$$',
            content
        )
        content = re.sub(
            r'suhu referensi, To digunakan',
            r'suhu referensi, $T_o$ digunakan',
            content
        )

    elif filename == '20040103-menghitung-radiasi-matahari.qmd':
        # Equation 1
        content = re.sub(
            r'Ra = \(24\(60\)\)/π \\\* Gsc \\\* dr \\\* \[ωs \\\* sin\(φ\) \\\* sin\(δ\) \+ cos\(φ\) \\\* cos\(δ\) \\\* sin\(ωs\)\] \(\*\*Persamaan 1\*\*\)',
            r'$$R_a = \\frac{24(60)}{\\pi} G_{sc} d_r [\\omega_s \\sin(\\phi) \\sin(\\delta) + \\cos(\\phi) \\cos(\\delta) \\sin(\\omega_s)] \\tag{1}$$',
            content
        )
        # Equation 2
        content = re.sub(
            r'evaporasi \[mm hari-1\] = 0,408 x Radiasi \[MJ m-2 hari-1\] \(\*\*Persamaan 2\*\*\)',
            r'$$\\text{evaporasi [mm hari}^{-1}\\text{]} = 0.408 \\times \\text{Radiasi [MJ m}^{-2}\\text{ hari}^{-1}\\text{]} \\tag{2}$$',
            content
        )
        # Equation 3
        content = re.sub(
            r'\[Radians\] = π/180 \\\* \[decimal degrees\] \(\*\*Persamaan 3\*\*\)',
            r'$$[\\text{Radians}] = \\frac{\\pi}{180} \\times [\\text{decimal degrees}] \\tag{3}$$',
            content
        )
        # Equation 4
        content = re.sub(
            r'dr = 1 \+ 0\.033 \\\* cos\(2π/365 \\\* J\) \(\*\*Persamaan 4\*\*\)',
            r'$$d_r = 1 + 0.033 \\cos\\left(\\frac{2\\pi}{365} J\\right) \\tag{4}$$',
            content
        )
        # Equation 5
        content = re.sub(
            r'δ = 0\.409 \\\* sin\(2π/365 \\\* J - 1\.39\) \(\*\*Persamaan 5\*\*\)',
            r'$$\\delta = 0.409 \\sin\\left(\\frac{2\\pi}{365} J - 1.39\\right) \\tag{5}$$',
            content
        )

    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Main execution
if __name__ == '__main__':
    blog_dir = r'C:\Users\benny\OneDrive\Documents\Github\site\docs\blog'

    files_to_convert = [
        '20031028-pengukuran-suhu.qmd',
        '20040103-menghitung-radiasi-matahari.qmd',
    ]

    for filename in files_to_convert:
        filepath = os.path.join(blog_dir, filename)
        if os.path.exists(filepath):
            if convert_file(filepath):
                print(f'Converted: {filename}')
            else:
                print(f'No changes: {filename}')
        else:
            print(f'File not found: {filename}')
