import numpy as np


def Pt_vector(model, trac, t=1):
    """Build the load vector for the internal heat source

    """
    Pt = np.zeros(model.ndof)

    for l in trac(1, 1).keys():
        # find which boundary element is in this line l
        bound_ele = model.bound_ele[np.where(model.bound_ele[:, 2] == l[1])[0]]

        for e, side, line in bound_ele:
            if l[0] == 'line':
                conn = model.CONN[e, :]
                xyz = model.XYZ[conn]
                dof = model.DOF[e]

                pt = pt_vector(model, xyz, trac, side, l, t)

                id = dof

                Pt[id] += pt
    return Pt


def pt_vector(model, xyz, trac, side, l, t=1):
    """Build the element vector for the internal heat source

    """
    gp = np.array([[[-1.0 / np.sqrt(3), -1.0],
                  [1.0 / np.sqrt(3), -1.0]],
                 [[1.0, -1.0 / np.sqrt(3)],
                  [1.0, 1.0 / np.sqrt(3)]],
                 [[-1.0 / np.sqrt(3), 1.0],
                  [1.0 / np.sqrt(3), 1.0]],
                 [[-1.0, -1.0 / np.sqrt(3)],
                  [-1.0, 1.0 / np.sqrt(3)]]])

    pt = np.zeros(8)

    for w in range(2):
        model.basis_function(gp[side, w])
        model.jacobian(xyz)
        dL = model.ArchLength[side]

        x1, x2 = model.mapping(xyz)

        pt[0] += model.phi[0]*trac(x1, x2, t)[l][0]*dL
        pt[1] += model.phi[0]*trac(x1, x2, t)[l][1]*dL
        pt[2] += model.phi[1]*trac(x1, x2, t)[l][0]*dL
        pt[3] += model.phi[1]*trac(x1, x2, t)[l][1]*dL
        pt[4] += model.phi[2]*trac(x1, x2, t)[l][0]*dL
        pt[5] += model.phi[2]*trac(x1, x2, t)[l][1]*dL
        pt[6] += model.phi[3]*trac(x1, x2, t)[l][0]*dL
        pt[7] += model.phi[3]*trac(x1, x2, t)[l][1]*dL

    return pt
