#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 22:49:38 2021

@author: ccaprani
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

"""
This module assumes that there is a df_disp in memory from the analysedata script
"""

# Base coords
xc = [12, -12]
yc = [25, -25]
zc = [0, 5, 10, 16, 20, 25]

# Channel nos.
iNode_channels = np.linspace(5, 33, 5, dtype=int)
jNode_channels = np.linspace(4, 32, 5, dtype=int)
kNode_channels = np.linspace(2, 30, 5, dtype=int)
lNode_channels = np.linspace(3, 31, 5, dtype=int)

# Displacement amplification factor
factor = 2000


def plot_quad(ax, iNode, jNode, kNode, lNode, col):
    surf = ax.plot_surface(
        np.array([[iNode[0], lNode[0]], [jNode[0], kNode[0]]]),
        np.array([[iNode[1], lNode[1]], [jNode[1], kNode[1]]]),
        np.array([[iNode[2], lNode[2]], [jNode[2], kNode[2]]]),
        color=col,
        alpha=0.3,
    )
    ax.plot(
        (iNode[0], jNode[0], kNode[0], lNode[0], iNode[0]),
        (iNode[1], jNode[1], kNode[1], lNode[1], iNode[1]),
        (iNode[2], jNode[2], kNode[2], lNode[2], iNode[2]),
        marker="",
        color=col,
        lw=0.1,
    )
    return surf


def channel_names(idx):
    return f"DYN1-{idx}X", f"DYN1-{idx}Y"


def disp_node(node, disp, factor):
    x, y, z = (*node,)
    xd = x + factor * disp[0]
    yd = y + factor * disp[1]
    return [xd, yd, z]


def init_frame():

    for j, z in enumerate(zc[1:]):
        iNode = [xc[0], yc[0], z]
        jNode = [xc[0], yc[1], z]
        kNode = [xc[1], yc[1], z]
        lNode = [xc[1], yc[0], z]
        surf = plot_quad(ax, iNode, jNode, kNode, lNode, "g")

    return (ax,)


#%%
def draw_frame(t):
    ax.clear()
    ax.patch.set_facecolor("k")
    ax.patch.set_alpha(1.0)
    ax.set_axis_off()

    str_time = np.datetime_as_string(t.to_datetime64(), unit="ms")
    # ax.set_title(str_time, color="white")
    # fig.suptitle(str_time, color="white")
    ax.text2D(
        0.5,
        0.02,
        str_time,
        ha="center",
        va="center",
        transform=ax.transAxes,
        color="white",
    )

    ax.axes.set_xlim3d(left=xc[0] - lim_margin, right=xc[1] + lim_margin)
    ax.axes.set_ylim3d(bottom=yc[0] - lim_margin, top=yc[1] + lim_margin)
    ax.axes.set_zlim3d(bottom=zc[0], top=zc[-1] + lim_margin)

    i = df_disp.index[df_disp.t == t][0]

    iNodeBelow = [xc[0], yc[0], 0]
    jNodeBelow = [xc[0], yc[1], 0]
    kNodeBelow = [xc[1], yc[1], 0]
    lNodeBelow = [xc[1], yc[0], 0]

    for j, z in enumerate(zc[1:]):
        iNode = [xc[0], yc[0], z]
        jNode = [xc[0], yc[1], z]
        kNode = [xc[1], yc[1], z]
        lNode = [xc[1], yc[0], z]
        # plot_quad(ax, iNode, jNode, kNode, lNode, "g")

        cx, cy = channel_names(iNode_channels[j])
        disp = df_disp[[cx, cy]].loc[i]
        iNodeD = disp_node(iNode, disp, factor)

        cx, cy = channel_names(jNode_channels[j])
        disp = df_disp[[cx, cy]].loc[i]
        jNodeD = disp_node(jNode, disp, factor)

        cx, cy = channel_names(kNode_channels[j])
        disp = df_disp[[cx, cy]].loc[i]
        kNodeD = disp_node(kNode, disp, factor)

        cx, cy = channel_names(lNode_channels[j])
        disp = df_disp[[cx, cy]].loc[i]
        lNodeD = disp_node(lNode, disp, factor)

        plot_quad(ax, iNodeD, jNodeD, kNodeD, lNodeD, "r")

        col = "w"
        lw = 2
        ax.plot(
            (iNodeBelow[0], iNodeD[0]),
            (iNodeBelow[1], iNodeD[1]),
            (iNodeBelow[2], z),
            color=col,
            lw=lw,
        )
        ax.plot(
            (jNodeBelow[0], jNodeD[0]),
            (jNodeBelow[1], jNodeD[1]),
            (jNodeBelow[2], z),
            color=col,
            lw=lw,
        )
        ax.plot(
            (kNodeBelow[0], kNodeD[0]),
            (kNodeBelow[1], kNodeD[1]),
            (kNodeBelow[2], z),
            color=col,
            lw=lw,
        )
        ax.plot(
            (lNodeBelow[0], lNodeD[0]),
            (lNodeBelow[1], lNodeD[1]),
            (lNodeBelow[2], z),
            color=col,
            lw=lw,
        )

        iNodeBelow = iNodeD
        jNodeBelow = jNodeD
        kNodeBelow = kNodeD
        lNodeBelow = lNodeD

    return (ax,)


time = df_disp["t"]
lim_margin = 0
fig = plt.figure()
fig.patch.set_facecolor("k")

ax = fig.add_subplot(projection="3d")
ax.set_axis_off()

anim = animation.FuncAnimation(
    fig,
    draw_frame,
    frames=time[3500:45000],
    interval=0,
    blit=True,
    repeat=False,
    save_count=1000,
)
# anim.save("ted_motion.mp4", writer=animation.FFMpegWriter(fps=30))
# anim.save("ted_motion.gif", writer=animation.PillowWriter(fps=30))
