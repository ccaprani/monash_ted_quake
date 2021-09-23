#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Contains data from the Monash Unviersity Woodside Living Lab Building 
recording of the 22 Sept 2021 Mansfield 5.8M earthquake

Animation of the building motions
"""

# pip install npTDMS for reading the NI TDMS file type
from nptdms import TdmsFile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import integrate as it
from scipy import signal


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype="high", analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def filter_and_integrate(data, fc_ddx, fc_dx, fc_x):
    ddx = 9.81 * data
    ddxf = butter_highpass_filter(ddx, fc_ddx, fs)
    dx = it.cumtrapz(ddxf, dx=dt)
    dxf = butter_highpass_filter(dx, fc_dx, fs)
    x = it.cumtrapz(dxf, dx=dt)
    xf = butter_highpass_filter(x, fc_x, fs)
    return ddxf, dxf, xf


def plot_channel(df, idc):
    t = df["t"]
    c = df.iloc[:, idc]
    data = c.squeeze()
    ddxf, dxf, xf = filter_and_integrate(data, 1.0, 1.0, 2.0)

    fig, axs = plt.subplots(3, 1, sharex=True)

    axs[0].plot(t, ddxf, label=c.name)
    axs[0].set_ylabel("Acceleration (m/s$^2$)")

    axs[1].plot(t[:-1], dxf, label=c.name)
    axs[1].set_ylabel("Velocity (m/s)")

    axs[2].plot(t[:-2], xf, label=c.name)
    axs[2].set_ylabel("Displacement (m)")

    fig.legend()
    fig.tight_layout()


# Reading the NI TDMS file
tdms_file = TdmsFile.read("202109220920_SHM-6.tdms")
channels = tdms_file.groups()[0].channels()
c0 = channels[0]
fs = 1 / c0.properties["wf_increment"]
dt = 1 / fs

t0 = c0.properties["wf_start_time"]
ts = t0 + np.timedelta64(60, "s")
tf = t0 + np.timedelta64(3, "m")

t = c0.time_track(absolute_time=True)
idx = np.where((t > ts) & (t < tf))
tw = t[idx]

# Collect zeroed accels in dataframe
df_acc = pd.DataFrame()
df_acc["t"] = tw
for c in channels:
    zero_data = c[: (t < ts).sum()]
    data = c[idx] - zero_data.mean()
    df_acc[c.name] = data

# And plot a channel of interest
plot_channel(df_acc, 65)

# Collect displacements in a dataframe
df_disp = pd.DataFrame()
df_disp["t"] = tw[:-2]
for col in df_acc:
    if col != "t":
        data = df_acc[col]
        ddxf, dxf, xf = filter_and_integrate(data, 1.0, 1.0, 2.0)
        df_disp[col] = xf

df_disp.to_csv("disps.csv", index=False)
