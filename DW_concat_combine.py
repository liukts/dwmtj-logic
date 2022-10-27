import os
from os import path
import time
import numpy as np

gpu_num = 0
os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_num)

Test = 0

src_dir = os.getcwd()
root_f = "DWswitch_concat.mx3"

# os.system("./mumax3 " + root_f)

J_LAA = np.load("./Output_Current/J_LAA.npy")
J_LAP = np.load("./Output_Current/J_LAP.npy")
J_LPA = np.load("./Output_Current/J_LPA.npy")
J_LPP = np.load("./Output_Current/J_LPP.npy")
J_RAA = np.load("./Output_Current/J_RAA.npy")
J_RAP = np.load("./Output_Current/J_RAP.npy")
J_RPA = np.load("./Output_Current/J_RPA.npy")
J_RPP = np.load("./Output_Current/J_RPP.npy")

Nsamples = J_LAA.shape[1]

# if gpu_num == 0:
#     seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
#         317769570,370982442,438702097],dtype=int)
# elif gpu_num == 1:
#     seedlist = np.array([480729151,539132639,594026345,675324135,686123422,701027736,\
#         701258021,709705655,944973596,962102195],dtype=int)

seedlist = np.array([52,53,54,55,56,\
        57,58,59,60, 61, 62, 63, 64, \
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74, \
        75, 76, 77, 78, 79, 80,81, 82, 83, \
        84, 85, 86, 87, 88, 89, 90, 91, 92, 93, \
        94, 95, 96, 97, 98, 99, 100],dtype=int)
num_seeds = 1


VCMA = open("VCMA.txt",'r')
VCMAdata = VCMA.read()
VCMA.close()    

r_HM = 1000
r_wire = 1000

for j in range(0,num_seeds):
    J_reset = (J_LAA)/6
    seed_j = seedlist[j]

    tempf = root_f.split("_")
    f = open(root_f,'r')
    filedata = f.read()
    f.close()

    newfile = "DWconcat_"
    tempf = str(seed_j)
    newfile += tempf + "_2.mx3"
    if path.isfile(newfile):
        os.remove(newfile)

    sizeX = 135e-9
    Nx = 135
    sizeY = 15e-9 # Width of the Wire
    Ny = 15 # Number of grids in y direction
    startpos = 35e-9
    magAn = 4.7e5
    offsetDistance = 22.5e-9
    oxideWidth = 15e-9 
    fixed_w = 5e-9
    VCMA_dur = 1/3
    p_dur = 3e-9

    newdata = filedata.replace("randomSeed := 0","randomSeed := " + str(seed_j))
    newdata = newdata.replace("sizeX := 320e-9","sizeX := " + "{:.2e}".format(sizeX))
    newdata = newdata.replace("Nx := 320","Nx := " + str(Nx))
    newdata = newdata.replace("sizeY := 15e-9","sizeY := " + "{:.2e}".format(sizeY))
    newdata = newdata.replace("Ny := 15","Ny := " + str(Ny))
    newdata = newdata.replace("startpos := 50e-9","startpos := " + "{:.2e}".format(startpos))
    newdata = newdata.replace("magAn := 7e5","magAn := " + "{:.2e}".format(magAn)) 
    newdata = newdata.replace("offsetDistance := 25e-9","offsetDistance := " + "{:.2e}".format(offsetDistance)) #Middle of DW to first edge of oxide contact
    newdata = newdata.replace("oxideWidth := 15e-9","oxideWidth := " + "{:.2e}".format(oxideWidth))
    newdata = newdata.replace("fixed_w := 5e-9","fixed_w := " + "{:.2e}".format(fixed_w)) 
    newdata = newdata.replace("/* VCMA */", "\n" + VCMAdata + "\n")

    GRAINflag = 0
    for i in range(Nsamples):
        newdata = newdata + "\n" + "j_x"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i]) + "\n" \
                + "j_stt"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i] * (r_HM / 2) / (r_wire / 2 + r_HM / 2)) + "\n" \
                + "j_sot"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i] * (r_wire / 2) / (r_wire / 2 + r_HM / 2)) + "\n" \
                + "J = vector(j_stt"+str(i)+", 0, j_sot" + str(i) + ")\n" + "tau_RE = (alpha_R * (j_stt" + str(i) + " / 2) * stt_P) / (u_B * Ms)" \
                + "\nB_ext = vector(0, tau_RE, 0)\nrun(dt_step)\n"

        if i == (20 + (1 - VCMA_dur) * p_dur / 1e-9 * 20 + 1): #Statement to turn on VCMA Pinning
            replaceString = "j_x"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i]) + "\n" + VCMAdata + "\n"
            newdata = newdata.replace("j_x"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i]),replaceString)
        elif (GRAINflag == 0) and (J_reset[j,i] != 0): #Set up graining after the first rest
            GRAINflag = 1
            GRAIN = open("GRAIN.txt",'r')
            GRAINdata = GRAIN.read()
            GRAIN.close()
            replaceString = "j_x"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i]) + "\n" + GRAINdata + "\n"
            newdata = newdata.replace("j_x"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i]),replaceString)
            
    f = open(newfile,'w')
    f.write(newdata)
    f.close()
    os.system("mumax3 " + newfile)
    os.remove(newfile)

newfolder = "Test" + str(Test) + "/"
for j in range(0,num_seeds):
    seed_j = seedlist[j]
    folder = "DWconcat_" + str(seed_j) + "_2.out"
    os.system("mv " + folder + " " + newfolder)