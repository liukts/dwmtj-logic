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

# This file processes the simulation results for a DW device driven first by a positive pulse,
# then a negative pulse, to move it back and forth across the magnetic track

Test = 0

#CHECKME Parameters that need to change
t_pulse = 3e-9 # length of current pulse
t_rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
sizeX = 135 # Size of DW (nm)
fixed_w = 5 # Size of fixed ends (nm)
MTJ_w = 15 # Size of the MTJ (nm)
offsetDistance = 22.5 #Distance from middle of DW to edge of contact (nm)
oxideWidth = 15 # Size of Contact (nm)
startpos = 0 #Start position (nm)

# What to plot
# mode 1: Jx vs total DW displacement, with 20 random seeds per Jx
# mode 2: t vs DW position for various seeds, fixed Jx (set below)
# mode 3: t vs DW position for negative pulse, various seeds. Save currents to file to use in concat simulation
mode = 3

seedlist = np.array([1,2,3,4,5,6,\
        7,8,9,10, 11, 12, 13, 14, \
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
        25, 26, 27, 28, 29, 30, 31, 32, 33, \
        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, \
        44, 45, 46, 47, 48, 49, 50],dtype=int)
# seedlist = np.array([480729151],dtype=int)
num_seeds = 3

# Indices for pulse amplitude
if mode == 1:
    # All pulse amplitudes are used
    # pulse_amp_indices = np.arange(0,30,1)
    pulse_amp_indices = [0]
    pulse_amps = np.zeros(len(pulse_amp_indices))
    dx_array = np.zeros((len(pulse_amp_indices),num_seeds))
    dx_array_neg = np.zeros((len(pulse_amp_indices),num_seeds))

elif mode == 2 or mode == 3:
    # Change line below to set pulse amplitude index (the actual Jx is inside for loop below)
    pulse_amp_indices = np.array([29])
    pulse_amps = np.zeros(len(pulse_amp_indices))    

