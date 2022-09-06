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

t_pulse = 5e-9
t_rest1 = 1e-9
t_rest2 = 2e-9

# seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
    # 317769570,370982442,438702097,480729151,539132639,594026345,675324135,686123422,701027736,\
    # 701258021,709705655,944973596,962102195],dtype=int)
seedlist = np.array([480729151,539132639,594026345],dtype=int)
nseeds = len(seedlist)

J_resets = np.load("J_reset_3.0e10_TMR=200.npy")

for i in range(nseeds):
    cur_data = np.loadtxt("./results_concat_3.0e10_TMR=200/DWconcat_"+str(seedlist[i])+"_2.out/table.txt")
    if i == 0:
        t = cur_data[:,0]
        dw_pos = np.zeros((nseeds,len(t)))
    dw_pos[i,:] = (cur_data[:,3] + 1) * 160 - 5 # translate mz vector to dw_pos

fig,(ax1,ax2) = plt.subplots(2,1,figsize=(7,11.5))
plt.subplots_adjust(hspace=0.25)

# Pulse start and end
ax2.plot([t_rest1/1e-9,t_rest1/1e-9],[0,320],'--k',linewidth=LW)
ax2.plot(np.array([t_rest1/1e-9,t_rest1/1e-9])+t_pulse/1e-9,[0,320],'--k',linewidth=LW)

for i in range(nseeds):
    ax2.plot(t/1e-9,dw_pos[i,:],linewidth=LW)

ax2.grid(which="both",color="#E2E2E2")
ax2.set_axisbelow(True)
ax2.tick_params(labelsize=FS)
ax2.set_xlim([0,8])
ax2.set_ylim([0,320])
ax2.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax2.set_ylabel('DW position (nm)',fontsize=FS,fontname="Arial")
ax2.set_xticks([0,1,2,3,4,5,6,7,8])
ax2.set_xticklabels(["0","1","2","3","4","5","6","7","8"],fontname="Arial")
ax2.set_yticks([0,40,80,120,160,200,240,280,320])
ax2.set_yticklabels(ax2.get_yticks().astype(int),fontname="Arial")

t_sample = np.arange(0,8e-9,0.05e-9)

for i in range(nseeds):
    ax1.plot(t_sample/1e-9,J_resets[i,:],linewidth=LW)

ax1.grid(which="both",color="#E2E2E2")
ax1.set_axisbelow(True)
ax1.tick_params(labelsize=FS)
ax1.set_xlim([0,8])
ax1.set_ylim([0,4.5])
ax1.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
ax1.set_ylabel(r'J$_2$ (A/m$^2$)',fontsize=FS,fontname="Arial")
ax1.set_xticks([0,1,2,3,4,5,6,7,8])
ax1.set_xticklabels(["0","1","2","3","4","5","6","7","8"],fontname="Arial")
ax1.set_yticks([0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4,4.5])
ax1.set_yticklabels(["0","","1","","2","","3","","4",""],fontname="Arial")
plt.savefig("var_waveform_reset.svg",bbox_inches="tight")


plt.savefig("var_waveform_dw2.svg",bbox_inches="tight")
plt.show()