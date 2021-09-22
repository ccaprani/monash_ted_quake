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

df = pd.DataFrame()
df["t"] = tw

for c in channels:
    zero_data = c[: (t < ts).sum()]
    data = c[idx] - zero_data.mean()
    df[c.name] = data


# examine one channel
idc = [65]
name = df.columns[idc]

ddx = 9.81 * df.iloc[:, idc].squeeze()
ddxf = butter_highpass_filter(ddx, 1.0, fs)

dx = it.cumtrapz(ddxf, dx=dt)
dxf = butter_highpass_filter(dx, 1.0, fs)

x = it.cumtrapz(dxf, dx=dt)
xf = butter_highpass_filter(x, 2.0, fs)

# And plot
fig, axs = plt.subplots(3, 1, sharex=True)

axs[0].plot(tw, ddxf, label=name)
axs[0].set_ylabel("Acceleration (m/s$^2$)")

axs[1].plot(tw[:-1], dxf, label=name)
axs[1].set_ylabel("Velocity (m/s)")

axs[2].plot(tw[:-2], xf, label=name)
axs[2].set_ylabel("Displacement (m)")

fig.legend()
fig.tight_layout()
