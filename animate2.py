#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:07:55 2021

@author: ccaprani

This module assumes that there is a disps.csv in the working directory which
is written by the analysedata.py script.

Alternative way to make the animation from static images saved to disk.

The native sample rate fs = 3125/18 = 173.6111...Hz; so fs/7 = ~24.80 frames 
per second, so only take every 7th to keep video fps reasonable, but real time.
"""

from draw_funcs import *

save_movie = False

time = df_disp["t"]
lim_margin = 0

fig = plt.figure(figsize=(8, 4.5))
fig.patch.set_facecolor("k")
axs = fig.add_subplot(projection="3d")
axs.set_box_aspect(
    [ub - lb for lb, ub in (getattr(axs, f"get_{a}lim")() for a in "xyz")]
)

decim = 7
tw = time[::decim]

for i, t in enumerate(tw):
    draw_frame(t, axs)
    plt.draw()
    plt.pause(1 / 24.8)
    if save_movie:
        plt.savefig(f"./images/img_{str(i).zfill(4)}.png", dpi=480)

if save_movie:
    # Now make the video, assuming ffmpeg is installed on system
    fps = (3125 / 18) / decim
    subprocess.call(
        [
            "ffmpeg",
            "-y",
            "-r",
            str(fps),
            "-i",
            "./images/img_%4d.png",
            "-vcodec",
            "libx264",
            "ted_motion3.mp4",
        ]
    )
