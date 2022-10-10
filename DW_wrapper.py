import os
from os import path
import time
import numpy as np

T1 = time.time()
Test = 0 #Test number

# FIRST (Parameters to modify for different runs)
num_seeds = 1 # Number of seeds up to 50 to run for same test
jx = 1e+10 # Current Density
voltage_pulse = 26.0e-3 # Voltage Pulse
p_dur = 1e-9 # length of current pulse

sizeX = 135e-9 # Size of DW
Nx = 135 # Number of grids in x direction
sizeY = 15e-9 # Width of the Wire
Ny = 15 # Number of grids in y direction
sizeZ = 3e-9 # Thickness of the Wire
Nz = 1 # Number of grinds in the z direction
thick_HM = 3e-9 # Thickness of HM (nm)

startpos = 35e-9 # Start position of the DW
rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
magAn = 4.7e5 # Magnetic Anisotrophy from VCMA
offsetDistance = 22.5e-9 #Distance from middle of DW to edge of contact (nm)
oxideWidth = 15e-9 # Size of Contact (nm)
fixed_w = 5e-9 # Size of fixed ends (nm)
MTJ_w = 15e-9 # Size of the MTJ (nm)
VCMA_dur = 0 # Ratio of pinning effect during current pulse

r_parallel = 3000 # Resistance of MTJ in parallel State
resistor = 10000 # Extra Resistor to help even out STT and SOT
TMR = 2.0 # TMR of the MTJ
resistivity_CoFeB = 500 # (uOhm*cm)
resistivity_HM = 200 # B-W (uOhm * cm)

#Calculation for resistance for device 1
r_wire = resistivity_CoFeB * (1e-6 * 1e-2) * sizeX / (sizeY * sizeZ)
r_HM = resistivity_HM * (1e-6 * 1e-2) * sizeX / (sizeY * thick_HM)
r_half = (r_wire * r_HM) / (r_wire + r_HM)
r_eff = (r_half + ((2* r_half + r_parallel) * (2* r_half + r_parallel)) / ((2* r_half + r_parallel) + (2* r_half + r_parallel)))

#Calculate for current density for device 1
jx = voltage_pulse / r_eff / (sizeY * (thick_HM + sizeZ))
j_sot = jx * (r_wire / 2) / (r_wire / 2 + r_HM / 2)
j_stt = jx * (r_HM / 2) / (r_wire / 2 + r_HM / 2)
# j_sot = voltage_pulse / r_HM / (sizeY * thick_HM)
# j_stt = voltage_pulse / r_eff / (sizeY * sizeZ)
# j_sot = jx * (r_wire / (r_HM + r_wire))
# j_stt = jx * (r_HM / (r_HM + r_wire))

# SECOND (Change parameters and run DW_seed_sweep_roundtrip.py)
root_f = "DW_seed_sweep_roundtrip.py"
f = open(root_f, 'r')
filedata = f.read()
f.close()

