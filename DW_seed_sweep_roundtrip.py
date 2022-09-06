import os
from os import path
import time
import numpy as np

gpu_num = 1
# os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_num)

T1 = time.time()

src_dir = os.getcwd()
root_f = "DWswitch_1.0e+10_1.0e-09_L150_roundtrip.mx3"

# os.system("./mumax3 " + root_f)
num_steps = 1
num_seeds = 3

if gpu_num == 0:
    seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
        317769570,370982442,438702097],dtype=int)
elif gpu_num == 1:
    seedlist = np.array([480729151,539132639,594026345,675324135,686123422,701027736,\
        701258021,709705655,944973596,962102195],dtype=int)

for j in range(0,num_seeds):
    seed_j = seedlist[j]
    for i in range(0,num_steps):
        tempf = root_f.split("_")
        f = open(root_f,'r')
        filedata = f.read()
        f.close()

        newfile = "DWswitch_"
        jx = float(tempf[1])
        # jx += i*0.1e+10
        jx = 3.0e+10

        tempf[1] = "{:.1e}".format(jx)
        tempf[2] = str(seed_j)
        for z in range(1,len(tempf)):
            newfile += tempf[z] + "_"
        newfile = newfile[:-1]
        if path.isfile(newfile):
            pass
        else:
            newdata = filedata.replace("j_x := -1.0e+10","j_x := -" + "{:.1e}".format(jx))
            newdata = newdata.replace("p_dur := 1.0e-09","p_dur := 5.0e-09")
            newdata = newdata.replace("randomSeed := 0","randomSeed := " + str(seed_j))
            newdata = newdata.replace("sizeX := 160e-9","sizeX := 320e-9")
            newdata = newdata.replace("Nx := 160","Nx := 320")
            f = open(newfile,'w')
            f.write(newdata)
            f.close()
            os.system("mumax3 " + newfile)
            os.remove(newfile)


T2 = time.time()
print("Elapsed time: {:.4f}".format(T2-T1)+"s")