#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Contains data from the Monash Unviersity Woodside Living Lab Building 
recording of the 22 Sept 2021 Mansfield 5.8M earthquake
"""

from nptdms import TdmsFile
import matplotlib.pyplot as plt


tdms_file = TdmsFile.read("202109220920_SHM-6.tdms")
group = tdms_file.groups()[0]
channels = group.channels()

fig, ax = plt.subplots()

plot_list = range(len(channels))
for c in plot_list:
    channel = channels[c]
    data = channel[:]
    t = channel.time_track(absolute_time=True)

    ax.plot(t, data, label=channel.name)

ax.legend()
plt.show()

# Sample rate and start time
t0 = channels[0].properties["wf_start_time"]
fs = 1 / channels[0].properties["wf_increment"]
print(f"Record start time {t0}")
print(f"Sample rate: {fs}")
