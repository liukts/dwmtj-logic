import os
from os import path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
FS = 24
LW = 3.5
font = font_manager.FontProperties(family='Arial',style='normal',size=FS)
matplotlib.rcParams['axes.linewidth'] = 4

Test = 0

# CHECKME Fixme
t_pulse = 3e-9 # length of current pulse
t_rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
sizeX = 135 # Size of DW (nm)
fixed_w = 5 # Size of fixed ends (nm)
MTJ_w = 15 # Size of the MTJ (nm)
offsetDistance = 22.5 #Distance from middle of DW to edge of contact (nm)
oxideWidth = 15 # Size of Contact (nm)
# t_rest2 = 2e-9

# seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
#     317769570,370982442,438702097,480729151,539132639,594026345,675324135,686123422,701027736,\
#     701258021,709705655,944973596,962102195],dtype=int)
# seedlist = np.array([480729151,539132639,594026345],dtype=int)
# nseeds = len(seedlist)

seedlist = np.array([52,53,54,55,56,\
        57,58,59,60, 61, 62, 63, 64, \
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74, \
        75, 76, 77, 78, 79, 80,81, 82, 83, \
        84, 85, 86, 87, 88, 89, 90, 91, 92, 93, \
        94, 95, 96, 97, 98, 99, 100],dtype=int)
num_seeds = 3

J_LAA = np.load("./Output_Current/J_LAA.npy")
J_LAP = np.load("./Output_Current/J_LAP.npy")
J_LPA = np.load("./Output_Current/J_LPA.npy")
J_LPP = np.load("./Output_Current/J_LPP.npy")
J_RAA = np.load("./Output_Current/J_RAA.npy")
J_RAP = np.load("./Output_Current/J_RAP.npy")
J_RPA = np.load("./Output_Current/J_RPA.npy")
J_RPP = np.load("./Output_Current/J_RPP.npy")

J_resets = J_LAA

for i in range(num_seeds):
    cur_data = np.loadtxt("./Test"+str(Test)+"/DWconcat_"+str(seedlist[i])+"_2.out/table.txt")
    if i == 0:
        t = cur_data[:,0]
        dw_pos = np.zeros((num_seeds,len(t)))
    dw_pos[i,:] = cur_data[:,3] * (sizeX + fixed_w * 2) / 2 + sizeX / 2 # translate mz vector to dw_pos
    # dw_pos[i,:] = (cur_data[:,3] + 1) * sizeX/2 - fixed_w # translate mz vector to dw_pos

fig,(ax1,ax2) = plt.subplots(2,1,figsize=(7,11.5))
plt.subplots_adjust(hspace=0.25)

# Pulse start and end
ax2.plot([1,1],[0,sizeX],'--k',linewidth=LW)
ax2.plot(np.array([1,1])+t_pulse/1e-9,[0,sizeX],'--k',linewidth=LW)

#MTJ Dimesions
x_L = sizeX/2 - MTJ_w/2 # MTJ left
x_R = sizeX/2 + MTJ_w/2 # MTJ right
ax2.plot([0,sizeX],[x_L,x_L],':r',linewidth=LW)
ax2.plot([0,sizeX],[x_R,x_R],':r',linewidth=LW)

#Plot VCMA
ax2.plot([0,sizeX],[sizeX/2 - (offsetDistance + oxideWidth),sizeX/2 - (offsetDistance + oxideWidth)],':g',linewidth=2)
ax2.plot([0,sizeX],[sizeX/2 - offsetDistance,sizeX/2 - offsetDistance],':g',linewidth=2)

ax2.plot([0,sizeX],[sizeX/2 + offsetDistance,sizeX/2 + offsetDistance],':g',linewidth=2)
ax2.plot([0,sizeX],[sizeX/2 + offsetDistance + oxideWidth,sizeX/2 + offsetDistance + oxideWidth],':g',linewidth=2)

for i in range(num_seeds):
    ax2.plot(t/1e-9,dw_pos[i,:],linewidth=LW)

ax2.grid(which="both",color="#E2E2E2")
ax2.set_axisbelow(True)
ax2.tick_params(labelsize=FS)
# ax2.set_xlim([0,8])
ax2.set_xlim([0,max(t/1e-9)])
ax2.set_ylim([0,sizeX])
ax2.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax2.set_ylabel('DW position (nm)',fontsize=FS,fontname="Arial")
# ax2.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12])
# ax2.set_xticklabels(["0","","2","","4","","6","","8","","10","","12"],fontname="Arial")
# ax2.set_yticks([0,65,130,195,260])
ax2.set_yticks([0,sizeX/2 - offsetDistance - oxideWidth,sizeX/2 - offsetDistance,x_L,x_R,sizeX/2 + offsetDistance,sizeX/2 + offsetDistance + oxideWidth,135])
ax2.set_yticklabels(ax2.get_yticks().astype(int),fontname="Arial")

t_sample = np.arange(0,t_pulse + t_rest,0.05e-9)

# ax1.plot([t_rest1/1e-9,t_rest1/1e-9],[0,260],'--k',linewidth=LW)
# ax1.plot(np.array([t_rest1/1e-9,t_rest1/1e-9])+t_pulse/1e-9,[0,260],'--k',linewidth=LW)
for i in range(num_seeds):
    ax1.plot(t_sample/1e-9,J_resets[i,:],linewidth=LW)

ax1.grid(which="both",color="#E2E2E2")
ax1.set_axisbelow(True)
ax1.tick_params(labelsize=FS)
ax1.set_xlim([0,t_pulse/1e-9 + 2])
# ax1.set_xlim([0,max(t/1e-9)])
ax1.set_ylim([0,4.5])
ax1.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax1.set_ylabel(r'J$_2$ (A/m$^2$)',fontsize=FS,fontname="Arial")
# ax1.set_xticks([0,1,2,3,4,5,6,7,8])
# ax1.set_xticklabels(["2","3","4","5","6","7","8","9","10"],fontname="Arial")
ax1.set_yticks([0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4,4.5])
ax1.set_yticklabels(["0","","1","","2","","3","","4",""],fontname="Arial")
# plt.savefig("var_waveform_reset.svg",bbox_inches="tight")


plt.savefig("var_waveform_dw2.svg",bbox_inches="tight")
plt.show()

newfolder = "Test" + str(Test) + "/"
os.system("mv var_waveform_dw2.svg " + newfolder)