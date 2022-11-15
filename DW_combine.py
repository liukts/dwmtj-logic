import os
from os import path
import time
import numpy as np

T1 = time.time()
Test = 0 #Test number
Test1 = 0
Test2 = 0

# FIRST (Parameters to modify for different runs)
num_seeds = 1 # Number of seeds up to 50 to run for same test
jx = 1e+10 # Current Density
voltage_pulse = 55.0e-3 # Voltage Pulse
p_dur = 2e-9 # length of current pulse

sizeX = 135e-9 # Size of DW
Nx = 135 # Number of grids in x direction
sizeY = 15e-9 # Width of the Wire
Ny = 15 # Number of grids in y direction
sizeZ = 3e-9 # Thickness of the Wire
Nz = 1 # Number of grinds in the z direction
thick_HM = 3e-9 # Thickness of HM (nm)
right = 110e-9 # Right side of the DW Track
left = 10e-9 # Left side of the DW Track
startpos = right # Start position of the DW
rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
magAn = 4.7e5 # Magnetic Anisotrophy from VCMA
offsetDistance = 22.5e-9 #Distance from middle of DW to edge of contact (nm)
oxideWidth = 15e-9 # Size of Contact (nm)
fixed_w = 5e-9 # Size of fixed ends (nm)
MTJ_w1 = 15e-9 # Size of the MTJ1 (nm)
MTJ_w2 = 15e-9 # Size of the MTJ2 (nm)
VCMA_dur = 0 # Ratio of pinning effect during current pulse (Ratio needs to be less than 1 to work correctly)
VCMA = 5.00 # minimum PMA value
TMR = 0.9 # TMR of the MTJ
resistivity_CoFeB = 500 # (uOhm*cm)
resistivity_HM = 40 # Pt (uOhm * cm)
r_parallel = 3000 # Resistance of MTJ in parallel State
r_ap = TMR * r_parallel + r_parallel # Resistance of MTJ in antiparallel state

#Assumption is that the same resistance levels for all devices
rmtj0 = r_parallel #Resistance of device 0
rmtj1 = r_parallel #Resistance of device 1

#Fanout for each device
fo0 = 1 #Fanout of device 0
fo1 = 1 #Fanout of device 1
fo2 = 1 #Fanout of device 2

simulate_deivce = 0 # This is a 1 or 0 depending on if there has already been a simulation in place
multiple_input = False

# Resistance calculation for the MTJ
r_parallel1 = r_parallel
if fo0 != 1/2:
    rmtj0 = rmtj0 / (3**fo0)
if fo1 != 1/2:
    rmtj1 = rmtj1 / (3**fo1)
    r_parallel1 = r_parallel1 / (3**fo1)

#Resistors Added when the Fanout is not 1
resistor0 = 0 # Extra Resistor added to device 0 between clk pin and ground
resistor1 = 0 # Extra Resistor added to device 1 between clk pin and ground
resistor2 = 0 # Extra Resistor added to device 2 between clk pin and ground

#Notches and Edge Roughness
notch_flag = 1
unotch_only = 1
edge_rough = 0
notch_dia = 3

#Calculation for resistance for device 1
r_wire = resistivity_CoFeB * (1e-6 * 1e-2) * sizeX / (sizeY * sizeZ)
r_HM = resistivity_HM * (1e-6 * 1e-2) * sizeX / (sizeY * thick_HM)
r_half = (r_wire/2 * r_HM/2) / (r_wire/2 + r_HM/2)
r0 = (2 * r_half + rmtj0) # Effective resistance of device 0
r1 = (2 * r_half + rmtj1) # Effective resistance of device 0
if fo1 > 1:
    r1 = (rmtj1 + 2*r_half/fo1)
# r_eff = (r_half + ((2 * r_half + rmtj0) * (2* r_half + rmtj1)) / ((2 * r_half + rmtj0) + (2 * r_half + rmtj1)))
r_eff = (r_half + ((r0) * (r1)) / ((r0) + (r1)))

#Calculate for current density for device 1
jx = voltage_pulse / r_eff / (sizeY * (thick_HM + sizeZ))
j_sot = jx * (r_wire) / (r_wire + r_HM)
j_stt = jx * (r_HM) / (r_wire + r_HM)

