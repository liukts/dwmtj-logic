import os
import math
from os import path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
FS = 30
LW = 3.5
sizeX = 135
offsetDistance = 22.5
oxideWidth = 15
fixed_w = 5
MTJ_w = 15

#sMidpoint is basically -sizeX/2 to sizeX/2 (scaled so just have them at normal values)
# sMidpoint = np.arange(-math.floor(sizeX/2), math.floor(sizeX/2), 0.1).tolist()
# magVal = np.arange(-math.floor(sizeX/2), math.floor(sizeX/2), 0.1).tolist()

sMidpoint = np.linspace(-math.floor(sizeX/2), math.floor(sizeX/2), sizeX)
magVal = np.zeros(sizeX)

for x in range(len(sMidpoint)):
    magVal[x] = 4.88074019590981 + (-2.99219411611410e-05 * x) + (-0.000432730246558269 * pow(sMidpoint[x],2)) 
    magVal[x] = magVal[x] + (6.89289264204922e-08 * pow(sMidpoint[x],3)) + (2.72096040781391e-07 * pow(sMidpoint[x],4))
    magVal[x] = magVal[x] + (-4.84756604766916e-11 * pow(sMidpoint[x],5)) + (2.27421161847804e-11 * pow(sMidpoint[x],6)) 
    magVal[x] = magVal[x] + (1.48725794080439e-14 * pow(sMidpoint[x],7)) + (-5.07091377189594e-14 * pow(sMidpoint[x],8))
    magVal[x] = magVal[x] + (-2.15271398114348e-18 * pow(sMidpoint[x],9)) + (1.29466529825287e-17 * pow(sMidpoint[x],10))
    magVal[x] = magVal[x] + (1.20738451272334e-22 * pow(sMidpoint[x],11)) + (-1.03762546194828e-21 * pow(sMidpoint[x],12))
    # magVal[x] = magVal[x] * 1e5

sMidpoint = np.linspace(0, sizeX, sizeX)

#Plot the Heatmap and the colorbar
# fig, ax = plt.subplots(figsize=[10,10])
# fig, ax = plt.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]})
# fig.set_size_inches(18.5, 10.5)
fig, ax = plt.subplots(sharex = True, squeeze = True, figsize=(16,5))
extent = [sMidpoint[0]-(sMidpoint[1]-sMidpoint[0])/2., sMidpoint[-1]+(sMidpoint[1]-sMidpoint[0])/2.,0,1]

# xval = np.zeros(sizeX)
# xval[]
#Plot for the HeatMap
im = ax.imshow(magVal[np.newaxis,:], 
                cmap='plasma', 
                aspect="auto", 
                extent=extent)
ax.set_yticks([])
ax.set_xlim(extent[0], extent[1])
ax.tick_params(labelsize=FS)
ax.set_xticks([0, 30, 45, 60, 75, 90, 105, 135])
ax.set_xlabel('Free Layer Location (nm)',fontsize=FS,fontname="Arial",labelpad=10)
ax.set_title('Perpendicual Magnetic Anistropy during VCMA',fontsize=FS,fontname="Arial")

#Plot for the Colorbar
# cb = fig.colorbar(im, shrink=0.85, location='bottom', orientation = "horizontal")
cb = fig.colorbar(im, shrink=1, location='right', ticks=[4.75, 4.85, 4.95])
cb.ax.set_ylabel('Magnetic Anistropy (J/$m^3$)',fontsize=FS,fontname="Arial",labelpad=10)
cb.ax.tick_params(labelsize=FS)
# cb.ax.tick([4.7, 4.8, 4.9, 5])

plt.tight_layout()
plt.show()
plt.savefig("heatmap.svg",bbox_inches="tight")