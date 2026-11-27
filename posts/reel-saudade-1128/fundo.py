"""Monta o fundo (clipes cortados em 9:16, aproximação lenta, cor e granulação) com fusões curtas."""
import subprocess, sys
C = '/home/claude/verdades/kit/clipes/'
X = 0.35
# (arquivo, início no clipe, centro horizontal do corte 0..1, brilho)
CENAS = [('m35979.mp4', 9.0, 0.63, 0.00),   # Saudade é o jeito que o amor encontrou de ficar
         ('m36091.mp4', 6.0, 0.62, 0.03),    # Dói lembrar da casa cheia
         ('m9121.mp4', 4.0, 0.36, -0.03),    # da voz chamando pro almoço
         ('m35982.mp4', 4.0, 0.64, -0.01),   # do abraço que não volta mais
         ('m23095.mp4', 1.0, 0.38, -0.01),   # Mas só dói assim o que foi bom de verdade
         ('m21674.mp4', 6.5, 0.32, -0.03),   # Então não foge da lembrança. Sorri pra ela.
         ('m36631.mp4', 2.5, 0.66, -0.01),   # Agradece por ter vivido tudo isso
         ('m5383.mp4', 2.5, 0.44, -0.02)]    # E abraça hoje quem ainda está aqui
T = [0, 4.2, 6.1, 7.9, 10.1, 12.8, 16.2, 18.7, 24.5]

ins, fil = [], []
for i, (f, ss, px, br) in enumerate(CENAS):
    d = T[i + 1] - T[i] + (X if i < len(CENAS) - 1 else 0)
    ins += ['-ss', str(ss), '-t', f'{d:.3f}', '-i', C + f]
    fil.append(
        f"[{i}:v]fps=30,crop='min(iw,ih*9/16)':'min(ih,iw*16/9)':'max(0,min(iw-ow,iw*{px}-ow/2))':'(ih-oh)/2',scale=1188:2112:flags=lanczos,setsar=1,"
        f"scale=w='trunc(1188*(1+0.05*t/{d:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:1920,"
        f"eq=saturation=0.86:contrast=1.04:brightness={br},colorbalance=rs=0.03:bs=-0.02:rh=0.02,"
        f"format=yuv420p,setpts=PTS-STARTPTS[v{i}]")
prev = 'v0'
for i in range(1, len(CENAS)):
    fil.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={T[i]:.3f}[x{i}]")
    prev = f'x{i}'
fil.append(f"[{prev}]vignette=PI/4.2,noise=alls=7:allf=t,format=yuv420p[out]")
cmd = ['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fil), '-map', '[out]',
       '-t', str(T[-1]), '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '/home/claude/w/fundo.tmp.mp4']
subprocess.run(cmd, check=True)
