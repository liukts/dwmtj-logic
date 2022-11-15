import os
import math
from os import path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
FS = 25
LW = 3.5
sizeX = 255
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
    magVal[x] = 499906.524947088 + (4.88528828379472 * x) + (-3.39575844205535 * pow(sMidpoint[x],2)) 
    magVal[x] = magVal[x] + (-0.00278279289587037 * pow(sMidpoint[x],3)) + (0.00104416207419544 * pow(sMidpoint[x],4))
    magVal[x] = magVal[x] + (4.15916396734823e-07 * pow(sMidpoint[x],5)) + (-6.37886433497943e-07 * pow(sMidpoint[x],6)) 
    magVal[x] = magVal[x] + (-1.14953989820526e-11 * pow(sMidpoint[x],7)) + (1.17294258135377e-10 * pow(sMidpoint[x],8))
    magVal[x] = magVal[x] + (-1.65496260085558e-15 * pow(sMidpoint[x],9)) + (-9.15628459945655e-15 * pow(sMidpoint[x],10))
    magVal[x] = magVal[x] + (1.21267342892931e-19 * pow(sMidpoint[x],11)) + (3.26262534072950e-19 * pow(sMidpoint[x],12))
    magVal[x] = magVal[x] + (-2.29301469365942e-24 * pow(sMidpoint[x],13)) + (-4.35827392584609e-24 * pow(sMidpoint[x],14))

magVal = magVal / 1e3
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
ax.set_xticks([0, 30, 45, 210, 225, 255])
ax.set_xlabel('Free Layer Location (nm)',fontsize=FS,fontname="Arial",labelpad=10)
ax.set_title('Perpendicual Magnetic Anistropy during VCMA',fontsize=FS,fontname="Arial")

#Plot for the Colorbar
ticks = np.linspace(magVal.min(), magVal.max(), 3, endpoint=True)
cb = fig.colorbar(im, shrink=1, location='right', ticks=ticks, format='%2.0f')
cb.ax.set_ylabel('Magnetic Anistropy (kJ/$m^3$)',fontsize=FS,fontname="Arial",labelpad=10)
cb.ax.tick_params(labelsize=FS)
cb.ax.set_yticklabels(["470", "485", "500"])

plt.tight_layout()
plt.show()
plt.savefig("heatmap.svg",bbox_inches="tight")