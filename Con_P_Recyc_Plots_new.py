# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:24:45 2016

@author: Ent00002
"""
#%% Import libraries

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
from getconstants import getconstants
from matplotlib.colors import LinearSegmentedColormap
import os

#%% BEGIN OF INPUT (FILL THIS IN)
years = np.arange(2009,2010) #fill in the years

# Manage the extent of your dataset (FILL THIS IN)
# Define the latitude and longitude cell numbers to consider and corresponding lakes that should be considered part of the land
latnrs = np.arange(0,121)
lonnrs = np.arange(0,240)

# the lake numbers below belong to the ERA-Interim data on 1.5 degree starting at Northern latitude 79.5 and longitude -180
lake_mask_1 = np.array([9,9,9,12,12,21,21,22,22,23,24,25,23,23,25,25,53,54,61,23,24,23,24,25,27,22,23,24,25,26,27,28,22,25,26,27,28,23,23,12,18])
lake_mask_2 = np.array([120+19,120+40,120+41,120+43,120+44,120+61,120+62,120+62,120+63,120+62,120+62,120+62,120+65,120+66,120+65,120+66,142-120,142-120,143-120,152-120,152-120,153-120,153-120,153-120,153-120,154-120,154-120,154-120,154-120,154-120,154-120,154-120,155-120,155-120,155-120,155-120,155-120,159-120,160-120,144-120,120+55])
lake_mask = np.transpose(np.vstack((lake_mask_1,lake_mask_2))) #recreate the arrays of the matlab model

# obtain the constants
#invariant_data = r'C:\Users\bec\Desktop\WAM2/invariants_15x15.nc'#invariants
invariant_data = r'E:/WAM2layersPython/ERA-Interim/DATA/Land-sea_mask.nc' #invariants
latitude,longitude,lsm,g,density_water,timestep,A_gridcell,L_N_gridcell,L_S_gridcell,L_EW_gridcell,gridcell = getconstants(latnrs,lonnrs,lake_mask,invariant_data)
A_gridcell2D = np.tile(A_gridcell,len(longitude));

# BEGIN OF INPUT 2 (FILL THIS IN)
timetracking = 1 # 0 for not tracking time and 1 for tracking time
Region = lsm

#output_folder = r'C:\Users\bec\Desktop\WAM2\output'
output_folder = r'E:\WAM2layersPython\ERA-Interim\DATA\output'  # 这里要用\ 表示back slash
# END OF INPUT

#%% Datapaths (FILL THIS IN)

def data_path(years,timetracking):
    load_data_pypm = os.path.join(output_folder, 'P_track_continental_full' + str(years[0]) + '-' + str(years[-1]) + '-timetracking' + str(timetracking) + '.mat')
    load_data_hf = os.path.join(output_folder, 'Hor_Fluxes_full' + str(years[0]) + '-' + str(years[-1]) + '.mat')
    return load_data_pypm,load_data_hf

#%% Calculations

# loading vertical fluxes and storages
datapath = data_path(years,timetracking)
loading_PT2SC = sio.loadmat(datapath[0])
E_per_year_per_month = loading_PT2SC['E_per_year_per_month']
P_track_per_year_per_month = loading_PT2SC['P_track_per_year_per_month']
P_per_year_per_month = loading_PT2SC['P_per_year_per_month']
Sa_track_down_per_year_per_month = loading_PT2SC['Sa_track_down_per_year_per_month']
Sa_track_top_per_year_per_month = loading_PT2SC['Sa_track_top_per_year_per_month']
Sa_time_down_per_year_per_month = loading_PT2SC['Sa_time_down_per_year_per_month']
Sa_time_top_per_year_per_month = loading_PT2SC['Sa_time_top_per_year_per_month']
P_time_per_year_per_month = loading_PT2SC['P_time_per_year_per_month']
W_down_per_year_per_month = loading_PT2SC['W_down_per_year_per_month']
W_top_per_year_per_month = loading_PT2SC['W_top_per_year_per_month']
north_loss_per_year_per_month = loading_PT2SC['north_loss_per_year_per_month']
south_loss_per_year_per_month = loading_PT2SC['south_loss_per_year_per_month']
down_to_top_per_year_per_month = loading_PT2SC['down_to_top_per_year_per_month']
top_to_down_per_year_per_month = loading_PT2SC['top_to_down_per_year_per_month']
water_lost_per_year_per_month = loading_PT2SC['water_lost_per_year_per_month']

E_total = np.squeeze(np.sum(np.sum(E_per_year_per_month,axis = 0), axis = 0))
P_c_total = np.squeeze(np.sum(np.sum(P_track_per_year_per_month,axis = 0), axis = 0))
P_total = np.squeeze(np.sum(np.sum(P_per_year_per_month,axis = 0), axis = 0))

# loading horizontal fluxes
loading_HF2S = sio.loadmat(datapath[1])
Fa_E_down_per_year_per_month = loading_HF2S['Fa_E_down_per_year_per_month']
Fa_E_top_per_year_per_month = loading_HF2S['Fa_E_top_per_year_per_month']
Fa_N_down_per_year_per_month = loading_HF2S['Fa_N_down_per_year_per_month']
Fa_N_top_per_year_per_month = loading_HF2S['Fa_N_top_per_year_per_month'] 
Fa_Vert_per_year_per_month = loading_HF2S['Fa_Vert_per_year_per_month']

Fa_E_down_total = np.squeeze(np.sum(np.sum(Fa_E_down_per_year_per_month,axis = 0),axis = 0))
Fa_E_top_total = np.squeeze(np.sum(np.sum(Fa_E_top_per_year_per_month,axis = 0),axis = 0))
Fa_N_down_total = np.squeeze(np.sum(np.sum(Fa_N_down_per_year_per_month,axis = 0),axis = 0))
Fa_N_top_total = np.squeeze(np.sum(np.sum(Fa_N_top_per_year_per_month,axis = 0),axis = 0))
Fa_E_total = Fa_E_down_total + Fa_E_top_total
Fa_N_total = Fa_N_down_total + Fa_N_top_total

# annual average fluxes per unit width (m3/m/a)
Fa_N_total_m2a = np.zeros(np.shape(Fa_N_total))
Fa_N_down_total_m2a = np.zeros(np.shape(Fa_N_down_total))
Fa_N_top_total_m2a = np.zeros(np.shape(Fa_N_top_total))

for i in range(len(latitude)):
    Fa_N_total_m2a[i,:] = (Fa_N_total[i,:] / (0.5*(L_N_gridcell[i] + L_S_gridcell[i])))/len(years)
    Fa_N_down_total_m2a[i,:] = (Fa_N_down_total[i,:] / (0.5*(L_N_gridcell[i] + L_S_gridcell[i])))/len(years)
    Fa_N_top_total_m2a[i,:] = (Fa_N_top_total[i,:] / (0.5*(L_N_gridcell[i] + L_S_gridcell[i])))/len(years)

Fa_E_total_m2a = (Fa_E_total / L_EW_gridcell) / len(years) # Annual average flux per unit width (m3/m/a)
Fa_E_down_total_m2a = (Fa_E_down_total / L_EW_gridcell) / len(years) # Annual average flux per unit width (m3/m/a)
Fa_E_top_total_m2a = (Fa_E_top_total / L_EW_gridcell) / len(years) # Annual average flux per unit width (m3/m/a)

# fluxes for plotting
FluxDispMatSmall = np.zeros([5,5])
FluxDispMatSmall[3,2] = 1
FluxDispMat = np.tile(FluxDispMatSmall,[int(np.floor(len(latitude)/5+1)),int(np.floor(len(longitude)/5)+1)])
FluxDispMat = FluxDispMat[:len(latitude),:len(longitude)]

Fa_E_total_m2a_part = Fa_E_total_m2a * FluxDispMat
Fa_N_total_m2a_part = Fa_N_total_m2a * FluxDispMat
Fa_E_down_total_m2a_part = Fa_E_down_total_m2a * FluxDispMat
Fa_N_down_total_m2a_part = Fa_N_down_total_m2a * FluxDispMat
Fa_E_top_total_m2a_part = Fa_E_top_total_m2a * FluxDispMat
Fa_N_top_total_m2a_part = Fa_N_top_total_m2a * FluxDispMat

# recycling metrics
rho_c_total = P_c_total / P_total

#only on land
E_landtotal = np.array(E_total)
E_landtotal[Region == 0] = 0
P_landtotal = np.array(P_total)
P_landtotal[Region == 0] = 0
P_c_landtotal = np.array(P_c_total)
P_c_landtotal[Region == 0] = 0
rho_c_landtotal = np.array(rho_c_total)
rho_c_landtotal[Region == 0] = -0.1
rho_c_abslandtotal = np.sum(np.sum(P_c_landtotal, axis = 0))/np.sum(np.sum(P_landtotal, axis = 0))

#what happens
Test_P_c = np.sum(P_c_total)
Test_E_land = np.sum(E_landtotal)
Mean_down_to_top = np.squeeze(np.sum(np.sum(down_to_top_per_year_per_month, axis = 0), axis = 0))
Test_down_to_top = np.sum(Mean_down_to_top)
Mean_top_to_down = np.squeeze(np.sum(np.sum(top_to_down_per_year_per_month, axis = 0), axis = 0))
Test_top_to_down = np.sum(Mean_top_to_down)
Mean_water_lost = np.squeeze(np.sum(np.sum(water_lost_per_year_per_month, axis = 0), axis = 0))
Test_water_lost = np.sum(Mean_water_lost)
Test_north_loss = np.sum(north_loss_per_year_per_month)
Test_south_loss = np.sum(south_loss_per_year_per_month)
Isthis100procent = (Test_P_c + Test_water_lost + Test_north_loss + Test_south_loss) / Test_E_land
print (Isthis100procent*100)

#just to know
water_lost_vertically = (Test_water_lost)/np.sum(E_landtotal) 
water_lost_north = (Test_north_loss)/np.sum(E_landtotal) 
water_lost_south = (Test_south_loss)/np.sum(E_landtotal) 
print(water_lost_vertically*100, water_lost_north*100, water_lost_south*100)


#%% Plotting constants
#get_ipython().magic(u'matplotlib qt')
#from mpl_toolkits.basemap import Basemap

import cartopy.crs as ccrs
import cartopy.feature as cf
import geocat.viz.util as gvutil
#from geocat.viz import cmaps as gvcmaps

cdict = {'red': ((0., 1, 1),
                 (0.05, 1, 1),
                 (0.11, 0, 0),
                 (0.66, 1, 1),
                 (0.89, 1, 1),
                 (1, 0.5, 0.5),
                 (1, 0, 0)),
         'green': ((0., 1, 1),
                   (0.05, 1, 1),
                   (0.11, 0, 0),
                   (0.375, 1, 1),
                   (0.64, 1, 1),
                   (0.91, 0, 0),
                   (1, 0, 0)),
         'blue': ((0., 1, 1),
                  (0.05, 1, 1),
                  (0.11, 1, 1),
                  (0.34, 1, 1),
                  (0.65, 0, 0),
                  (1, 0, 0))}

my_cmap = LinearSegmentedColormap('my_colormap',cdict,256)
vmax = 1.0
cmap = LinearSegmentedColormap.from_list('mycmap', [(0 / vmax, 'white'),
                                                    (0.01 / vmax, 'blue'),
                                                    (0.3 / vmax, 'lightgreen'),
                                                    (0.5 / vmax, 'orange'),
                                                    (0.6 / vmax, 'red'),
                                                    (1.0 / vmax, 'black')])

#%% Plots
#plt.close('all')
####################### CONTOUR PLOT

fig=plt.figure(figsize=(10,8)) # nice projections are 'cea', 'cyl', 'eck4' and 'robin', however only 'cea' and 'cyl' allows for not showing the entire world
#map = Basemap(projection='cyl',lat_0=0,lon_0=0,
#              llcrnrlon=-180, llcrnrlat=-78,
#              urcrnrlon=180, urcrnrlat=78)
#map.drawcoastlines(linewidth=0.25)
#map.drawcountries(linewidth=0.25)
#map.drawmeridians(np.arange(0,360,30),linewidth=0.1)
#map.drawparallels(np.arange(-90,90,30),linewidth=0.1)

ax = plt.axes(projection=ccrs.PlateCarree())
#ax.coastlines(linewidth=0.5, alpha=0.6)
ax.add_feature(cf.COASTLINE)
ax.add_feature(cf.BORDERS)

#gvutil.add_major_minor_ticks(ax)
gvutil.add_lat_lon_ticklabels(ax)

#gvutil.set_axes_limits_and_ticks(ax,
#                                 xlim=(-180, 180),
#                                 ylim=(-90, 90),
#                                 xticks=np.linspace(-180, 180, 13),
#                                 yticks=np.linspace(-90, 90, 7))
#
#ax.set_extent([-180,180,90,0],ccrs.PlateCarree())
###################################

x_shift,y_shift = np.meshgrid(longitude,latitude)
x = x_shift 
y = y_shift 

# contour data over the map
Fa_E_total_m2a_part[Fa_E_total_m2a_part==0] = np.nan
Fa_N_total_m2a_part[Fa_N_total_m2a_part==0] = np.nan
clevs = np.linspace(0,1.00,11)
clevs2 = np.linspace(0,1,1100)
#cs = map.contourf(x,y,rho_c_landtotal,clevs2,linewidths=1.5,latlon=True, cmap=cmap)

col = ax.contourf(x, y, rho_c_landtotal, transform=ccrs.PlateCarree(), levels=clevs2, cmap=cmap)
#plt.colorbar(col)

plt.colorbar(col,location='right',ticks = clevs)

windplot = ax.quiver(x,y,Fa_E_total_m2a_part,Fa_N_total_m2a_part,color = 'black',scale = 199999999,width = 0.002, headaxislength = 5, headwidth = 2)
#adjust scale till arrows are visible

plt.title('Continental precipitation recycling ratio ' r'$\rho_c$', fontsize = 14)
plt.show()
