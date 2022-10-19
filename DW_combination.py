import os
from os import path
import time
import numpy as np

T1 = time.time()
Test = 0 #Test number

# FIRST (Parameters to modify for different runs)
num_seeds = 1 # Number of seeds up to 50 to run for same test
sizeX = 135e-9 # Size of DW
Nx = 135 # Number of grids in x direction
sizeY = 2*15e-9 # Width of the Wire
Ny = 2*15 # Number of grids in y direction
sizeZ = 3e-9 # Thickness of the Wire
Nz = 1 # Number of grinds in the z direction
thick_HM = 3e-9 # Thickness of HM (nm)
p_dur = 1e-9 # length of current pulse


startpos = 35e-9 # Start position of the DW
rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
magAn = 4.7e5 # Magnetic Anisotrophy from VCMA
offsetDistance = 22.5e-9 #Distance from middle of DW to edge of contact (nm)
oxideWidth = 15e-9 # Size of Contact (nm)
fixed_w = 5e-9 # Size of fixed ends (nm)
MTJ_w = 15e-9 # Size of the MTJ (nm)
VCMA_dur = 0 # Ratio of pinning effect during current pulse

TMR = 2.0 # TMR of the MTJ
resistivity_CoFeB = 500 # (uOhm*cm)
resistivity_HM = 200 # B-W (uOhm * cm)
r_wire = resistivity_CoFeB * (1e-6 * 1e-2) * sizeX / (sizeY * sizeZ)
r_HM = resistivity_HM * (1e-6 * 1e-2) * sizeX / (sizeY * thick_HM)

# FOURTH (Change parameters and run DW_concat.py)
root_f = "DW_concat_combine.py"
f = open(root_f, 'r')
filedata = f.read()
f.close()

# Modify the roundtrip wrapper to have updated parameters
newdata = filedata.replace("num_seeds = 3", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("sizeX = 135e-9", "sizeX = " + "{:.2e}".format(sizeX), 1)
newdata = newdata.replace("Nx = 135", "Nx = " + str(Nx), 1)
newdata = newdata.replace("sizeY = 15e-9", "sizeY = " + "{:.2e}".format(sizeY), 1)
newdata = newdata.replace("Ny = 15", "Ny = " + str(Ny), 1)
newdata = newdata.replace("startpos = 35e-9", "startpos = " + "{:.2e}".format(startpos), 1)
newdata = newdata.replace("p_dur = 3e-9", "p_dur = " + "{:.2e}".format(p_dur), 1)
newdata = newdata.replace("magAn = 4.7e5", "magAn = " + "{:.2e}".format(magAn), 1)
newdata = newdata.replace("offsetDistance = 22.5e-9", "offsetDistance = " + "{:.2e}".format(offsetDistance), 1)
newdata = newdata.replace("oxideWidth = 15e-9", "oxideWidth = " + "{:.2e}".format(oxideWidth), 1)
newdata = newdata.replace("fixed_w = 5e-9", "fixed_w = " + "{:.2e}".format(fixed_w), 1)
newdata = newdata.replace("VCMA_dur = 1/3", "VCMA_dur = " + str(VCMA_dur), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)
newdata = newdata.replace("r_wire = 1000", "r_wire = " + str(r_wire), 1)
newdata = newdata.replace("r_HM = 1000", "r_HM = " + str(r_HM), 1)

#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_concat_combine.py" 
f = open(newfile, 'w')
f.write(newdata)
f.close()
os.system("python3 " + newfile)
os.remove(newfile)

# FIFTH (Change parameters and run get_DW_dynamics_concat.py)
root_f = "get_DW_dynamics_concat_combine.py"
f = open(root_f, 'r')
filedata = f.read()
f.close()

# Modify the concat wrapper to have updated parameters
newdata = filedata.replace("num_seeds = 3", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("sizeX = 135", "sizeX = " + str(sizeX / 1e-9), 1)
newdata = newdata.replace("t_rest = 3e-9", "t_rest = " + "{:.2e}".format(rest), 1)
newdata = newdata.replace("t_pulse = 3e-9", "t_pulse = " + "{:.2e}".format(p_dur), 1)
newdata = newdata.replace("offsetDistance = 22.5", "offsetDistance = " + str(offsetDistance / 1e-9), 1)
newdata = newdata.replace("oxideWidth = 15", "oxideWidth = " + str(oxideWidth / 1e-9), 1)
newdata = newdata.replace("fixed_w = 5", "fixed_w = " + str(fixed_w / 1e-9), 1)
newdata = newdata.replace("MTJ_w = 15", "MTJ_w = " + str(MTJ_w / 1e-9), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)

#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_get_concat.py" 
f = open(newfile, 'w')
f.write(newdata)
f.close()
os.system("python3 " + newfile)
os.remove(newfile)
