import os
from os import path
import time
import numpy as np
import shutil


T1 = time.time()

# Size Parameters
sizeX = 135e-9 # Size of DW
Nx = 135 # Number of grids in x direction
sizeY = 15e-9 # Width of the Wire
Ny = 15 # Number of grids in y direction
sizeZ = 3e-9 # Thickness of the Wire
Nz = 1 # Number of grinds in the z direction
thick_HM = 3e-9 # Thickness of HM (nm)

# Position Parameters
offsetDistance = 22.5e-9 #Distance from middle of DW to edge of contact (nm)
oxideWidth = 15e-9 # Size of Contact (nm)
MTJ_w = 15e-9 # Size of the MTJ (nm)
right = 110e-9 # Right side of the DW Track
left = 10e-9 # Left side of the DW Track

# Resistance Parameters
resistivity_CoFeB = 500 # (uOhm*cm)
resistivity_HM = 40 # Pt (uOhm * cm)

#Notches and Edge Roughness Parameters
notch_flag = 1
unotch_only = 1
edge_rough = 0
notch_dia = 3

#Fanout of the Devices
fo0 = 1 #Fanout of device 0
fo1 = 1 #Fanout of device 1
fo2 = 1 #Fanout of device 2

# (CHECKME) Parameters that will be changed
Test = 0 #Test number
num_seeds = 1 # Number of seeds up to 50 to run for same test
rest = 3e-9 # length of settling time with no current (time before pulse 1, between pulses, and after pulse 2)
voltage_pulse = 55.0e-3 # Voltage Pulse (55 mV required for single fo)
VCMA_dur = 0 # Ratio of pinning effect during current pulse (Ratio needs to be less than 1 to work correctly)
VCMA = 4.70 # minimum PMA value
TMR = 0.90 # TMR of the MTJ
simulate_deivce = 0 # (Basically what device to simulate) 1 device 1 2 device 2
multiple_input = False # If the device is going to be used as multiple input

# Replacing all the data
if not multiple_input:
    root_f = "DW_wrapper.py"
else:
    root_f = "DW_combine.py"

f = open(root_f, 'r')
filedata = f.read()
f.close()

newdata = filedata.replace("sizeX = 135e-9", "sizeX = " + "{:.2e}".format(sizeX), 1)
newdata = newdata.replace("sizeY = 15e-9", "sizeY = " + "{:.2e}".format(sizeY), 1)
newdata = newdata.replace("sizeZ = 3e-9", "sizeZ = " + "{:.2e}".format(sizeZ), 1)
newdata = newdata.replace("Nx = 135", "Nx = " + str(Nx), 1)
newdata = newdata.replace("Ny = 15", "Ny = " + str(Ny), 1)
newdata = newdata.replace("Nz = 1", "Nz = " + str(Nz), 1)
newdata = newdata.replace("thick_HM = 3e-9", "thick_HM = " + "{:.2e}".format(thick_HM), 1)
newdata = newdata.replace("offsetDistance = 22.5e-9", "offsetDistance = " + "{:.2e}".format(offsetDistance), 1)
newdata = newdata.replace("oxideWidth = 15e-9", "oxideWidth = " + "{:.2e}".format(oxideWidth), 1)
newdata = newdata.replace("MTJ_w = 15e-9", "MTJ_w = " + "{:.2e}".format(MTJ_w), 1)
newdata = newdata.replace("right = 110e-9", "right = " + "{:.2e}".format(right), 1)
newdata = newdata.replace("left = 10e-9", "left = " + "{:.2e}".format(left), 1)
newdata = newdata.replace("resistivity_CoFeB = 500", "resistivity_CoFeB = " + str(resistivity_CoFeB), 1)
newdata = newdata.replace("resistivity_HM = 40", "resistivity_HM = " + str(resistivity_HM), 1)
newdata = newdata.replace("notch_flag = 1", "notch_flag = " + str(notch_flag), 1)
newdata = newdata.replace("unotch_only = 1", "unotch_only = " + str(unotch_only), 1)
newdata = newdata.replace("edge_rough = 0", "edge_rough = " + str(edge_rough), 1)
newdata = newdata.replace("notch_dia = 3", "notch_dia = " + str(notch_dia), 1)
newdata = newdata.replace("num_seeds = 1", "num_seeds = " + str(num_seeds), 1)
newdata = newdata.replace("rest = 3e-9", "rest = " + "{:.2e}".format(rest), 1)
newdata = newdata.replace("voltage_pulse = 55.0e-3", "voltage_pulse = " + "{:.2e}".format(voltage_pulse), 1)
newdata = newdata.replace("VCMA_dur = 0", "VCMA_dur = " + str(VCMA_dur), 1)
newdata = newdata.replace("TMR = 0.9", "TMR = " + "{:.2e}".format(TMR), 1)
newdata = newdata.replace("fo0 = 1", "fo0 = " + str(fo0), 1)
newdata = newdata.replace("fo1 = 1", "fo1 = " + str(fo1), 1)
newdata = newdata.replace("fo2 = 1", "fo2 = " + str(fo2), 1)
newdata = newdata.replace("simulate_deivce = 0", "simulate_deivce = " + str(simulate_deivce), 1)
newdata = newdata.replace("multiple_input = False", "multiple_input = " + str(multiple_input), 1)
newdata = newdata.replace("VCMA = 5.00", "VCMA = " + "{:.2e}".format(VCMA), 1)

