#!/usr/bin/env python3
"""
File:          Utilities.py
Author:        Mridul Bansal
Last Modified: Binit on 10/12
"""

import os
import numpy as np
import pybullet as p

class Utilities:
    """Utility class to convert between units of measure"""

    def gen_urdf_path(urdf_fname, cwd):
        return os.path.join(cwd, "data", urdf_fname)

    def add_debug_pose(position=np.array([0,0,0]),
                        orientation=np.array([0,0,0,1]),
                        x_color=np.array([1,0,0]),
                        y_color=np.array([0,1,0]),
                        z_color=np.array([0,0,1]),
                        lineLength=0.1,
                        lineWidth=1,
                        lifeTime=0,
                        parentObjectUniqueId=-1,
                        parentLinkIndex=-1,
                        replaceItemUniqueIds=(-1, -1, -1),
                        physicsClientId=0):
        '''Create a pose marker that identifies a position and orientation in space with 3 colored lines.
        '''
        pts = np.array([[0,0,0],[lineLength,0,0],[0,lineLength,0],[0,0,lineLength]])
        rotIdentity = np.array([0,0,0,1])
        po, _ = p.multiplyTransforms(position, orientation, pts[0,:], rotIdentity)
        px, _ = p.multiplyTransforms(position, orientation, pts[1,:], rotIdentity)
        py, _ = p.multiplyTransforms(position, orientation, pts[2,:], rotIdentity)
        pz, _ = p.multiplyTransforms(position, orientation, pts[3,:], rotIdentity)
        px_uid = p.addUserDebugLine(po, px, x_color, lineWidth, lifeTime, parentObjectUniqueId, parentLinkIndex, replaceItemUniqueIds[0])
        py_uid = p.addUserDebugLine(po, py, y_color, lineWidth, lifeTime, parentObjectUniqueId, parentLinkIndex, replaceItemUniqueIds[1])
        pz_uid = p.addUserDebugLine(po, pz, z_color, lineWidth, lifeTime, parentObjectUniqueId, parentLinkIndex, replaceItemUniqueIds[2])
        return (px_uid, py_uid, pz_uid)
