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
num_seeds = 3

for i in range(num_seeds):
    cur_data = np.loadtxt("./TestVCMA/DWconcat_"+str(seedlist[i])+".out/table.txt")
    if i == 0:
        t = cur_data[:,0]
        dw_pos = np.zeros((num_seeds,len(t)))
    dw_pos[i,:] = cur_data[:,3] * (sizeX + fixed_w * 2) / 2 + sizeX / 2 # translate mz vector to dw_pos

fig,ax = plt.subplots(1,1,figsize=(8,8))

strings = ["5e5", "4.85e5", "4.7e5"]
for i in range(num_seeds):
    plt.plot(t/1e-9,dw_pos[i,:],linewidth=LW, label=strings[i])

plt.show()

# Plot t vs DW Position
# This is the verticle lines help signifying pulses
plt.plot([(t_rest)/1e-9,(t_rest)/1e-9],[0,sizeX],'--k',linewidth=LW)
plt.plot(np.array([(t_rest)/1e-9,(t_rest)/1e-9])+t_pulse/1e-9,[0,sizeX],'--k',linewidth=LW)


#MTJ Dimesions
x_L = sizeX/2 - MTJ_w/2 # MTJ left
x_R = sizeX/2 + MTJ_w/2 # MTJ right
plt.plot([0,sizeX],[x_L,x_L],':r',linewidth=LW)
plt.plot([0,sizeX],[x_R,x_R],':r',linewidth=LW)

#Plot VCMA
plt.plot([0,sizeX],[sizeX/2 - (offsetDistance + oxideWidth),sizeX/2 - (offsetDistance + oxideWidth)],':g',linewidth=LW)
plt.plot([0,sizeX],[sizeX/2 - offsetDistance,sizeX/2 - offsetDistance],':g',linewidth=LW)

plt.plot([0,sizeX],[sizeX/2 + offsetDistance,sizeX/2 + offsetDistance],':g',linewidth=LW)
plt.plot([0,sizeX],[sizeX/2 + offsetDistance + oxideWidth,sizeX/2 + offsetDistance + oxideWidth],':g',linewidth=LW)

plt.grid(which="both",color="#E2E2E2")
plt.tick_params(labelsize=FS)
ax.set_xlim([1,7])
ax.set_ylim([0,sizeX])
ax.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax.set_ylabel('DW Position (nm)',fontsize=FS,fontname="Arial")
ax.set_xticks([1,2,3,4,5,6,7])
ax.set_xticklabels(["0","","2","","4","","6"],fontname="Arial")
ax.legend(loc='lower right', prop={'size': FS})
ax.set_yticks([0,sizeX/2 - offsetDistance - oxideWidth,sizeX/2 - offsetDistance,x_L,x_R,sizeX/2 + offsetDistance,sizeX/2 + offsetDistance + oxideWidth])
ax.set_yticklabels(ax.get_yticks().astype(int),fontname="Arial")

plt.savefig("figure2.svg",bbox_inches="tight")
plt.show()