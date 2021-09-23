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


def plot_quad(ax, iNode, jNode, kNode, lNode, col):
    surf = ax.plot_surface(
        np.array([[iNode[0], lNode[0]], [jNode[0], kNode[0]]]),
        np.array([[iNode[1], lNode[1]], [jNode[1], kNode[1]]]),
        np.array([[iNode[2], lNode[2]], [jNode[2], kNode[2]]]),
        color=col,
        alpha=0.3,
    )
    surfline = ax.plot(
        (iNode[0], jNode[0], kNode[0], lNode[0], iNode[0]),
        (iNode[1], jNode[1], kNode[1], lNode[1], iNode[1]),
        (iNode[2], jNode[2], kNode[2], lNode[2], iNode[2]),
        marker="",
        color=col,
        lw=0.5,
    )
    return surf, surfline


def update_quad(surf, surfline, iNode, jNode, kNode, lNode):
    surf.set_verts(np.array([iNode, jNode, kNode, lNode]))
    # Weird artefact on surfaces that can't be got rid of?
    # surf.do_3d_projection()  # https://bit.ly/3kwE93O
    # surf.draw(surf.axes.get_figure().canvas.get_renderer())
    surfline.set_data_3d(
        (iNode[0], jNode[0], kNode[0], lNode[0], iNode[0]),
        (iNode[1], jNode[1], kNode[1], lNode[1], iNode[1]),
        (iNode[2], jNode[2], kNode[2], lNode[2], iNode[2]),
    )
    return surf, surfline


def plot_column(ax, btmNode, topNode, col="w", lw=2):
    line = ax.plot(
        (btmNode[0], topNode[0]),
        (btmNode[1], topNode[1]),
        (btmNode[2], topNode[2]),
        color=col,
        lw=lw,
    )
    return line


def update_column(line, btmNode, topNode):
    line.set_data_3d(
        (btmNode[0], topNode[0]), (btmNode[1], topNode[1]), (btmNode[2], topNode[2]),
    )
    return line


def get_artists(surfs, surflines, lines, text):
    artists = np.concatenate(
        (
            np.array(surfs),
            np.array(surflines).squeeze(),
            np.array(lines).squeeze().flatten(),
            np.array([text]),
        )
    )
    return artists


def from_artists(artists):
    nsurf = len(zc) - 1
    surfs = artists[:nsurf]
    surflines = artists[nsurf : 2 * nsurf]
    lines = artists[2 * nsurf : -1].reshape(nsurf, 4)
    text = artists[-1]
    return surfs, surflines, lines, text


def channel_names(idx):
    return f"DYN1-{idx}X", f"DYN1-{idx}Y"


def disp_node(node, disp, factor):
    x, y, z = (*node,)
    xd = x + factor * disp[0]
    yd = y + factor * disp[1]
    return [xd, yd, z]


def init_frame(ax):
    surfs = []
    surflines = []
    lines = []

    ax.patch.set_facecolor("k")
    ax.patch.set_alpha(1.0)
    ax.set_axis_off()

    ax.axes.set_xlim3d(left=xc[0] - lim_margin, right=xc[1] + lim_margin)
    ax.axes.set_ylim3d(bottom=yc[0] - lim_margin, top=yc[1] + lim_margin)
    ax.axes.set_zlim3d(bottom=zc[0], top=zc[-1] + lim_margin)

    ax.text2D(
        0.5,
        1.0,
        "Monash University Living Lab\nM5.9 Mansfield Earthquake (22/9/21)\nMotion (x2000)",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color="white",
    )

    text = ax.text2D(
        0.5,
        0.02,
        "Monash Uni Living Lab",
        ha="center",
        va="center",
        transform=ax.transAxes,
        color="white",
    )

    iNodeBelow = [xc[0], yc[0], 0]
    jNodeBelow = [xc[0], yc[1], 0]
    kNodeBelow = [xc[1], yc[1], 0]
    lNodeBelow = [xc[1], yc[0], 0]

    for j, z in enumerate(zc[1:]):
        iNode = [xc[0], yc[0], z]
        jNode = [xc[0], yc[1], z]
        kNode = [xc[1], yc[1], z]
        lNode = [xc[1], yc[0], z]
        surf, surfline = plot_quad(ax, iNode, jNode, kNode, lNode, "r")
        surfs.append(surf)
        surflines.append(surfline)

        line = []
        line.append(plot_column(ax, iNodeBelow, [*iNode, z]))
        line.append(plot_column(ax, jNodeBelow, [*jNode, z]))
        line.append(plot_column(ax, kNodeBelow, [*kNode, z]))
        line.append(plot_column(ax, lNodeBelow, [*lNode, z]))
        lines.append(line)

        iNodeBelow = iNode
        jNodeBelow = jNode
        kNodeBelow = kNode
        lNodeBelow = lNode

    return get_artists(surfs, surflines, lines, text)


def draw_frame(t, artists):
    surfs, surflines, lines, text = from_artists(artists)

    str_time = np.datetime_as_string(np.datetime64(t), unit="ms")
    text.set_text(str_time)

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

        update_quad(surfs[j], surflines[j], iNodeD, jNodeD, kNodeD, lNodeD)

        update_column(lines[j][0], iNodeBelow, [*iNodeD, z])
        update_column(lines[j][1], jNodeBelow, [*jNodeD, z])
        update_column(lines[j][2], kNodeBelow, [*kNodeD, z])
        update_column(lines[j][3], lNodeBelow, [*lNodeD, z])

        iNodeBelow = iNodeD
        jNodeBelow = jNodeD
        kNodeBelow = kNodeD
        lNodeBelow = lNodeD

    return get_artists(surfs, surflines, lines, text)


time = df_disp["t"]
lim_margin = 0
fig = plt.figure(figsize=(8, 4.5))
fig.patch.set_facecolor("k")

axs = fig.add_subplot(projection="3d")
artists = init_frame(axs)

anim = animation.FuncAnimation(
    fig,
    draw_frame,
    frames=time,  # [4000:4346],
    interval=10,
    fargs=(artists,),
    blit=True,
    repeat=False,
    save_count=3460,
)

# fps = 173 is very close to sample rate, so basically real time
anim.save("ted_motion2.mp4", writer=animation.FFMpegWriter(fps=173), dpi=480)
# anim.save("ted_motion.gif", writer=animation.PillowWriter(fps=173))
