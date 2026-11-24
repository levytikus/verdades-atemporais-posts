"""Monta o fundo (clipes cortados em 9:16, aproximação lenta, cor e granulação) com fusões curtas."""
import subprocess, sys
C = '/home/claude/verdades/kit/clipes/'
X = 0.35
# (arquivo, início no clipe, centro horizontal do corte 0..1, brilho)
CENAS = [('m46702.mp4', 7.0, 0.52, -0.02),   # Repara no jeito que você fala com você
         ('m46558.mp4', 3.0, 0.50, -0.06),   # se chama de burro, de fraco, de incapaz
         ('m52240.mp4', 7.0, 0.45, -0.04),   # quem você ama
         ('m4511.mp4', 1.0, 0.30, -0.09),    # então por que fala assim com você?
         ('m41225.mp4', 0.5, 0.27, -0.05),   # seu melhor amigo
         ('m18272.mp4', 2.0, 0.44, -0.03),   # com paciência, com carinho
         ('m32131.mp4', 2.0, 0.60, -0.07)]   # você também merece a sua gentileza
T = [0, 3.15, 7.95, 10.8, 14.3, 18.3, 21.15, 26.9]

ins, fil = [], []
for i, (f, ss, px, br) in enumerate(CENAS):
    d = T[i + 1] - T[i] + (X if i < len(CENAS) - 1 else 0)
    ins += ['-ss', str(ss), '-t', f'{d:.3f}', '-i', C + f]
    fil.append(
        f"[{i}:v]fps=30,crop='min(iw,ih*9/16)':'min(ih,iw*16/9)':'max(0,min(iw-ow,iw*{px}-ow/2))':'(ih-oh)/2',scale=1188:2112:flags=lanczos,setsar=1,"
        f"scale=w='trunc(1188*(1+0.05*t/{d:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:1920,"
        f"eq=saturation=0.82:contrast=1.04:brightness={br},colorbalance=rs=0.03:bs=-0.02:rh=0.02,"
        f"format=yuv420p,setpts=PTS-STARTPTS[v{i}]")
prev = 'v0'
for i in range(1, len(CENAS)):
    fil.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={T[i]:.3f}[x{i}]")
    prev = f'x{i}'
fil.append(f"[{prev}]vignette=PI/4.2,noise=alls=7:allf=t,format=yuv420p[out]")
cmd = ['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fil), '-map', '[out]',
       '-t', str(T[-1]), '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '/home/claude/w/fundo.tmp.mp4']
subprocess.run(cmd, check=True)