# Create new folder for all tests to run in
newfolder = "Test" + str(Test) + "/"
if os.path.isdir(newfolder):
    shutil.rmtree(newfolder)

os.system("mkdir " + newfolder)

#Copy (simulation and graphing to directory)
os.system("cp DW_seed_sweep_roundtrip.py " + newfolder)
os.system("cp DW_concat.py " + newfolder)
os.system("cp get_DW_dynamics_roundtrip.py " + newfolder)
os.system("cp get_DW_dynamics_concat.py " + newfolder)
os.system("cp DWswitch_roundtrip.mx3 " + newfolder)
os.system("cp DWswitch_concat.mx3 " + newfolder)
os.system("cp GRAIN.txt " + newfolder)
os.system("cp VCMA/VCMA_" + "{:.2e}".format(VCMA) + ".txt " + newfolder)
os.system("cp -r J_reset_TMR" + str(int(TMR * 100)) + " " + newfolder)

if not multiple_input:
    # (Run the 8 Different orientations based on potiion and all that stuff)
    #Test 1 (DW - R, MTJ0 - P, MTJ1 - P)
    TestNum = 1
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 0", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = right", "startpos = " + "{:.2e}".format(right), 1)
    newdata = newdata.replace("rmtj0 = r_parallel", "rmtj0 = r_parallel", 1)
    newdata = newdata.replace("rmtj1 = r_parallel", "rmtj1 = r_parallel", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 2 (DW - R, MTJ0 - P, MTJ1 - AP)
    TestNum = 2
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 1", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(right), "startpos = " + "{:.2e}".format(right), 1)
    newdata = newdata.replace("rmtj0 = r_parallel", "rmtj0 = r_parallel", 1)
    newdata = newdata.replace("rmtj1 = r_parallel", "rmtj1 = r_ap", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 3 (DW - R, MTJ0 - AP, MTJ1 - P)
    TestNum = 3
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 2", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(right), "startpos = " + "{:.2e}".format(right), 1)
    newdata = newdata.replace("rmtj0 = r_parallel", "rmtj0 = r_ap", 1)
    newdata = newdata.replace("rmtj1 = r_ap", "rmtj1 = r_parallel", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 4 (DW - R, MTJ0 - AP, MTJ1 - AP)
    TestNum = 4
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 3", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(right), "startpos = " + "{:.2e}".format(right), 1)
    newdata = newdata.replace("rmtj0 = r_ap", "rmtj0 = r_ap", 1)
    newdata = newdata.replace("rmtj1 = r_parallel", "rmtj1 = r_ap", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 5 (DW - L, MTJ0 - P, MTJ1 - P)
    TestNum = 5
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 4", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(right), "startpos = " + "{:.2e}".format(left), 1)
    newdata = newdata.replace("rmtj0 = r_ap", "rmtj0 = r_parallel", 1)
    newdata = newdata.replace("rmtj1 = r_ap", "rmtj1 = r_parallel", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 6 (DW - L, MTJ0 - P, MTJ1 - AP)
    TestNum = 6
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 5", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(left), "startpos = " + "{:.2e}".format(left), 1)
    newdata = newdata.replace("rmtj0 = r_parallel", "rmtj0 = r_parallel", 1)
    newdata = newdata.replace("rmtj1 = r_parallel", "rmtj1 = r_ap", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 7 (DW - L, MTJ0 - AP, MTJ1 - P)
    TestNum = 7
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 6", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(left), "startpos = " + "{:.2e}".format(left), 1)
    newdata = newdata.replace("rmtj0 = r_parallel", "rmtj0 = r_ap", 1)
    newdata = newdata.replace("rmtj1 = r_ap", "rmtj1 = r_parallel", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 8 (DW - L, MTJ0 - AP, MTJ1 - AP)
    TestNum = 8
    newfile = "Test" + str(TestNum) + "_wrapper.py" 
    newdata = newdata.replace("Test = 7", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("startpos = " + "{:.2e}".format(left), "startpos = " + "{:.2e}".format(left), 1)
    newdata = newdata.replace("rmtj0 = r_ap", "rmtj0 = r_ap", 1)
    newdata = newdata.replace("rmtj1 = r_parallel", "rmtj1 = r_ap", 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)
else:
    #This is used for NAND Simulation ‘00’, ‘01’, ‘11’ 
    #Test 1 ('11')
    TestNum = 1
    Test1 = 1
    Test2 = 1
    newfile = "Test" + str(TestNum) + "_combine.py" 
    newdata = newdata.replace("Test = 0", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("Test1 = 0", "Test1 = " + str(Test1), 1)
    newdata = newdata.replace("Test2 = 0", "Test2 = " + str(Test2), 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 2 ('10')
    TestNum = 2
    pTest1 = Test1
    pTest2 = Test2
    Test1 = 1
    Test2 = 5
    newfile = "Test" + str(TestNum) + "_combine.py" 
    newdata = newdata.replace("Test = 1", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("Test1 = " + str(pTest1), "Test1 = " + str(Test1), 1)
    newdata = newdata.replace("Test2 = " + str(pTest2), "Test2 = " + str(Test2), 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)

    #Test 3 ('00')
    TestNum = 3
    pTest1 = Test1
    pTest2 = Test2
    Test1 = 5
    Test2 = 5
    newfile = "Test" + str(TestNum) + "_combine.py" 
    newdata = newdata.replace("Test = 2", "Test = " + str(TestNum), 1)
    newdata = newdata.replace("Test1 = " + str(pTest1), "Test1 = " + str(Test1), 1)
    newdata = newdata.replace("Test2 = " + str(pTest2), "Test2 = " + str(Test2), 1)

    f = open(newfolder + newfile, 'w')
    f.write(newdata)
    f.close()
    os.chdir(newfolder)
    os.system("python3 " + newfile)
    os.chdir("../")
    os.remove(newfolder + newfile)



#Remove all the uneccessary files in the new directory
os.remove(newfolder + "DW_seed_sweep_roundtrip.py")
os.remove(newfolder + "DW_concat.py")
os.remove(newfolder + "get_DW_dynamics_roundtrip.py")
os.remove(newfolder + "get_DW_dynamics_concat.py")
os.remove(newfolder + "DWswitch_roundtrip.mx3")
os.remove(newfolder + "DWswitch_concat.mx3")
os.remove(newfolder + "GRAIN.txt")