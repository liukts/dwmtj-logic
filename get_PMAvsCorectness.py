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

yval = [0, 0, 0, 0, 0, 0, 1, 2, 47, 60, 86]
yval = np.array(yval)

fig,ax = plt.subplots(1,1,figsize=(8,8))
xticks = np.linspace(450, 500, 11, endpoint=True)

for i in range(len(yval)):
    yval[i] = ((200 - yval[i]) / 200) * 100
supper = np.ma.masked_where(yval != 100.0, yval)

#Plot the figure
plt.plot(xticks,yval,linewidth=LW, color='black')
plt.plot(xticks,supper,linewidth=LW, color='orange')
plt.grid(which="both",color="#E2E2E2")
plt.tick_params(labelsize=FS)
ax.set_xlim([450,500])
ax.set_ylim([48,102])
ax.set_xlabel('Minimum PMA (kJ/$m^3$)',fontsize=FS,fontname="Arial")
ax.set_ylabel('Correctness (%)',fontsize=FS,fontname="Arial")
ax.set_xticks([450,455,460,465,470,475,480,485,490,495,500])
ax.set_xticklabels(["450", "", "460", "", "470", "", "480", "", "490", "", "500"],fontname="Arial")
ax.set_yticks([50,55,60,65,70,75,80,85,90,95,100])
ax.set_yticklabels(["50","","60","","70","","80","","90","","100"],fontname="Arial")

plt.savefig("PMA_Correctness.svg",bbox_inches="tight")
plt.show()