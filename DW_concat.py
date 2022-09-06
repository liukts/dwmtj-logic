import os
from os import path
import time
import numpy as np

gpu_num = 0
os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_num)

T1 = time.time()

src_dir = os.getcwd()
root_f = "DWswitch_1.0e+10_1.0e-09_L150_concat.mx3"

# os.system("./mumax3 " + root_f)

J_reset = np.load("J_reset_3.0e10_TMR=200.npy")
Nsamples = J_reset.shape[1]

# if gpu_num == 0:
#     seedlist = np.array([1052981872,136925168,151867838,247587902,255367361,258676125,301209998,\
#         317769570,370982442,438702097],dtype=int)
# elif gpu_num == 1:
#     seedlist = np.array([480729151,539132639,594026345,675324135,686123422,701027736,\
#         701258021,709705655,944973596,962102195],dtype=int)

seedlist = np.array([480729151,539132639,594026345],dtype=int)
num_seeds = len(seedlist)

for j in range(0,num_seeds):
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

    newdata = filedata.replace("randomSeed := 0","randomSeed := " + str(seed_j))
    for i in range(Nsamples):
        newdata = newdata.replace("j_x"+str(i)+" = 1.0e10","j_x"+str(i)+" := -" + "{:.5e}".format(1e10*J_reset[j,i]))
    f = open(newfile,'w')
    f.write(newdata)
    f.close()
    os.system("mumax3 " + newfile)
    os.remove(newfile)


T2 = time.time()
print("Elapsed time: {:.4f}".format(T2-T1)+"s")