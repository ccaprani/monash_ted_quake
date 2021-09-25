#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 12:30:42 2021

@author: ccaprani
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

"""
This module assumes that there is a disps.csv in the working directory which
is written by the analysedata.py script.
"""

df_disp = pd.read_csv("disps.csv")

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


def plot_quad(ax, iNode, jNode, kNode, lNode, col="r"):
    # Ordering of node coords to match what np.meshgrid would produce
    ax.plot_surface(
        np.array([[iNode[0], lNode[0]], [jNode[0], kNode[0]]]),
        np.array([[iNode[1], lNode[1]], [jNode[1], kNode[1]]]),
        np.array([[iNode[2], lNode[2]], [jNode[2], kNode[2]]]),
        color=col,
        alpha=0.3,
        edgecolor=col,
        lw=2,
    )


def plot_column(ax, btmNode, topNode, col="w", lw=2):
    ax.plot(
        (btmNode[0], topNode[0]),
        (btmNode[1], topNode[1]),
        (btmNode[2], topNode[2]),
        color=col,
        lw=lw,
    )


def channel_names(idx):
    return f"DYN1-{idx}X", f"DYN1-{idx}Y"


def disp_node(node, disp, factor):
    x, y, z = (*node,)
    xd = x + factor * disp[0]
    yd = y + factor * disp[1]
    return [xd, yd, z]


def draw_frame(t, ax):
    ax.clear()

    ax.patch.set_facecolor("k")
    ax.patch.set_alpha(1.0)
    ax.set_axis_off()

    ax.axes.set_xlim3d(left=xc[0] - lim_margin, right=xc[1] + lim_margin)
    ax.axes.set_ylim3d(bottom=yc[0] - lim_margin, top=yc[1] + lim_margin)
    ax.axes.set_zlim3d(bottom=zc[0], top=zc[-1] + lim_margin)

    ax.text2D(
        0.5,
        1.0,
        f"Monash University Living Lab\nM5.9 Mansfield Earthquake (22/9/21)\nMotion (x{factor})",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color="white",
    )

    str_time = np.datetime_as_string(np.datetime64(t), unit="ms")
    text = ax.text2D(
        0.5,
        0.05,
        str_time,
        ha="center",
        va="center",
        transform=ax.transAxes,
        color="white",
    )

    i = df_disp.index[df_disp.t == t][0]

    az = -(i / 20) % 360
    ax.view_init(elev=-20, azim=az)

    iNodeBelow = [xc[0], yc[0], 0]
    jNodeBelow = [xc[0], yc[1], 0]
    kNodeBelow = [xc[1], yc[1], 0]
    lNodeBelow = [xc[1], yc[0], 0]

    for j, z in enumerate(zc[1:]):
        iNode = [xc[0], yc[0], z]
        jNode = [xc[0], yc[1], z]
        kNode = [xc[1], yc[1], z]
        lNode = [xc[1], yc[0], z]
        # plot_quad(ax, iNode, jNode, kNode, lNode, "r")

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

        plot_quad(ax, iNodeD, jNodeD, kNodeD, lNodeD)

        plot_column(ax, iNodeBelow, [*iNodeD, z])
        plot_column(ax, jNodeBelow, [*jNodeD, z])
        plot_column(ax, kNodeBelow, [*kNodeD, z])
        plot_column(ax, lNodeBelow, [*lNodeD, z])

        iNodeBelow = iNodeD
        jNodeBelow = jNodeD
        kNodeBelow = kNodeD
        lNodeBelow = lNodeD

    return (ax,)


time = df_disp["t"]
lim_margin = 0

fig = plt.figure(figsize=(8, 4.5))
fig.patch.set_facecolor("k")
axs = fig.add_subplot(projection="3d")
axs.set_box_aspect(
    [ub - lb for lb, ub in (getattr(axs, f"get_{a}lim")() for a in "xyz")]
)
