import os
from os import path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

FS = 30
LW = 4.5
font = font_manager.FontProperties(family='Arial',style='normal',size=FS)
matplotlib.rcParams['axes.linewidth'] = 4

# CHECKME Fixme
t_pulse = 2e-9 # length of current pulse
t_rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
sizeX = 255 # Size of DW (nm)
fixed_w = 5 # Size of fixed ends (nm)
MTJ_w = 45 # Size of the MTJ (nm)
offsetDistance = (9 * 15e-9)/2 + 15e-9 #Distance from middle of DW to edge of contact (nm)
offsetDistance = offsetDistance / 1e-9
oxideWidth = 15 # Size of Contact (nm)

yval = [100, 100, 100, 99, 84, 63, 41, 23, 16, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 4, 4, 4, 4, 14, 16, 19, 20]
yval = np.array(yval)
# eval = [1.158511,1.142367,1.127156,1.112798,1.099226,1.086374,1.074186,1.062613,1.051609,1.041133,1.031147,1.021618,1.012516,1.003812,0.99548,0.987498,0.979842,0.972496,0.965436,0.958377,0.951317,0.944257,0.937198,0.930138,0.923078,0.916019,0.908959,0.9019,0.89484,0.88778,0.880721,0.873661,0.8666,0.859542,0.852482, 0.845423,0.838363,0.831303,0.824244,0.817184,0.810124,0.803064,0.796005,0.788945,0.781886]
eval = [1.158511,1.142367,1.127156,1.112798,1.099226,1.086374,1.074186,1.062613,1.051609,1.041133,1.031147,1.021618,1.012516,1.003812,0.99548,0.987498,0.979842,0.972496,0.965436,0.958377,0.951317,0.944257,0.937198,0.930138,0.923078,0.916019,0.908959,0.9019,0.89484,0.88778,0.880721,0.873661,0.8666,0.859542,0.852482, 0.845423,0.838363,0.831303,0.824244,0.817184,0.810124,0.739528,0.668932,0.598335,0.527739]

#0 (1.1585, 1.1585, 1.1585, 1.1585) - 1.1585
#5 (1.1585, 1.1423978, 1.1423978, 1.12616339) - 1.14236
#10 (1.1585, 1.12727, 1.12727, 1.09557344) - 1.12715
#10 (1.1585, 1.11304, 1.11304, 1.0666) - 1.112795
#...
#60 (1.1585, 1.01500165, 1.01500165, 0.8615506) - 1.0125125
#65 (1.1585, 1.0066026, 1.0066026, 0.8435321456)
#70 (1.1585, 0.9985796, 0.9985796, 0.82625189)
#75 (1.1585, 0.9909079, 0.9909079, 0.8096654)
#80

#75 (2.2234, 2.004, 2.004, 1.736)
fig,ax = plt.subplots(1,1,figsize=(8,8))
xticks = np.linspace(0, 200, 41, endpoint=True)
xticks = np.append(xticks, 250)
xticks = np.append(xticks, 300)
xticks = np.append(xticks, 350)
xticks = np.append(xticks, 400)

for i in range(len(yval)):
    yval[i] = ((200 - yval[i]) / 200) * 100
supper = np.ma.masked_where(yval != 100.0, eval)

#Plot the figure
plt.plot(xticks,eval,linewidth=LW, color='black')
plt.plot(xticks,supper,linewidth=LW, color='orange')
plt.grid(which="both",color="#E2E2E2")
plt.tick_params(labelsize=FS)
ax.set_xlim([0,400])
ax.set_ylim([0.5,1.25])
ax.set_xlabel('TMR (%)',fontsize=FS,fontname="Arial")
ax.set_ylabel('Average Energy (fJ)',fontsize=FS,fontname="Arial")
ax.set_xticks([0,50,100,150,200,250,300,350,400])
ax.set_xticklabels(["0","","100","","200","","300","","400"],fontname="Arial")
# ax.set_yticks([50,55,60,65,70,75,80,85,90,95,100])
# ax.set_yticklabels(["50","","60","","70","","80","","90","","100"],fontname="Arial")

plt.savefig("TMR_Energy.svg",bbox_inches="tight")
plt.show()