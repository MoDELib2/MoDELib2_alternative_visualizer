import os
import sys
import string
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from pathlib import Path
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D

#plt.rcParams['text.usetex'] = True
sys.path.append("../../python")
from modlibUtils import *
sys.path.append("../../build/tools/pyMoDELib")
import pyMoDELib


def rotate_points_plane_to_xy(point, normal, inplane_ref=None):
    P = np.asarray(point, dtype=float);
    n = np.asarray(normal, dtype=float); 
    u = np.asarray(inplane_ref, float)
    u /= np.linalg.norm(inplane_ref); 
    v = np.cross(n, u)

    # rotation matrix of a plane formed by normal and inplane_ref vectors
    R = np.vstack([u, v, n])         # global -> plane frame
    # take inverse rotation
    P_rot = (R @ (P.T).T)
    return P_rot


def main():
    # ------------- Create data objects ------------- #
    base_path = Path("./example_data/dipole/evl")
    ddio = pyMoDELib.DDconfigIO(str(base_path))
    run_ID = 2500
    ddio.readTxt(run_ID)
    nodes = ddio.nodes
    loops = ddio.loops
    loopNodes=ddio.loopNodes
    loopLinks=ddio.loopLinks
    segments = ddio.segments()

    NetNode_pos = {n.sID: np.array(n.P) for n in nodes}

    n = len(loops)
    cols = 2
    rows = (n + cols - 1) // cols 
    fig = plt.figure(figsize=(12, rows * 4))
    fig2 = plt.figure(figsize=(12, rows * 4))

    for i in range(len(loops)):
        loop_b = loops[i].B
        loop_n = loops[i].N
        loop_p = loops[i].P
        ax = fig.add_subplot(rows, cols, i+1, projection="3d")
        ax2 = fig2.add_subplot(rows, cols, i+1)

        print(loop_b, loop_n, loop_p)
        print("Plane Noraml",loop_n)
        hasReferenceVector = False

        for segKey, seg in segments.items(): # loop over segments
            b = np.array(seg.b)

            if np.linalg.norm(b) > 0:
                sid1 = seg.sourceID
                sid2 = seg.sinkID
                p1 = NetNode_pos.get(sid1)
                p2 = NetNode_pos.get(sid2)

                tol = 1e-4
                if ( np.linalg.norm( np.abs(seg.b) - np.abs(loop_b)) < tol) and ( np.linalg.norm(seg.n - loop_n) < tol):

                    p1_vec = loop_p - p1
                    p2_vec = loop_p - p2

                    p1_norm = p1_vec/np.linalg.norm(p1_vec)
                    p2_norm = p2_vec/np.linalg.norm(p2_vec)

                    loop_norm = loop_n/np.linalg.norm(loop_n)

                    angle1 = np.degrees( np.arccos( np.dot(p1_norm, loop_norm) ) )
                    angle2 = np.degrees( np.arccos( np.dot(p2_norm, loop_norm) ) )

                    if hasReferenceVector==False:
                        ref_vector = p1_vec
                        hasReferenceVector = True

                    if (np.round(angle1)==90) or (np.round(angle2)==90):

                        p1_rot = rotate_points_plane_to_xy(p1, loop_n, ref_vector)
                        p2_rot = rotate_points_plane_to_xy(p2, loop_n, ref_vector)

                        print("Position 1", p1,"Position 2", p2)
                        print("Rotated Position 1", p1_rot,"Rotated Position 2", p2_rot)

                        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], linewidth=2)
                        ax2.plot([p1_rot[0], p2_rot[0]], [p1_rot[1], p2_rot[1]], linewidth=2)

                        # ax2.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], linewidth=2)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
