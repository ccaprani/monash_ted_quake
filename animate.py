#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 22:49:38 2021
@author: ccaprani

This module assumes that there is a disps.csv in the working directory which
is written by the analysedata.py script.

Using FuncAnimation is complex due to the need to return the artists after each 
frame, but it does not render otherwise. This script just returns the axes 
artist and redraws the entire axes each frame - quite inelegant.

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

anim = animation.FuncAnimation(
    fig,
    draw_frame,
    frames=tw,
    interval=10,
    fargs=(axs,),
    blit=True,
    repeat=False,
    save_count=3460,
)

if save_movie:
    # fps = 173 is very close to sample rate, so basically real time
    anim.save("ted_motion4.mp4", writer=animation.FFMpegWriter(fps=173), dpi=480)
    # anim.save("ted_motion.gif", writer=animation.PillowWriter(fps=173))
