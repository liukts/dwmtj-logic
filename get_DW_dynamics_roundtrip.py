import os
from os import path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
FS = 30
LW = 3.5
font = font_manager.FontProperties(family='Arial',style='normal',size=FS)
matplotlib.rcParams['axes.linewidth'] = 4

# This file processes the simulation results for a DW device driven first by a positive pulse,
# then a negative pulse, to move it back and forth across the magnetic track

t_pulse = 5e-9 # length of current pulse
t_rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)

# What to plot
# mode 1: Jx vs total DW displacement, with 20 random seeds per Jx
# mode 2: t vs DW position for various seeds, fixed Jx (set below)
# mode 3: t vs DW position for negative pulse, various seeds. Save currents to file to use in concat simulation
mode = 3

seedlist = np.array([480729151,539132639,594026345],dtype=int)
nseeds = len(seedlist)

# Indices for pulse amplitude
if mode == 1:
    # All pulse amplitudes are used
    # pulse_amp_indices = np.arange(0,30,1)
    pulse_amp_indices = [0]
    pulse_amps = np.zeros(len(pulse_amp_indices))
    dx_array = np.zeros((len(pulse_amp_indices),nseeds))
    dx_array_neg = np.zeros((len(pulse_amp_indices),nseeds))

elif mode == 2 or mode == 3:
    # Change line below to set pulse amplitude index (the actual Jx is inside for loop below)
    pulse_amp_indices = np.array([29])
    pulse_amps = np.zeros(len(pulse_amp_indices))    

# Load and process DW position data
for i in range(nseeds):
    seed_i = str(seedlist[i])
    for j in range(len(pulse_amp_indices)):

        # obtain current working directory of data
        # jx = 1.0e+10 + pulse_amp_indices[j]*0.1e+10
        jx = 3.0e+10
        pulse_amps[j] = jx

        jx_str = "{:.1e}".format(jx)
        current_dir = "./results_roundtrip/DWswitch_"+jx_str+"_"+seed_i+"_L150_roundtrip.out"
        cur_data = np.loadtxt(current_dir + '/table.txt')

        if j == 0 and i == 0:
            t = cur_data[:,0]

        x = (cur_data[:,3] + 1) * 160 - 5 # translate mz vector to dw_pos
        if mode == 2 or mode == 3:
            if j == 0 and i == 0:
                dw_pos = np.zeros((nseeds,len(t)))
            dw_pos[i,:] = (cur_data[:,3] + 1) * 160 - 5 # translate mz vector to dw_pos
        elif mode == 1:
            t1 = t_rest + t_pulse + t_rest
            t2 = t_rest + t_pulse + t_rest + t_pulse + t_rest
            ind1 = np.argmin(np.abs(t - t1))
            ind2 = np.argmin(np.abs(t - t2))
            # DW position after positive pulse + settling time
            dx_array[j,i] = x[ind1]
            # DW position after both pulses + settling time
            dx_array_neg[j,i] = x[ind2]

if mode == 1:
    fig,ax = plt.subplots(1,1,figsize=(10,8))

    dx_means = np.median(dx_array,axis=1)
    dx_stds = np.std(dx_array,axis=1)
    dx_means_neg = np.median(dx_array_neg,axis=1)
    dx_stds_neg = np.std(dx_array_neg,axis=1)

    ax.plot(pulse_amps/1e10,dx_means,linewidth=LW,color='tab:blue')
    (_,caps1,_) = ax.errorbar(pulse_amps/1e10,dx_means,yerr=dx_stds,ls="none",linewidth=LW,color="tab:blue",capsize=6)
    for cap in caps1: cap.set_markeredgewidth(LW)

    ax.plot(pulse_amps/1e10,dx_means_neg,color='tab:red',linewidth=LW)
    (_,caps2,_) = ax.errorbar(pulse_amps/1e10,dx_means_neg,yerr=dx_stds,ls="none",linewidth=LW,color="tab:red",capsize=6)
    for cap in caps2: cap.set_markeredgewidth(LW)

    ax.set_axisbelow(True)
    ax.tick_params(labelsize=FS)
    ax.set_xlim([1,3.9])
    ax.set_ylim([0,320])
    ax.set_xlabel(r'Pulse amplitude $\times 10^{10}$ [A/m$^2$]',fontsize=FS,fontname="Arial",labelpad=10)
    ax.set_ylabel('DW displacement [nm])',fontsize=FS,fontname="Arial",labelpad=10)
    ax.set_xticks([1.0,1.5,2.0,2.5,3.0,3.5])
    ax.set_xticklabels(ax.get_xticks(),fontname="Arial")
    ax.set_yticks([0,40,80,120,160,200,240,280,320])
    ax.set_yticklabels(ax.get_yticks().astype(int),fontname="Arial")
    ax.grid(which="both",color="#E2E2E2")
    plt.savefig("var_2ns.svg",bbox_inches="tight")

elif mode == 2:
    fig,ax = plt.subplots(1,1,figsize=(12,8))

    # Pulse start and end
    ax.plot([t_rest/1e-9,t_rest/1e-9],[0,320],'--k',linewidth=LW)
    ax.plot(np.array([t_rest/1e-9,t_rest/1e-9])+t_pulse/1e-9,[0,320],'--k',linewidth=LW)
    ax.plot(np.array([t_rest/1e-9,t_rest/1e-9])+(t_pulse+t_rest)/1e-9,[0,320],'--k',linewidth=LW)
    ax.plot(np.array([t_rest/1e-9,t_rest/1e-9])+(2*t_pulse+t_rest)/1e-9,[0,320],'--k',linewidth=LW)

    for i in range(nseeds):
        ax.plot(t/1e-9,dw_pos[i,:],linewidth=LW,label="{:.1f}".format(pulse_amps[0]/1e10))
    ax.grid(which="both",color="#E2E2E2")
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=FS)
    ax.set_xlim([0,19])
    ax.set_ylim([0,320])
    ax.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
    ax.set_ylabel('DW position (nm)',fontsize=FS,fontname="Arial")
    ax.set_xticks([0,2,4,6,8,10,12,14,16,18])
    ax.set_xticklabels(["0","2","4","6","8","10","12","14","16","18"],fontname="Arial")
    ax.set_yticks([0,40,80,120,160,200,240,280,320])
    ax.set_yticklabels(ax.get_yticks().astype(int),fontname="Arial")
    plt.savefig("var_waveform.svg",bbox_inches="tight")