# Modify the roundtrip wrapper to have updated parameters
newdata = filedata.replace("num_seeds = 3", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("jx = 3.0e+10", "jx = " + "{:.2e}".format(jx), 1)
newdata = newdata.replace("sizeX = 135e-9", "sizeX = " + "{:.2e}".format(sizeX), 1)
newdata = newdata.replace("Nx = 135", "Nx = " + str(Nx), 1)
newdata = newdata.replace("startpos = 35e-9", "startpos = " + "{:.2e}".format(startpos), 1)
newdata = newdata.replace("rest = 3e-9", "rest = " + "{:.2e}".format(rest), 1)
newdata = newdata.replace("p_dur = 3e-9", "p_dur = " + "{:.2e}".format(p_dur), 1)
newdata = newdata.replace("magAn = 4.7e5", "magAn = " + "{:.2e}".format(magAn), 1)
newdata = newdata.replace("offsetDistance = 22.5e-9", "offsetDistance = " + "{:.2e}".format(offsetDistance), 1)
newdata = newdata.replace("oxideWidth = 15e-9", "oxideWidth = " + "{:.2e}".format(oxideWidth), 1)
newdata = newdata.replace("fixed_w = 5e-9", "fixed_w = " + "{:.2e}".format(fixed_w), 1)
newdata = newdata.replace("VCMA_dur = 1/3", "VCMA_dur = " + str(VCMA_dur), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)
newdata = newdata.replace("j_stt = jx", "j_stt = " + "{:.2e}".format(j_stt), 1)
newdata = newdata.replace("j_sot = jx", "j_sot = " + "{:.2e}".format(j_sot), 1)

#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_roundtrip.py" 
f = open(newfile, 'w')
f.write(newdata)
f.close()
os.system("python3 " + newfile)
os.remove(newfile)

# THIRD (Change parameters and run get_DW_dynamics_roundtrip.py)
root_f = "get_DW_dynamics_roundtrip.py"
f = open(root_f, 'r')
filedata = f.read()
f.close()

# Modify the roundtrip wrapper to have updated parameters
newdata = filedata.replace("num_seeds = 3", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("jx = 3.0e+10", "jx = " + "{:.2e}".format(jx), 1) #TODO Need to modify this value
newdata = newdata.replace("sizeX = 135", "sizeX = " + str(sizeX / 1e-9), 1)
newdata = newdata.replace("t_rest = 3e-9", "t_rest = " + "{:.2e}".format(rest), 1)
newdata = newdata.replace("t_pulse = 3e-9", "t_pulse = " + "{:.2e}".format(p_dur), 1)
newdata = newdata.replace("offsetDistance = 22.5", "offsetDistance = " + str(offsetDistance / 1e-9), 1)
newdata = newdata.replace("oxideWidth = 15", "oxideWidth = " + str(oxideWidth / 1e-9), 1)
newdata = newdata.replace("fixed_w = 5", "fixed_w = " + str(fixed_w / 1e-9), 1)
newdata = newdata.replace("MTJ_w = 15", "MTJ_w = " + str(MTJ_w / 1e-9), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)
newdata = newdata.replace("TMR = 2.0", "TMR = " + str(TMR), 1)
newdata = newdata.replace("r_parallel = 1000", "r_parallel = " + str(r_parallel), 1)
newdata = newdata.replace("r_wire = 1000", "r_wire = " + str(r_wire), 1)
newdata = newdata.replace("r_HM = 1000", "r_HM = " + str(r_wire), 1)
newdata = newdata.replace("resistor = 0", "resistor = " + str(resistor), 1)


#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_get_roundtrip.py" 
f = open(newfile, 'w')
f.write(newdata)
f.close()
os.system("python3 " + newfile)
os.remove(newfile)

# FOURTH (Change parameters and run DW_concat.py)
root_f = "DW_concat.py"
f = open(root_f, 'r')
filedata = f.read()
f.close()

#Calculate for current density for device 2
# j_sot = voltage_pulse / r_HM / (sizeY * thick_HM)
# j_stt = voltage_pulse / r_eff / (sizeY * sizeZ)

# Modify the roundtrip wrapper to have updated parameters
newdata = filedata.replace("num_seeds = 3", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("sizeX = 135e-9", "sizeX = " + "{:.2e}".format(sizeX), 1)
newdata = newdata.replace("Nx = 135", "Nx = " + str(Nx), 1)
newdata = newdata.replace("startpos = 35e-9", "startpos = " + "{:.2e}".format(startpos), 1)
newdata = newdata.replace("p_dur = 3e-9", "p_dur = " + "{:.2e}".format(p_dur), 1)
newdata = newdata.replace("magAn = 4.7e5", "magAn = " + "{:.2e}".format(magAn), 1)
newdata = newdata.replace("offsetDistance = 22.5e-9", "offsetDistance = " + "{:.2e}".format(offsetDistance), 1)
newdata = newdata.replace("oxideWidth = 15e-9", "oxideWidth = " + "{:.2e}".format(oxideWidth), 1)
newdata = newdata.replace("fixed_w = 5e-9", "fixed_w = " + "{:.2e}".format(fixed_w), 1)
newdata = newdata.replace("VCMA_dur = 1/3", "VCMA_dur = " + str(VCMA_dur), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)
newdata = newdata.replace("j_sot = jx", "j_sot = j_x / " + str(r_HM) + " / " + "{:.2e}".format(sizeY * thick_HM))
newdata = newdata.replace("j_stt = jx", "j_stt = j_x / " + str(r_wire) + " / " + "{:.2e}".format(sizeY * sizeZ))

#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_concat.py" 
f = open(newfile, 'w')
f.write(newdata)
f.close()
os.system("python3 " + newfile)
os.remove(newfile)

# FIFTH (Change parameters and run get_DW_dynamics_concat.py)
root_f = "get_DW_dynamics_concat.py"
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
