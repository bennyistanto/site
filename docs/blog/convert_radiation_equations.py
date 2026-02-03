#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert mathematical equations to LaTeX format in radiation blog post
"""

import re

def convert_radiation_file():
    """Convert equations in 20040103-menghitung-radiasi-matahari.qmd"""
    filepath = r'C:\Users\benny\OneDrive\Documents\Github\site\docs\blog\20040103-menghitung-radiasi-matahari.qmd'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Store original for comparison
    original_content = content

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

    # Equation 6 (multi-line)
    content = re.sub(
        r'J = INTEGER \(275 M / 9 - 30 \+ D\) - 2\n\nIF \(M <3\) THEN J = J \+ 2\n\nIF \("tahun kabisat" and \(M> 2\)\) THEN J = J \+ 1 \(\*\*Persamaan 6\*\*\)',
        r'$$J = \\text{INTEGER}\\left(\\frac{275M}{9} - 30 + D\\right) - 2$$\n\n$$\\text{IF } (M < 3) \\text{ THEN } J = J + 2$$\n\n$$\\text{IF ("tahun kabisat" and } (M > 2)) \\text{ THEN } J = J + 1 \\tag{6}$$',
        content
    )

    # Equation 7
    content = re.sub(
        r'ωs = arccos\[-tan\(φ\) \\\* tan\(δ\)\] \(\*\*Persamaan 7\*\*\)',
        r'$$\\omega_s = \\arccos[-\\tan(\\phi) \\tan(\\delta)] \\tag{7}$$',
        content
    )

    # Equation 8
    content = re.sub(
        r'ωs = π/2 - arctan\[\(-tan\(φ\) \\\* tan\(δ\)\)/X\^0\.5\] \(\*\*Persamaan 8\*\*\)',
        r'$$\\omega_s = \\frac{\\pi}{2} - \\arctan\\left[\\frac{-\\tan(\\phi) \\tan(\\delta)}{X^{0.5}}\\right] \\tag{8}$$',
        content
    )

    # Equation 9
    content = re.sub(
        r'\* X = 1 - \[tan\(φ\)\]\^2 \[tan\(δ\)\]\^2 \(\*\*Persamaan 9\*\*\)\n\n  dan X = 0\.00001 jika X ≤ 0',
        r'$$X = 1 - [\\tan(\\phi)]^2 [\\tan(\\delta)]^2 \\tag{9}$$\n\n  dan $X = 0.00001$ jika $X \\leq 0$',
        content
    )

    # Equation 10
    content = re.sub(
        r'Ra = \(12\(60\)\)/π \\\* Gsc \\\* dr \\\* \[\(ω2 - ω1\) \\\* sin\(φ\) \\\* sin\(δ\) \+ cos\(φ\) \\\* cos\(δ\) \\\* \(sin\(ω2\)-sin\(ω1\)\)\] \(\*\*Persamaan 10\*\*\)',
        r'$$R_a = \\frac{12(60)}{\\pi} G_{sc} d_r [(\\omega_2 - \\omega_1) \\sin(\\phi) \\sin(\\delta) + \\cos(\\phi) \\cos(\\delta) (\\sin(\\omega_2)-\\sin(\\omega_1))] \\tag{10}$$',
        content
    )

    # Equations 11 and 12
    content = re.sub(
        r'ω1 = ω - \(πt1/24\) \(\*\*Persamaan 11\*\*\)\n\nω2 = ω \+ \(πt1/24\) \(\*\*Persamaan 12\*\*\)',
        r'$$\\omega_1 = \\omega - \\frac{\\pi t_1}{24} \\tag{11}$$\n\n$$\\omega_2 = \\omega + \\frac{\\pi t_1}{24} \\tag{12}$$',
        content
    )

    # Equation 13
    content = re.sub(
        r'ω = π/12 \\\* \[\(t \+ 0\.06667 \\\* \(Lz - Lm\) \+ Sc\) - 12\] \(\*\*Persamaan 13\*\*\)',
        r'$$\\omega = \\frac{\\pi}{12} [(t + 0.06667 (L_z - L_m) + S_c) - 12] \\tag{13}$$',
        content
    )

    # Equation 14
    content = re.sub(
        r'Sc = 0\.1645 \\\* sin\(2 b\) - 0\.1255 \\\* cos\(b\) - 0\.025 sin\(b\) \(\*\*Persamaan 14\*\*\)',
        r'$$S_c = 0.1645 \\sin(2b) - 0.1255 \\cos(b) - 0.025 \\sin(b) \\tag{14}$$',
        content
    )

    # Equation 15
    content = re.sub(
        r'b = \(2π\(J-81\)\)/364 \(\*\*Persamaan 15\*\*\)',
        r'$$b = \\frac{2\\pi(J-81)}{364} \\tag{15}$$',
        content
    )

    # Equation 16
    content = re.sub(
        r'N = 24/π \\\* ωs \(\*\*Persamaan 16\*\*\)',
        r'$$N = \\frac{24}{\\pi} \\omega_s \\tag{16}$$',
        content
    )

    # Equation 17
    content = re.sub(
        r'Rs = \(as \+ bs \\\* \(n/N\)\) \\\* Ra \(\*\*Persamaan 17\*\*\)',
        r'$$R_s = (a_s + b_s \\frac{n}{N}) R_a \\tag{17}$$',
        content
    )

    # Equation 18
    content = re.sub(
        r'Rso = \(as \+ bs\) Ra \(\*\*Persamaan 18\*\*\)',
        r'$$R_{so} = (a_s + b_s) R_a \\tag{18}$$',
        content
    )

    # Equation 19
    content = re.sub(
        r'Rso = \(0,75 \+ 2E10-5z\) Ra \(\*\*Persamaan 19\*\*\)',
        r'$$R_{so} = (0.75 + 2 \\times 10^{-5}z) R_a \\tag{19}$$',
        content
    )

    # Equation 20
    content = re.sub(
        r'Rns = \(1-a\) Rs \(\*\*Persamaan 20\*\*\)',
        r'$$R_{ns} = (1-\\alpha) R_s \\tag{20}$$',
        content
    )

    # Equation 21 (complex)
    content = re.sub(
        r'Rnl = σ\[\(\(Tmax \+ 273\.16\)\^4 \+ \(Tmin \+ 273\.16\)\^4\) / 2\] \\\* \(0\.34 - 0\.14√ea\) \\\* \[1\.35 \\\* Rs/Rso - 0\.35\] \(\*\*Persamaan 21\*\*\)',
        r'$$R_{nl} = \\sigma\\left[\\frac{(T_{max} + 273.16)^4 + (T_{min} + 273.16)^4}{2}\\right] (0.34 - 0.14\\sqrt{e_a}) \\left[1.35 \\frac{R_s}{R_{so}} - 0.35\\right] \\tag{21}$$',
        content
    )

    # Equation 22
    content = re.sub(
        r'Rn = Rns - Rnl \(\*\*Persamaan 22\*\*\)',
        r'$$R_n = R_{ns} - R_{nl} \\tag{22}$$',
        content
    )

    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Successfully converted equations in 20040103-menghitung-radiasi-matahari.qmd')
        return True
    else:
        print(f'No changes made to 20040103-menghitung-radiasi-matahari.qmd')
        return False

if __name__ == '__main__':
    convert_radiation_file()