# Load and process DW position data
for i in range(num_seeds):
    seed_i = str(seedlist[i])
    for j in range(len(pulse_amp_indices)):

        # obtain current working directory of data
        # jx = 1.0e+10 + pulse_amp_indices[j]*0.1e+10
        jx = 3.0e+10
        pulse_amps[j] = jx

        jx_str = "{:.1e}".format(jx)
        current_dir = "./Test"+str(Test)+"/DWswitch_"+seed_i+"_1.out"
        cur_data = np.loadtxt(current_dir + '/table.txt')

        if j == 0 and i == 0:
            t = cur_data[:,0]

        # x = (cur_data[:,3] + 1) * (sizeX/2) - fixed_w # translate mz vector to dw_pos
        x = cur_data[:,3] * (sizeX + fixed_w * 2) / 2 + sizeX / 2
        # x = cur_data[:,6] / 1e-9
        if mode == 2 or mode == 3:
            if j == 0 and i == 0:
                dw_pos = np.zeros((num_seeds,len(t)))
            dw_pos[i,:] = x
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

    for i in range(num_seeds):
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
    ax1.plot([0,sizeX],[sizeX/2 - (offsetDistance + oxideWidth),sizeX/2 - (offsetDistance + oxideWidth)],':g',linewidth=2)
    ax1.plot([0,sizeX],[sizeX/2 - offsetDistance,sizeX/2 - offsetDistance],':g',linewidth=2)

    ax1.plot([0,sizeX],[sizeX/2 + offsetDistance,sizeX/2 + offsetDistance],':g',linewidth=2)
    ax1.plot([0,sizeX],[sizeX/2 + offsetDistance + oxideWidth,sizeX/2 + offsetDistance + oxideWidth],':g',linewidth=2)
    
    for i in range(num_seeds):
        ax1.plot(t/1e-9,dw_pos[i,:],linewidth=LW,label="{:.1f}".format(pulse_amps[0]/1e10))
    ax1.grid(which="both",color="#E2E2E2")
    ax1.set_axisbelow(True)
    ax1.tick_params(labelsize=FS)
    # ax1.set_xlim([10,18])
    # ax1.set_xlim([0,18])
    # ax1.set_xlim([0,60])
    ax1.set_xlim([0,max(t/1e-9)])
    ax1.set_ylim([0,sizeX])
    ax1.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
    ax1.set_ylabel('DW position (nm)',fontsize=FS,fontname="Arial")
    # ax1.set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    # ax1.set_xticklabels(["0","","2","","4","","6","","8","","10","","12","","14","","16"],fontname="Arial")
    # ax1.set_yticks([0,50,60,90,112.5,135])
    ax1.set_yticks([0,sizeX/2 - offsetDistance - oxideWidth,sizeX/2 - offsetDistance,x_L,x_R,sizeX/2 + offsetDistance,sizeX/2 + offsetDistance + oxideWidth,135])
    ax1.set_yticklabels(ax1.get_yticks().astype(int),fontname="Arial")

    # Plot t vs current that will go through the second device
    J_resets = np.zeros(dw_pos.shape)
    TMR = 2.0
    r_parallel = 1000
    r_wire = 1000
    r_HM = 1000
    r_half = 0
    resistor0 = 0 # Extra Resistor added to device 0 between clk pin and ground
    resistor1 = 0 # Extra Resistor added to device 1 between clk pin and ground
    resistor2 = 0 # Extra Resistor added to device 2 between clk pin and ground
    rmtj0 = 1000
    rmtj1 = 1000
    fo1 = 1

    # Assume that if MTJ is on, all the input current flows through it, and none to the left end of the
    # track. This is not realistic and should be replaced by a resistive divider model
    # J_high = (pulse_amps[0]/1e10) * (r_wire / 2 + resistor) / ((r_wire / 2) + resistor + ((r_wire * r_HM) / (r_wire + r_HM)) + r_parallel)
    # J_high = (pulse_amps[0]/1e10) * (2*r_half + rmtj0 + resistor0) / (4*r_half + rmtj0 + rmtj1 + resistor0 + resistor2)
    r0 = (2 * r_half + rmtj0) # Effective resistance of device 0
    r1 = (2 * r_half + rmtj1) # Effective resistance of device 0
    if fo1 > 1:
        r1 = (rmtj1 + 2*r_half/fo1)
    J_high = (pulse_amps[0]/1e10) * (r0) / (r0 + r1)
    J_low = J_high/(1 + TMR)

    # Get J vs time based on DW position
    for i in range(num_seeds):
        if rmtj1 == r_parallel:
            if startpos < sizeX/2:
                J_i = J_high
            else:
                J_i = J_high * (dw_pos[i,:] > x_R)
                J_i += J_low * (dw_pos[i,:] < x_L)
                J_i += (1/((1/J_high)*(dw_pos[i,:] - x_L)/Dx + (1/J_low)*(x_R - dw_pos[i,:])/Dx)) \
                    * (dw_pos[i,:] <= x_R) * (dw_pos[i,:] >= x_L)
        else:
            if startpos < sizeX/2:
                J_i = J_low
            else:
                J_i = J_low * (dw_pos[i,:] > x_R)
                J_i += J_high * (dw_pos[i,:] < x_L)
                J_i += (1/((1/J_low)*(dw_pos[i,:] - x_L)/Dx + (1/J_high)*(x_R - dw_pos[i,:])/Dx)) \
                    * (dw_pos[i,:] <= x_R) * (dw_pos[i,:] >= x_L)

        # J_i += J_i
        # J_i *= (t > (t_pulse + 2*t_rest))
        # J_i *= (t < (2*t_pulse + 2*t_rest))
        J_i *= (t > (t_rest))
        J_i *= (t < (t_pulse + t_rest))

        J_resets[i,:] = J_i
        ax2.plot(t/1e-9,J_i,linewidth=LW)

    ax2.grid(which="both",color="#E2E2E2")
    ax2.set_axisbelow(True)
    ax2.tick_params(labelsize=FS)

    # ax2.set_xlim([(t_pulse + 2 * t_rest - 1e-9) * 1e9, (2* t_pulse + 2 * t_rest + 1e-9) * 1e9])
    ax2.set_xlim([(t_rest - 1e-9) * 1e9, (t_pulse + t_rest + 1e-9) * 1e9])

    # ax2.set_ylim([0,4.5])
    ax2.set_ylim([0,15])
    # ax2.set_ylim([0,25])
    ax2.set_xlabel('Time (ns)',fontsize=FS,fontname="Arial")
    ax2.set_ylabel(r'J$_2$ (A/m$^2$)',fontsize=FS,fontname="Arial")
    # ax2.set_xticks([8,9,10,11,12,13])
    # ax2.set_xticklabels(["8","9","10","11","12","13"],fontname="Arial")
    # ax2.set_yticks([0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15])
    # ax2.set_yticklabels(["0","","1","","2","","3","","4","","5","","6","","7","","8","","9","","10","","11","","12","","13","","14","","15"],fontname="Arial")
    plt.savefig("var_waveform_reset.svg",bbox_inches="tight")

    # Save the current
    # t_reset0 = t[t > (t_pulse + 2 * t_rest - 1e-9)] - (t_pulse + 2 * t_rest - 1e-9)
    t_reset0 = t[t > (t_rest - 1e-9)] - (t_rest - 1e-9)

    t_reset = t_reset0[t_reset0 <= (t_pulse + t_rest)]
    t_reset[0] = 0

    # Crop and resample current waveform to some fixed dt
    J_reset_sample = np.zeros((num_seeds,len(t_reset)))
    for i in range(num_seeds):
        J_reset = J_resets[i,:]
        # J_reset2 = J_reset[t > (t_pulse + 2 * t_rest - 1e-9)]
        J_reset2 = J_reset[t > (t_rest - 1e-9)]
        J_reset2 = J_reset2[t_reset0 <= (t_pulse + t_rest)]
        J_reset_sample[i,:] = J_reset2
    
    dt = 0.05e-9
    t_sample = np.arange(0,(t_pulse + t_rest),dt)
    J_sample = np.zeros((num_seeds,len(t_sample)))
    from scipy.interpolate import interp1d
    for i in range(num_seeds):
        interp_J_i = interp1d(t_reset,J_reset_sample[i,:], fill_value="extrapolate")
        J_sample_i = interp_J_i(t_sample)
        J_sample_i[J_sample_i < 0] = 0
        J_sample[i,:] = J_sample_i

    # J_val = (1.0e+10 + pulse_amp_indices[0]*0.1e+10)/1.0e+10
    # J_val = jx
    # np.save("J_reset_{:.2f}".format(J_val)+"e10_TMR="+str(int(TMR*100))+".npy",J_sample)
    # np.save("J_reset_3.0e10_TMR="+str(int(TMR*100))+".npy",J_sample)
    np.save("J_reset_D1_Test" + str(Test) + ".npy", J_sample)

plt.show()

newfolder = "Test" + str(Test) + "/"
os.system("mv J_reset_D1_Test" + str(Test) + ".npy " + newfolder)
os.system("mv var_waveform_reset.svg " + newfolder)