import matplotlib.pyplot as plt
from elastopy import draw
from elastopy import stress


def show():
    plt.show()


def model(model, name=None, color='k', dpi=100, ele=False, ele_label=False,
          surf_label=False, nodes_label=False, edges_label=False):
    """Plot the  model geometry

    """
    fig = plt.figure(name, dpi=dpi)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')
    ax.set_aspect('equal')

    draw.domain(model, ax, color=color)

    if ele is True:
        draw.elements(model, ax, color=color)

    if ele_label is True:
        draw.elements_label(model, ax)

    if surf_label is True:
        draw.surface_label(model, ax)

    if nodes_label is True:
        draw.nodes_label(model, ax)

    if edges_label is True:
        draw.edges_label(model, ax)

    return None


def model_deformed(model, U, magf=1, ele=False, name=None, color='Tomato',
                   dpi=100):
    """Plot deformed model

    """
    fig = plt.figure(name, dpi=dpi)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')
    ax.set_aspect('equal')

    if ele is True:
        draw.elements(model, ax, color='SteelBlue')
        draw.deformed_elements(model, U, ax, magf=magf, color=color)

    draw.domain(model, ax, color='SteelBlue')
    draw.deformed_domain(model, U, ax, magf=magf, color=color)


def stresses(model, SIG, ftr=1, s11=False, s12=False, s22=False, spmax=False,
             spmin=False, dpi=100, name=None, lev=20):
    """Plot stress with nodal stresses

    """
    fig = plt.figure(name, dpi=dpi, facecolor=None)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_aspect('equal')
    ax.set_xlabel(r'x')
    ax.set_ylabel(r'y')

    if s11 is True:
        ax.set_title(r'Stress 11 ('+str(ftr)+' Pa)')
        draw.tricontourf(model, SIG[:, 0]/ftr, ax, 'spring', lev=lev)

    if s12 is True:
        ax.set_title(r'Stress 12 ('+str(ftr)+' Pa)')
        draw.tricontourf(model, SIG[:, 2]/ftr, ax, 'cool', lev=lev)

    if s22 is True:
        ax.set_title(r'Stress 22 ('+str(ftr)+' Pa)')
        draw.tricontourf(model, SIG[:, 1]/ftr, ax, 'autumn', lev=lev)

    if spmax is True:
        spmx = stress.principal_max(SIG[:, 0], SIG[:, 1], SIG[:, 2])
        ax.set_title(r'Stress Principal Max ('+str(ftr)+' Pa)')
        draw.tricontourf(model, spmx/ftr, ax, 'plasma', lev=lev)

    if spmin is True:
        spmn = stress.principal_min(SIG[:, 0], SIG[:, 1], SIG[:, 2])
        ax.set_title(r'Stress Principal Min ('+str(ftr)+' Pa)')
        draw.tricontourf(model, spmn/ftr, ax, 'viridis', lev=lev)
