"""Gera os quadros da logo do Verdades (círculo amarelo + carinha oficial) piscando.

Uso: python piscada.py PASTA_SAIDA [TAMANHO]
Saída: w_KK_B.png  (KK = 00..20, quanto o olho direito está fechado; B = 0..6, pulinho de 0% a 6%)
O olho fechado fica centralizado na mesma altura e no mesmo eixo do olho aberto.
Requer rsvg-convert.
"""
import subprocess, sys, os, tempfile

AMARELO, PRETO = '#FFCD11', '#111111'
# olhos do SVG oficial (marca/va-perfil.svg): linhas x=530 e x=718, y 465..585, traço 110, ponta redonda
EYE_TOP, EYE_BOT, EYE_W = 465, 585, 110
EYE_CY = (EYE_TOP + EYE_BOT) / 2

def olho(x, k):
    # aberto: pílula vertical 110 x 230 centrada em (x, EYE_CY). fechado: pílula horizontal achatada, mesmo centro
    h_aberto = (EYE_BOT - EYE_TOP) + EYE_W
    h = h_aberto - (h_aberto - 46) * k          # altura vai de 230 a 46
    w = EYE_W + 40 * k                          # alarga um pouco ao fechar (110 a 150)
    r = min(w, h) / 2
    return f"<rect x='{x - w/2:.1f}' y='{EYE_CY - h/2:.1f}' width='{w:.1f}' height='{h:.1f}' rx='{r:.1f}' fill='{PRETO}'/>"

def svg(k, b, size):
    boca = (f"<polyline points='341,745 341,855 898,855 898,745' fill='none' stroke='{PRETO}' stroke-width='104' stroke-linecap='round' stroke-linejoin='round'/>"
            f"<path d='M390,776 L390,806 L418,806 L418,803 A25 25 0 0 1 393,778 L393,776 Z M849,776 L849,806 L821,806 L821,803 A25 25 0 0 0 846,778 L846,776 Z' fill='{PRETO}'/>")
    face = olho(530, 0) + olho(718, k) + boca
    s = 0.93 * b
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='73 74 1092 1092' width='{size}' height='{size}'>"
            f"<g transform='translate(619 620) scale({s:.4f}) translate(-619 -620)'><circle cx='619' cy='620' r='546' fill='{AMARELO}'/>"
            f"<g transform='translate(619 620) scale(0.86) translate(-619 -660)'>{face}</g></g></svg>")

if __name__ == '__main__':
    out = sys.argv[1]; size = int(sys.argv[2]) if len(sys.argv) > 2 else 280
    os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        for i in range(21):
            for j in range(7):
                p = os.path.join(td, 't.svg')
                open(p, 'w').write(svg(i / 20, 1 + 0.01 * j, size))
                subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), p, '-o', os.path.join(out, f'w_{i:02d}_{j}.png')], check=True)
