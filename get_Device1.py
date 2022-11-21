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
sizeX = 255 # Size of DW (nm)
fixed_w = 5 # Size of fixed ends (nm)
MTJ_w = 45 # Size of the MTJ (nm)
oxideWidth = 15 # Size of Contact (nm)
startpos = 0 #Start position (nm)
offsetDistance = (9 * 15e-9)/2 + 15e-9
offsetDistance = offsetDistance / 1e-9

seedlist = np.array([1,2,3,4,5,6,\
        7,8,9,10, 11, 12, 13, 14, \
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
        25, 26, 27, 28, 29, 30, 31, 32, 33, \
        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, \
        44, 45, 46, 47, 48, 49, 50],dtype=int)
num_seeds = 25
pulse_amp_indices = np.array([29])

# Load and process DW position data
for i in range(num_seeds):
    seed_i = str(seedlist[i])
    for j in range(len(pulse_amp_indices)):

        current_dir = "./Test"+str(Test)+"/DWswitch_"+seed_i+"_1.out"
        cur_data = np.loadtxt(current_dir + '/table.txt')

        if j == 0 and i == 0:
            t = cur_data[:,0]

        x = cur_data[:,3] * (sizeX + fixed_w * 2) / 2 + sizeX / 2
        if j == 0 and i == 0:
            dw_pos = np.zeros((num_seeds,len(t)))
        dw_pos[i,:] = x

fig,ax1 = plt.subplots(1,1,figsize=(8,8))
x_L = sizeX/2 - MTJ_w/2 # MTJ left
x_R = sizeX/2 + MTJ_w/2 # MTJ right
Dx = x_R - x_L

# Plot t vs DW position
# This is the veritcle lines
ax1.plot([t_rest/1e-9,t_rest/1e-9],[0,sizeX],'--k',linewidth=LW)
ax1.plot(np.array([t_rest/1e-9,t_rest/1e-9])+t_pulse/1e-9,[0,sizeX],'--k',linewidth=LW)
ax1.plot(np.array([t_rest/1e-9,t_rest/1e-9])+(t_pulse+t_rest)/1e-9,[0,sizeX],'--k',linewidth=LW)
ax1.plot(np.array([t_rest/1e-9,t_rest/1e-9])+(2*t_pulse+t_rest)/1e-9,[0,sizeX],'--k',linewidth=LW)

#Plot MTJ dimensions
ax1.plot([0,sizeX],[x_L,x_L],':r',linewidth=LW)
ax1.plot([0,sizeX],[x_R,x_R],':r',linewidth=LW)

#Plot VCMA (15 nm for oxide)
ax1.plot([0,sizeX],[sizeX/2 - (offsetDistance + oxideWidth),sizeX/2 - (offsetDistance + oxideWidth)],':g',linewidth=LW)
ax1.plot([0,sizeX],[sizeX/2 - offsetDistance,sizeX/2 - offsetDistance],':g',linewidth=LW)

ax1.plot([0,sizeX],[sizeX/2 + offsetDistance,sizeX/2 + offsetDistance],':g',linewidth=LW)
ax1.plot([0,sizeX],[sizeX/2 + offsetDistance + oxideWidth,sizeX/2 + offsetDistance + oxideWidth],':g',linewidth=LW)

for i in range(num_seeds):
    plt.plot(t/1e-9,dw_pos[i,:],linewidth=LW)

ax1.grid(which="both",color="#E2E2E2")
ax1.set_axisbelow(True)
ax1.tick_params(labelsize=FS)
ax1.set_xlim([0,max(t/1e-9)])
ax1.set_xlim([1,7])
ax1.set_ylim([0,sizeX])
ax1.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax1.set_ylabel('DW position (nm)',fontsize=FS,fontname="Arial")
ax1.set_xticks([1,2,3,4,5,6,7])
ax1.set_xticklabels(["0","","2","","4","","6"],fontname="Arial")
ax1.set_yticks([0,sizeX/2 - offsetDistance - oxideWidth,sizeX/2 - offsetDistance,x_L,x_R,sizeX/2 + offsetDistance,sizeX/2 + offsetDistance + oxideWidth])
ax1.set_yticklabels(ax1.get_yticks().astype(int),fontname="Arial")

plt.savefig("device1.svg",bbox_inches="tight")

plt.show()