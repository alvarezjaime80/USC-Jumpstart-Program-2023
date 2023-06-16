import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from astropy import units as u
import sys


for i in range(len(sys.argv) - 1):
    file_name = sys.argv[1 + i]

    data = pd.read_csv(file_name)

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

    #converting time from second to weeks
    t_weeks = [((i*u.s).to(u.wk))/u.wk for i in data.t]

    #calling jumpstart style sheet
    plt.style.use('jumpstart')
    ax = plt.subplot()

    #plotting x vs time in Cardinal Red
    plt.scatter(t_weeks, x_pix, color='#990000')

    #plotting y vs time in Gold
    plt.scatter(t_weeks, y_pix, color='#FFC72C')

    #labeling x-axis as Time in units of Weeks
    plt.xlabel('Time [Weeks]')

    #labeling y-axis as difference from mean position in units of pixels
    plt.ylabel('Distance from Mean Position [$\mu$Pixels]')

    #setting ticks
    xticks = np.linspace(0, 13, 14, dtype='int')
    ax.set_xticks(xticks)

    #creating a legend for the plot
    plt.legend(['x-position','y-position'])

    #adding a title to the plot
    plt.title('Change in Position Over Time')

    plt.show()

    fig = plt.figure(figsize = (16, 12))
    ax = plt.subplot(1,4,(1,3))

    scatter_plot = ax.scatter(x_pix, y_pix,c = t_weeks, cmap = 'rainbow', s=range(1010,10,-1))

    plt.xlabel('x-position [$\mu$Pixels]')
    plt.ylabel('y-position [$\mu$Pixels]')
    plt.title('Y vs X Positions Over Time')
    cbar = plt.colorbar(scatter_plot, label = "Time [s]")
    cbar.set_label("Time [Weeks]", size=34, labelpad=20)
    cbar.ax.tick_params(labelsize=30)

    def update(frame):
        x = x_pix[:frame*20]
        y = y_pix[:frame*20]
        c = t_weeks[:frame*20]
        s = range(1010,10,-1)[:frame*20]
        frame_data = np.stack([x, y, c]).T
        scatter_plot.set_offsets(frame_data)
        return scatter_plot
        
    ani = animation.FuncAnimation(fig=fig, func=update, frames=50, interval=1, blit=False)

    plt.show()