import os
import math
from os import path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
FS = 30
LW = 4.5
font = font_manager.FontProperties(family='Arial',style='normal',size=FS)
matplotlib.rcParams['axes.linewidth'] = 4

Test = 100

#CHECKME Parameters that need to change
t_pulse = 2e-9 # length of current pulse
t_rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
J_resets = np.load("./Test"+str(Test)+"/J_reset_D1_Test1.npy")
t_sample = np.arange(0,t_pulse + t_rest,0.05e-9)
seedlist = np.array([1,2,3,4,5,6,\
        7,8,9,10, 11, 12, 13, 14, \
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
        25, 26, 27, 28, 29, 30, 31, 32, 33, \
        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, \
        44, 45, 46, 47, 48, 49, 50],dtype=int)
num_seeds = 25
pulse_amp_indices = np.array([29])

fig,ax1 = plt.subplots(1,1,figsize=(8,8))
for i in range(num_seeds):
    ax1.plot(t_sample/1e-9,J_resets[i,:],linewidth=LW)

ax1.grid(which="both",color="#E2E2E2")
ax1.set_axisbelow(True)
ax1.tick_params(labelsize=FS)
ax1.set_xlim([0,t_pulse/1e-9 + 2])
ax1.set_ylim([0,10])
ax1.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax1.set_ylabel(r'J$_2$ (A/m$^2$)',fontsize=FS,fontname="Arial")
ax1.set_xticks([0,1,2,3,4])
ax1.set_xticklabels(["1","2","3","4","5"],fontname="Arial")
ax1.set_yticks([0,1.0,2.0,3.0,4.0,5,6,7,8,9,10])
ax1.set_yticklabels(["0","","2","","4","","6","","8","","10"],fontname="Arial")

plt.savefig("currentpulse.svg",bbox_inches="tight")

plt.show()