elif mode == 3:
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(16,6))
    plt.subplots_adjust(wspace=0.3)
    x_L = 120 # MTJ left
    x_R = 160 # MTJ right
    Dx = x_R - x_L

    # Plot t vs DW position
    ax1.plot([t_rest/1e-9,t_rest/1e-9],[0,320],'--k',linewidth=LW)
    ax1.plot(np.array([t_rest/1e-9,t_rest/1e-9])+t_pulse/1e-9,[0,320],'--k',linewidth=LW)
    ax1.plot(np.array([t_rest/1e-9,t_rest/1e-9])+(t_pulse+t_rest)/1e-9,[0,320],'--k',linewidth=LW)
    ax1.plot(np.array([t_rest/1e-9,t_rest/1e-9])+(2*t_pulse+t_rest)/1e-9,[0,320],'--k',linewidth=LW)
    ax1.plot([10,18],[x_L,x_L],'--k',linewidth=LW)
    ax1.plot([10,18],[x_R,x_R],'--k',linewidth=LW)
    for i in range(nseeds):
        ax1.plot(t/1e-9,dw_pos[i,:],linewidth=LW,label="{:.1f}".format(pulse_amps[0]/1e10))
    ax1.grid(which="both",color="#E2E2E2")
    ax1.set_axisbelow(True)
    ax1.tick_params(labelsize=FS)
    ax1.set_xlim([10,18])
    ax1.set_ylim([0,320])
    ax1.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
    ax1.set_ylabel('DW position (nm)',fontsize=FS,fontname="Arial")
    ax1.set_xticks([10,11,12,13,14,15,16,17,18])
    ax1.set_xticklabels(["10","","12","","14","","16","","18"],fontname="Arial")
    ax1.set_yticks([0,40,80,120,160,200,240,280,320])
    ax1.set_yticklabels(ax1.get_yticks().astype(int),fontname="Arial")

    # Plot t vs current that will go through the second device
    J_resets = np.zeros(dw_pos.shape)
    TMR = 2.0

    # Assume that if MTJ is on, all the input current flows through it, and none to the left end of the
    # track. This is not realistic and should be replaced by a resistive divider model
    J_high = pulse_amps[0]/1e10
    J_low = J_high/(1 + TMR)

    # Get J vs time based on DW position
    for i in range(nseeds):
        J_i = J_high * (dw_pos[i,:] > x_R)
        J_i += J_low * (dw_pos[i,:] < x_L)
        J_i += (1/((1/J_high)*(dw_pos[i,:] - x_L)/Dx + (1/J_low)*(x_R - dw_pos[i,:])/Dx)) \
            * (dw_pos[i,:] <= x_R) * (dw_pos[i,:] >= x_L)
        J_i *= (t > (t_pulse + 2*t_rest))
        J_i *= (t < (2*t_pulse + 2*t_rest))
        J_resets[i,:] = J_i
        ax2.plot(t/1e-9,J_i,linewidth=LW)

    ax2.grid(which="both",color="#E2E2E2")
    ax2.set_axisbelow(True)
    ax2.tick_params(labelsize=FS)
    ax2.set_xlim([10,18])
    ax2.set_ylim([0,4.5])
    ax2.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
    ax2.set_ylabel(r'J$_2$ (A/m$^2$)',fontsize=FS,fontname="Arial")
    ax2.set_xticks([10,11,12,13,14,15,16,17,18])
    ax2.set_xticklabels(["10","","12","","14","","16","","18"],fontname="Arial")
    ax2.set_yticks([0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5])
    ax2.set_yticklabels(["0","","1","","2","","3","","4",""],fontname="Arial")
    plt.savefig("var_waveform_reset.svg",bbox_inches="tight")

    # Save the current
    t_reset0 = t[t > 10e-9] - 10e-9
    t_reset = t_reset0[t_reset0 <= 8e-9]
    t_reset[0] = 0

    # Crop and resample current waveform to some fixed dt
    J_reset_sample = np.zeros((nseeds,len(t_reset)))
    for i in range(nseeds):
        J_reset = J_resets[i,:]
        J_reset2 = J_reset[t > 10e-9]
        J_reset2 = J_reset2[t_reset0 <= 8e-9]
        J_reset_sample[i,:] = J_reset2
    
    dt = 0.05e-9
    t_sample = np.arange(0,8e-9,dt)
    J_sample = np.zeros((nseeds,len(t_sample)))
    from scipy.interpolate import interp1d
    for i in range(nseeds):
        interp_J_i = interp1d(t_reset,J_reset_sample[i,:])
        J_sample_i = interp_J_i(t_sample)
        J_sample_i[J_sample_i < 0] = 0
        J_sample[i,:] = J_sample_i

    J_val = (1.0e+10 + pulse_amp_indices[0]*0.1e+10)/1.0e+10
    # J_val = jx
    # np.save("J_reset_{:.2f}".format(J_val)+"e10_TMR="+str(int(TMR*100))+".npy",J_sample)
    np.save("J_reset_3.0e10_TMR="+str(int(TMR*100))+".npy",J_sample)

plt.show()
