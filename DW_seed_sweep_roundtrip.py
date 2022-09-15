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

seedlist = np.array([480729151,539132639,594026345,675324135,686123422,701027736,\
        701258021,709705655,944973596,962102195, 3737392, 102375943, 392749, 75849383, \
        2748383, 67363, 8474, 203938, 9833245, 82873, 182933, 27838393, 282937, 96544, \
        73832839, 8943829, 6849373, 50938292, 2829383, 283749, 837, 883320, 5038322, \
        6302833, 8464939, 27293, 740038, 87393222, 32, 85948, 8292, 0, 58392223, \
        49403, 3938277, 859493, 7283, 293873, 3653332, 3839],dtype=int)

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
        sizeX = 135e-9
        Nx = 135
        startpos = 35e-9
        rest = 3e-9
        p_dur = 3e-9
        magAn = 4.7e5
        offsetDistance = 22.5e-9
        oxideWidth = 15e-9 
        fixed_w = 5e-9
        VCMA_dur = 1/3

        newfile = newfile + str(seed_j) + "_1.mx3"
        if path.isfile(newfile):
            pass
        else:
            newdata = filedata.replace("j_x := -1.0e+10","j_x := -" + "{:.2e}".format(jx))
            newdata = newdata.replace("p_dur := 1.0e-09","p_dur := " + "{:.2e}".format(p_dur)) #Default was 4.0e-09
            newdata = newdata.replace("randomSeed := 0","randomSeed := " + str(seed_j))
            newdata = newdata.replace("sizeX := 160e-9","sizeX := " + "{:.2e}".format(sizeX))
            newdata = newdata.replace("Nx := 160","Nx := " + str(Nx))
            newdata = newdata.replace("startpos := 50e-9","startpos := " + "{:.2e}".format(startpos))
            newdata = newdata.replace("rest := 3e-9","rest := " + "{:.2e}".format(rest))
            newdata = newdata.replace("magAn := 7e5","magAn := " + "{:.2e}".format(magAn)) 
            newdata = newdata.replace("offsetDistance := 25e-9","offsetDistance := " + "{:.2e}".format(offsetDistance)) #Middle of DW to first edge of oxide contact
            newdata = newdata.replace("oxideWidth := 15e-9","oxideWidth := " + "{:.2e}".format(oxideWidth)) 
            newdata = newdata.replace("fixed_w := 5e-9","fixed_w := " + "{:.2e}".format(fixed_w))
            newdata = newdata.replace("VCMA_dur := 1","VCMA_dur := " + str(VCMA_dur))

            f = open(newfile,'w')
            f.write(newdata)
            f.close()
            os.system("mumax3 " + newfile)
            os.remove(newfile)

newfolder = "Test" + str(Test) + "/"
if os.path.isdir(newfolder):
    shutil.rmtree(newfolder)

os.system("mkdir " + newfolder)
for j in range(0,num_seeds):
    seed_j = seedlist[j]
    folder = "DWswitch_" + str(seed_j) + "_1.out"
    os.system("mv " + folder + " " + newfolder)