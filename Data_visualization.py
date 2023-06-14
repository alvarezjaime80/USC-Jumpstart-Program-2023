import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from astropy import units as u

data = pd.read_csv(r"C:\Users\jaime\OneDrive\Documents\Jumpstart Data\3112020.csv")

def get_pix(deg, pix_deg_conversion):
    """function takes a value in degrees and returns converted value in pixels
    parameter: deg - int, initial value in degrees
    parameter: pix_deg_conversion - int, conversion ratio between pixels and degrees
    returns: int, converted value in pixels
    """
    pix = deg.to(u.deg)*(pix_deg_conversion*(1/u.deg))
    return pix.to('')

#finding mean value for right acension
degree_ra_mean = data.kic_degree_ra.mean()

#finding mean value for declenation
degree_dec_mean = data.kic_deg.mean()

#setting x to the difference of the right ascension values from the mean
x = [degree_ra_mean - i for i in data.kic_degree_ra]

#converting x values from degrees to pixels
x_pix = [get_pix(i*u.deg, (60**2)/4)*10**6 for i in x]

#setting y to the difference of the declenation values from the mean
y = [degree_dec_mean - i for i in data.kic_deg]

#converting y values from degrees to pixels
y_pix = [get_pix(i*u.deg, (60**2)/4)*10**6 for i in y]

#converting time from second to years
t_weeks = [((i*u.s).to(u.wk))/u.wk for i in data.t]

#creating figure of size 12x12 inches
plt.figure(figsize = (12,12))
ax = plt.subplot()

#plotting x vs time in green
plt.scatter(t_weeks, x_pix, color='#990000')

#plotting y vs time in navy
plt.scatter(t_weeks, y_pix, color='#FFC72C')

#labeling x-axis as Time in units of seconds
plt.xlabel('Time [Weeks]', fontsize=18, labelpad=10)

#labeling y-axis as difference from mean position in units of pixels
plt.ylabel('Distance from Mean Position [$\mu$Pixels]', fontsize=18)

#setting ticks
xticks = np.linspace(0, 13, 14, dtype='int')
ax.set_xticks(xticks)

#rotating x-tick labels for visibility
ax.xaxis.set_tick_params(rotation=0)

#using exact x and y values as ticks
ax.ticklabel_format(useMathText=True)

#making xtick labels larger
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

#creating a legend for the plot
plt.legend(['x-position','y-position'], fontsize=22, shadow = True)

#adding a title to the plot
plt.title('Change in Position Over Time', fontsize=30, pad=10)
plt.show()

fig = plt.figure(figsize = (18,12))
ax = plt.subplot(1,4,(1,3))

scatter_plot = ax.scatter(x_pix, y_pix,c = t_weeks, cmap = 'rainbow', s=range(1010,10,-1))

plt.xlabel('x-position [$\mu$Pixels]', fontsize=22, labelpad=15)
plt.ylabel('y-position [$\mu$Pixels]', fontsize=22)
plt.title('Y vs X Positions Over Time', fontsize=30)
cbar = plt.colorbar(scatter_plot, label = "Time [s]")
cbar.set_label("Time [Weeks]", size=20, labelpad=20)
cbar.ax.tick_params(labelsize=18)
ax.ticklabel_format(useMathText=True)
#making tick labels larger
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

def update(frame):
    x = x_pix[:frame]
    y = y_pix[:frame]
    c = t_weeks[:frame]
    s = range(1010,10,-1)[:frame]
    frame_data = np.stack([x, y, c]).T
    scatter_plot.set_offsets(frame_data)
    return scatter_plot
    
ani = animation.FuncAnimation(fig=fig, func=update, frames=1000, interval=10, blit=False)

plt.show()