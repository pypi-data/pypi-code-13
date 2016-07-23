import numpy as np


def M_matrix(model, material, t=1):
    """Build the global stiffness matrix

    """
    M = np.zeros((model.ndof, model.ndof))
    for e, conn in enumerate(model.CONN):
        xyz = model.XYZ[conn]
        surf = model.surf_of_ele[e]
        dof = model.DOF[e]

        try:
            dnsty = material.dnsty[surf]
        except:
            print('Surface {} has no property assigned!'
                  'Default values were used!'.format(surf))
            dnsty = 1.0

        m = m_matrix(model, xyz, dnsty, t)

        id = np.ix_(dof, dof)

        M[id] += m

    return M


def m_matrix(model, xyz, dnsty, t=1):
    """Build the element mass matrix

    """
    gauss_points = model.chi / np.sqrt(3.0)

    m = np.zeros((8, 8))

    for gp in gauss_points:
        model.basis_function(gp)
        model.jacobian(xyz)
        dJ = model.detJac

        n = model.phi

        N = np.array([[n[0], 0., n[1], 0., n[2], 0., n[3], 0.],
                      [0., n[0], 0., n[1], 0., n[2], 0., n[3]]])

        m += (N.T @ N)*dnsty*dJ

    return m