#Calculation for Energy of the voltage pulse
energy = (voltage_pulse * voltage_pulse / r_eff) * p_dur

# FOURTH (Change parameters and run DW_concat.py)
root_f = "DW_concat.py"
f = open(root_f, 'r')
filedata = f.read()
f.close()

# Modify the roundtrip wrapper to have updated parameters
newdata = filedata.replace("num_seeds = 3", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("sizeX = 135e-9", "sizeX = " + "{:.2e}".format(sizeX), 1)
newdata = newdata.replace("Nx = 135", "Nx = " + str(Nx), 1)
newdata = newdata.replace("sizeY = 15e-9", "sizeY = " + "{:.2e}".format(sizeY), 1)
newdata = newdata.replace("Ny = 15", "Ny = " + str(Ny), 1)
newdata = newdata.replace("rest = 3e-9", "rest = " + "{:.2e}".format(rest), 1)
newdata = newdata.replace("p_dur = 3e-9", "p_dur = " + "{:.2e}".format(p_dur), 1)
newdata = newdata.replace("magAn = 4.7e5", "magAn = " + "{:.2e}".format(magAn), 1)
newdata = newdata.replace("offsetDistance = 22.5e-9", "offsetDistance = " + "{:.2e}".format(offsetDistance), 1)
newdata = newdata.replace("oxideWidth = 15e-9", "oxideWidth = " + "{:.2e}".format(oxideWidth), 1)
newdata = newdata.replace("fixed_w = 5e-9", "fixed_w = " + "{:.2e}".format(fixed_w), 1)
newdata = newdata.replace("VCMA_dur = 1/3", "VCMA_dur = " + str(VCMA_dur), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)
newdata = newdata.replace("r_wire = 1000", "r_wire = " + str(r_wire), 1)
newdata = newdata.replace("r_HM = 1000", "r_HM = " + str(r_HM), 1)
newdata = newdata.replace("notch_flag = 0", "notch_flag = " + str(notch_flag), 1)
newdata = newdata.replace("unotch_only = 0", "unotch_only = " + str(unotch_only), 1)
newdata = newdata.replace("edge_rough = 0", "edge_rough = " + str(edge_rough), 1)
newdata = newdata.replace("notch_dia = 3e-9", "notch_dia = " + "{:.2e}".format((2*fo2 - 1) * notch_dia * 1e-9), 1)
newdata = newdata.replace("simulate_deivce = 0", "simulate_deivce = " + str(simulate_deivce), 1)
newdata = newdata.replace("TMR = 2.0", "TMR = " + str(TMR), 1)
newdata = newdata.replace("Test1 = 0", "Test1 = " + str(Test1), 1)
newdata = newdata.replace("Test2 = 0", "Test2 = " + str(Test2), 1)
newdata = newdata.replace("multiple_input = False", "multiple_input = " + str(multiple_input), 1)
newdata = newdata.replace("VCMA_val = 5.00", "VCMA_val = " + "{:.2e}".format(VCMA), 1)

#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_concat.py" 
f = open(newfile, 'w')
f.write(newdata)
f.close()
if simulate_deivce != 1:
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
newdata = newdata.replace("MTJ_w = 15", "MTJ_w = " + str(MTJ_w2 / 1e-9), 1)
newdata = newdata.replace("Test = 0", "Test = " + str(Test), 1)
newdata = newdata.replace("TMR = 2.0", "TMR = " + str(TMR), 1)
newdata = newdata.replace("simulate_deivce = 0", "simulate_deivce = " + str(simulate_deivce), 1)
newdata = newdata.replace("Test1 = 0", "Test1 = " + str(Test1), 1)
newdata = newdata.replace("Test2 = 0", "Test2 = " + str(Test2), 1)
newdata = newdata.replace("multiple_input = False", "multiple_input = " + str(multiple_input), 1)

#Create a new file from the wrapper
newfile = "Test" + str(Test) + "_get_concat.py"
f = open(newfile, 'w')
f.write(newdata)
f.close()
if simulate_deivce != 1:
    os.system("python3 " + newfile)
os.remove(newfile)

#Save the Energy Calculation
EnergyFile = open("Energy.txt",'w')
EnergyFile.write(str(energy))
EnergyFile.close()
newfolder = "Test" + str(Test) + "/"
os.system("mv Energy.txt " + newfolder)