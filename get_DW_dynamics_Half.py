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

# seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
#     317769570,370982442,438702097,480729151,539132639,594026345,675324135,686123422,701027736,\
#     701258021,709705655,944973596,962102195],dtype=int)
# seedlist = np.array([480729151,539132639,594026345],dtype=int)
# nseeds = len(seedlist)

seedlist = np.array([1,2,3],dtype=int) #1 being 5 2 being 4.9 and 3 being 4.7
num_seeds = 1

J_resets1 = np.load("./TestHalf/J_reset_D1_Test1.npy")
J_resets2 = np.load("./TestHalf/J_reset_D1_Test2.npy")
J_resets = J_resets1 + J_resets2



fig,ax = plt.subplots(1,1,figsize=(8,8))

strings = ["5e5", "4.85e5", "4.7e5"]
t_sample = np.arange(0,t_pulse + t_rest,0.05e-9)

for i in range(num_seeds):
    plt.plot(t_sample/1e-9,J_resets[i,:],linewidth=LW, color='black')
    plt.plot(t_sample/1e-9,J_resets1[i,:],linewidth=LW)
    plt.plot(t_sample/1e-9,J_resets2[i,:],linewidth=LW)


plt.grid(which="both",color="#E2E2E2")
plt.tick_params(labelsize=FS)
ax.set_xlim([0,4])
ax.set_ylim([0,7])
ax.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax.set_ylabel(r'J$_2$ (A/m$^2$)',fontsize=FS,fontname="Arial")
ax.set_xticks([0,1,2,3,4])
ax.set_xticklabels(["1","2","3","4","5"],fontname="Arial")
# ax.legend(loc='lower right', prop={'size': FS})
ax.set_yticks([0,1,2,3,4,5,6,7])
ax.set_yticklabels(["","1","","3","","5","","7"],fontname="Arial")

plt.savefig("figure5H.svg",bbox_inches="tight")
plt.show()