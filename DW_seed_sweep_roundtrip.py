import os
from os import path
import time
import numpy as np
import shutil

gpu_num = 1
# os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_num)

Test = 0

src_dir = os.getcwd()
root_f = "DWswitch_roundtrip.mx3"

# os.system("./mumax3 " + root_f)
num_steps = 1
num_seeds = 3

# if gpu_num == 0:
#     seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
#         317769570,370982442,438702097],dtype=int)
# elif gpu_num == 1:
#     seedlist = np.array([480729151,539132639,594026345,675324135,686123422,701027736,\
#         701258021,709705655,944973596,962102195],dtype=int)

seedlist = np.array([1,2,3,4,5,6,\
        7,8,9,10, 11, 12, 13, 14, \
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
        25, 26, 27, 28, 29, 30, 31, 32, 33, \
        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, \
        44, 45, 46, 47, 48, 49, 50],dtype=int)

VCMA = open("VCMA.txt",'r')
VCMAdata = VCMA.read()
VCMA.close()   

GRAIN = open("GRAIN.txt",'r')
GRAINdata = GRAIN.read()
GRAIN.close()

for j in range(0,num_seeds):
    seed_j = seedlist[j]
    for i in range(0,num_steps):
        # tempf = root_f.split("_")
        f = open(root_f,'r')
        filedata = f.read()
        f.close()

        newfile = "DWswitch_"
        # jx = float(tempf[1])
        # jx += i*0.1e+10
        jx = 3.0e+10
        j_sot = jx
        j_stt = jx
        rmtj0 = 1000
        rmtj1 = 1000
        sizeX = 135e-9
        Nx = 135
        sizeY = 15e-9
        Ny = 15
        startpos = 35e-9
        rest = 3e-9
        p_dur = 3e-9
        magAn = 4.7e5
        offsetDistance = 22.5e-9
        oxideWidth = 15e-9 
        fixed_w = 5e-9
        VCMA_dur = 1/3
        left = False
        dt_step = 0.05e-09
        notch_flag = 0
        unotch_only = 0
        edge_rough = 0
        notch_dia = 3e-9

        newfile = newfile + str(seed_j) + "_1.mx3"
        if path.isfile(newfile):
            pass
        else:
            newdata = filedata.replace("j_x := -1.0e+10","j_x := -" + "{:.2e}".format(jx))
            newdata = newdata.replace("j_stt := j_x", "j_stt := -" + "{:.2e}".format(j_stt), 1)
            newdata = newdata.replace("j_sot := j_x", "j_sot := -" + "{:.2e}".format(j_sot), 1)
            newdata = newdata.replace("j_sttAMTJ := j_x", "j_sttAMTJ := -" + "{:.2e}".format(j_stt * (rmtj1) / (rmtj0 + rmtj1)), 1)
            newdata = newdata.replace("j_sotAMTJ := j_x", "j_sotAMTJ := -" + "{:.2e}".format(j_sot * (rmtj1) / (rmtj0 + rmtj1)), 1)
            newdata = newdata.replace("p_dur := 1.0e-09","p_dur := " + "{:.2e}".format(p_dur))
            newdata = newdata.replace("randomSeed := 0","randomSeed := " + str(seed_j))
            newdata = newdata.replace("sizeX := 160e-9","sizeX := " + "{:.2e}".format(sizeX))
            newdata = newdata.replace("Nx := 160","Nx := " + str(Nx))
            newdata = newdata.replace("sizeY := 15e-9","sizeY := " + "{:.2e}".format(sizeY))
            newdata = newdata.replace("Ny := 15","Ny := " + str(Ny))
            newdata = newdata.replace("startpos := 50e-9","startpos := " + "{:.2e}".format(startpos))
            newdata = newdata.replace("rest := 3e-9","rest := " + "{:.2e}".format(rest))
            newdata = newdata.replace("magAn := 7e5","magAn := " + "{:.2e}".format(magAn)) 
            newdata = newdata.replace("offsetDistance := 25e-9","offsetDistance := " + "{:.2e}".format(offsetDistance)) #Middle of DW to first edge of oxide contact
            newdata = newdata.replace("oxideWidth := 15e-9","oxideWidth := " + "{:.2e}".format(oxideWidth)) 
            newdata = newdata.replace("fixed_w := 5e-9","fixed_w := " + "{:.2e}".format(fixed_w))
            newdata = newdata.replace("/* VCMA */", "\n" + VCMAdata + "\n")
            newdata = newdata.replace("notch_flag := 0","notch_flag := " + str(notch_flag), 1)
            newdata = newdata.replace("unotch_only := 0","unotch_only := " + str(unotch_only), 1)
            newdata = newdata.replace("edge_rough := 0","edge_rough := " + str(edge_rough), 1)
            newdata = newdata.replace("notch_diam := 3e-9", "notch_diam := " + "{:.2e}".format(notch_dia))

            Nsamples = int((p_dur) / dt_step) #No need to do this for the first resting phase
            negateFLAG = 1 #Negate Flag in order to see if the direction needs to be negated
            CURRENTFLAG = 0 # Flag signifying current being 0
            VCMAFLAG = 0 #Flag to signify if VCMA is applied
            for k in range(Nsamples):
                if k == ((p_dur * VCMA_dur) / dt_step): #Add Grianing to being second pulse
                    newdata = newdata + "\n" + GRAINdata + "\n" #Add graining to the freelayer track
                    CURRENTFLAG = 0
                # elif k == ((p_dur) / dt_step): #Add VCMA to begin third rest
                #     newdata = newdata + "\n" + VCMAdata + "\n" #Apply VCMA to the freelayer track
                #     CURRENTFLAG = 1

                if CURRENTFLAG:
                    newdata = newdata + "J = vector(0, 0, 0)\nB_ext = vector(0, 0, 0)\nrun(dt_step)\n"
                elif negateFLAG: #Move the Domain Wall to the Left
                    newdata = newdata + "\nif (m.comp(2).average() * (sizeX + fixed_w * 2) / 2 + sizeX / 2) <= sizex/2 {"
                    newdata = newdata + "\n\tJ = vector(-j_sttAMTJ, 0, -j_sotAMTJ*scale2hm)\n\tB_ext = vector(0, -tau_REAMTJ, 0)\n\trun(dt_step)\n} else {" #Moving Domain Wall Left (Left of MTJ)
                    newdata = newdata + "\n\tJ = vector(-j_stt, 0, -j_sot*scale2hm)\n\tB_ext = vector(0, -tau_RE, 0)\n\trun(dt_step)\n}\n" #Moving Domain Wall Left (Right of MTJ)
                else: #Move the Domain Wall to the Right
                    newdata = newdata + "\nif (m.comp(2).average() * (sizeX + fixed_w * 2) / 2 + sizeX / 2) <= sizex/2 {"
                    newdata = newdata + "\n\tJ = vector(j_sttAMTJ, 0, j_sotAMTJ*scale2hm)\n\tB_ext = vector(0, tau_REAMTJ, 0)\n\trun(dt_step)\n} else {" #Moving Domain Wall Right (Left of MTJ)
                    newdata = newdata + "\n\tJ = vector(j_stt, 0, j_sot*scale2hm)\n\tB_ext = vector(0, tau_RE, 0)\n\trun(dt_step)\n}\n" #Moving Domain Wall Right (Right of MTJ)

            newdata = newdata + "\n" + VCMAdata + "\n" #Apply VCMA to the freelayer track
            newdata = newdata + "\nrun(rest)\n"
            f = open(newfile,'w')
            f.write(newdata)
            f.close()
            os.system("mumax3 " + newfile)
            os.remove(newfile)

for j in range(0, num_seeds):
    seed_j = seedlist[j]
    folder = "DWswitch_" + str(seed_j) + "_1.out"
    os.system("mumax3-convert -png " + folder + "/*.ovf")

newfolder = "Test" + str(Test) + "/"
if os.path.isdir(newfolder):
    shutil.rmtree(newfolder)

os.system("mkdir " + newfolder)
for j in range(0,num_seeds):
    seed_j = seedlist[j]
    folder = "DWswitch_" + str(seed_j) + "_1.out"
    os.system("mv " + folder + " " + newfolder)