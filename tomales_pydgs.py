# Code by Lukas WinklerPrins
# lukas_wp@berkeley.edu
# Last modified Dec 2 2020

from dgs import *
import os, glob
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
plt.style.use('fivethirtyeight')

def run_tomales_gs():
    files = glob.glob('tomales/crops/*.jpeg')
    resolution = 1 # Doesn't seem to work if I make it 10/158
    maxscale = 3
    verbose = 1
    x = -1 # Gonna use this as a tuning parameter...

    actual_resolution = 10/158

    sieving_bins = [0.05, 0.063, 0.09, 0.125, 0.18, 0.25, 0.355, 0.5, 0.71, 1, 1.4, 2, 2.8, 4, 5.6, 8, 11.2, 16]
    # in mm 0.5 represents finer
    with open('test_sieves.csv') as csvfile:
        csvreader = csv.reader(csvfile,quoting=csv.QUOTE_NONNUMERIC)
        for row in csvreader:
            total = sum(row)
            # new_row = [i/total for i in row]
            # new_row = np.cumsum(new_row)
            new_row = np.cumsum(row)/total
            plt.plot(sieving_bins,new_row,'r',alpha=0.7)
            i = np.where(new_row > 0.5)

    for f in tqdm(files):
        filename = f + '_percentiles.csv'
        data_out = dgs(f, resolution, maxscale, verbose, x)

        with open(filename,'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data_out['percentile_values']*actual_resolution)
            csvwriter.writerow(data_out['percentiles'])

        filename = f + '_bins.csv'

        with open(filename,'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data_out['grain size bins']*actual_resolution)
            csvwriter.writerow(data_out['grain size frequencies'])

        # plt.plot(data_out['grain size bins']*actual_resolution,data_out['grain size frequencies'],'b',alpha=0.7)
        plt.plot(data_out['percentile_values']*actual_resolution,data_out['percentiles'],'b',alpha=0.7)

    plt.show()


if __name__ == '__main__':

   # all images in data folder, with plot
   run_tomales_gs()
