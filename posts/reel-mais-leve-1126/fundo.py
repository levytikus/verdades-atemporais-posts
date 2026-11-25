"""Monta o fundo (clipes cortados em 9:16, aproximação lenta, cor e granulação) com fusões curtas."""
import subprocess, sys
C = '/home/claude/verdades/kit/clipes/'
X = 0.35
# (arquivo, início no clipe, centro horizontal do corte 0..1, brilho)
CENAS = [('m36913.mp4', 5.0, 0.42, 0.0),    # Tem gente que deixa a vida mais leve
         ('m8900.mp4', 0.5, 0.50, -0.01),    # só de estar perto
         ('m4872.mp4', 6.0, 0.37, -0.01),    # uma terça qualquer numa história pra contar
         ('m42583.mp4', 2.3, 0.68, -0.02),   # ri das mesmas bobagens até a barriga doer
         ('m4709.mp4', 2.5, 0.57, -0.01),    # comemora as suas vitórias
         ('m23582.mp4', 0.2, 0.45, 0.0),     # você já ganhou na vida
         ('m8741.mp4', 7.0, 0.40, -0.01)]    # manda isso pra essa pessoa agora
T = [0, 3.3, 4.65, 8.3, 12.1, 15.5, 19.3, 25.25]

ins, fil = [], []
for i, (f, ss, px, br) in enumerate(CENAS):
    d = T[i + 1] - T[i] + (X if i < len(CENAS) - 1 else 0)
    ins += ['-ss', str(ss), '-t', f'{d:.3f}', '-i', C + f]
    fil.append(
        f"[{i}:v]fps=30,{'tpad=stop_mode=clone:stop_duration=2,' if i == len(CENAS) - 1 else ''}crop='min(iw,ih*9/16)':'min(ih,iw*16/9)':'max(0,min(iw-ow,iw*{px}-ow/2))':'(ih-oh)/2',scale=1188:2112:flags=lanczos,setsar=1,"
        f"scale=w='trunc(1188*(1+0.05*t/{d:.3f})/2)*2':h=-2:eval=frame:flags=bicubic,crop=1080:1920,"
        f"eq=saturation=0.97:contrast=1.03:brightness={br},colorbalance=rs=0.03:bs=-0.02:rh=0.02,"
        f"format=yuv420p,setpts=PTS-STARTPTS[v{i}]")
prev = 'v0'
for i in range(1, len(CENAS)):
    fil.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={T[i]:.3f}[x{i}]")
    prev = f'x{i}'
fil.append(f"[{prev}]vignette=PI/4.2,noise=alls=7:allf=t,format=yuv420p[out]")
cmd = ['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fil), '-map', '[out]',
       '-t', str(T[-1]), '-c:v', 'libx264', '-crf', '14', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '/home/claude/w/fundo.tmp.mp4']
subprocess.run(cmd, check=True)
