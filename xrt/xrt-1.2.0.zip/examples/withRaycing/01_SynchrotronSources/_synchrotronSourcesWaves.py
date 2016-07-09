# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "08 Mar 2016"

#import matplotlib
#matplotlib.use('agg')

import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import time
import pickle
import numpy as np

import xrt.backends.raycing as raycing
import xrt.backends.raycing.sources as rs
import xrt.backends.raycing.screens as rsc
import xrt.backends.raycing.run as rr
import xrt.plotter as xrtp
import xrt.runner as xrtr

pprefix = ''

# one of 'u', 'cu':
sourceType = 'eu'
suffix = ''
R0 = 25000.
xPrimeMax = 0.2
zPrimeMax = 0.2
bins = 512
ppb = 1

Source = rs.Undulator
kwargs = dict(
    period=30., n=40, eE=3., eI=0.5,
    betaX=9., betaZ=2.,
    eEpsilonX=0.263, eEpsilonZ=0.008,
    xPrimeMaxAutoReduce=False,
    zPrimeMaxAutoReduce=False)
if (sourceType == 'u') or (sourceType == 'cu'):  # cu = custom field undulator
    kwargs['K'] = 1.45
    if sourceType == 'cu':  # cu = custom field undulator
#        Blong = 10.  # +15 T of longitudinal field
#        kwargs['customField'] = Blong
#        suffix += '-{0:.0f}T'.format(Blong)
#        kwargs['eEpsilonX'] = (0.263*0.008)**0.5
#        kwargs['eEpsilonZ'] = (0.263*0.008)**0.5

        sheet = 'EPU_HP_mode'
#        sheet = 'QEPU_HP_mode'
#        sheet = 'EPU_VP_mode'
#        sheet = 'QEPU_VP_mode'
        kwargs['customField'] = ['B-Hamed.xlsx',
                                 dict(sheetname=sheet, skiprows=0)]
elif sourceType == 'eu':
    kwargs['Ky'] = 1.45
    kwargs['Kx'] = 1.45
    kwargs['phaseDeg'] = 90
#    kwargs['targetE'] = 920., 1, True
else:
    raise ValueError('Unknown source type!')

if True:  # zero source size:
#    kwargs['eSigmaX'] = 1e-3
#    kwargs['eSigmaZ'] = 1e-3
    kwargs['eEpsilonX'] = 0
    kwargs['eEpsilonZ'] = 0
    eEpsilonC = '0'
else:
    eEpsilonC = 'n'

eUnit = 'eV'
#prefix, eMinRays, eMaxRays, repeats = pprefix+'0-{0}-wide-'.format(eEpsilonC),\
#    100, 1000, 1
#prefix, eMinRays, eMaxRays, repeats = pprefix+'1-{0}-oneH-'.format(eEpsilonC),\
#    6600, 7200, 1
#prefix, eMinRays, eMaxRays, repeats = pprefix+'2-{0}-mono-'.format(eEpsilonC),\
#    6600, 7200, 1
prefix, eMinRays, eMaxRays, repeats = pprefix+'2-{0}-mono-'.format(eEpsilonC),\
    920*2-20, 920*2+20, 1
#prefix, eMinRays, eMaxRays, repeats = pprefix+'2-{0}-mono-'.format(eEpsilonC),\
#    460-20, 460+20, 1
kwargs['eMin'] = eMinRays
kwargs['eMax'] = eMaxRays

if 'mono' in prefix:
#    fixedEnergy = 6920.
    fixedEnergy = 920.*2
    prefix += '-E={0:.0f}eV'.format(fixedEnergy)
    filamentBeam = True
else:
    fixedEnergy = False
    filamentBeam = False

if sourceType == 'eu':
    xPrimeMax *= 4
    zPrimeMax *= 4
else:
    xPrimeMax /= 5.
    zPrimeMax /= 5.
    
kwargs['filamentBeam'] = filamentBeam
kwargs['xPrimeMax'] = xPrimeMax
kwargs['zPrimeMax'] = zPrimeMax
xlimits = [-xPrimeMax*R0*1e-3, xPrimeMax*R0*1e-3]
zlimits = [-zPrimeMax*R0*1e-3, zPrimeMax*R0*1e-3]
xlimits = [0.8, 1.1]
zlimits = [0.8, 1.1]


def build_beamline(nrays=1e5):
    beamLine = raycing.BeamLine()
    beamLine.source = Source(beamLine, nrays=nrays, **kwargs)
    beamLine.fsm1 = rsc.Screen(beamLine, 'FSM1', (0, R0, 0))
    return beamLine


def run_process(beamLine):
    startTime = time.time()
    if 'mono' in prefix:
#    if True:
        x = beamLine.fsmExpX
        z = beamLine.fsmExpZ
        waveOnScreen = beamLine.fsm1.prepare_wave(beamLine.source, x, z)
        beamSource = beamLine.source.shine(wave=waveOnScreen,
                                           fixedEnergy=fixedEnergy)
        dx = np.gradient(x)
        dz = np.gradient(z)
        field = beamSource.Es.reshape((len(dz), len(dx)))
        dFdz, dFdx = np.gradient(field)
        ly = dFdx/dx*z[:, None] - dFdz/dz[:, None]*x
        avem = np.real(1j*field.conjugate()*ly).sum()
        norm = np.abs(field*field.conjugate()).sum()
        print('avems = {0}'.format(avem/norm))
        field = beamSource.Ep.reshape((len(dz), len(dx)))
        dFdz, dFdx = np.gradient(field)
        ly = dFdx/dx*z[:, None] - dFdz/dz[:, None]*x
        avem = np.real(1j*field.conjugate()*ly).sum()
        norm = np.abs(field*field.conjugate()).sum()
        print('avemp = {0}'.format(avem/norm))
    else:
        beamSource = beamLine.sources[0].shine()
    print('shine time = {0}s'.format(time.time() - startTime))
    beamFSM1 = beamLine.fsm1.expose(beamSource)
    outDict = {'beamSource': beamSource,
               'beamFSM1': beamFSM1}
    return outDict

rr.run_process = run_process


def define_plots(beamLine):
    plots = []
    plotsE = []

    xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
    yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
    caxis = xrtp.XYCAxis('energy', eUnit, fwhmFormatStr=None,
                         bins=bins, ppb=ppb)
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
        aspect='auto', title='total flux')
    plot.caxis.fwhmFormatStr = None
    plot.saveName = prefix + '1TotalFlux' + suffix + '.png'
    plots.append(plot)
    plotsE.append(plot)

    xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
    yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
    caxis = xrtp.XYCAxis('energy', eUnit, fwhmFormatStr=None,
                         bins=bins, ppb=ppb)
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
        fluxKind='s', aspect='auto', title='horizontal polarization flux')
    plot.caxis.fwhmFormatStr = None
    plot.saveName = prefix + '2horizFlux' + suffix + '.png'
    plots.append(plot)
    plotsE.append(plot)

    xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
    yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
    caxis = xrtp.XYCAxis('energy', eUnit, fwhmFormatStr=None,
                         bins=bins, ppb=ppb)
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
        fluxKind='p', aspect='auto', title='vertical polarization flux')
    plot.caxis.fwhmFormatStr = None
    plot.saveName = prefix + '3vertFlux' + suffix + '.png'
    plots.append(plot)
    plotsE.append(plot)

    xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
    yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
    caxis = xrtp.XYCAxis('degree of polarization', '',
                         data=raycing.get_polarization_degree,
                         limits=[0.95, 1.0005], bins=bins, ppb=ppb)
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
        aspect='auto', title='degree of polarization')
    plot.saveName = prefix + '4DegPol' + suffix + '.png'
    plot.caxis.fwhmFormatStr = None
    plots.append(plot)

    xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
    yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
    caxis = xrtp.XYCAxis('circular polarization rate', '',
                         data=raycing.get_circular_polarization_rate,
                         limits=[-1, 1], bins=bins, ppb=ppb)
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
        aspect='auto', title='circular polarization rate')
    plot.saveName = prefix + '5CircPolRate' + suffix + '.png'
    plot.caxis.fwhmFormatStr = None
    plots.append(plot)

    xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
    yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
    caxis = xrtp.XYCAxis('Es phase', '', data=raycing.get_Es_phase,
                         bins=bins, ppb=ppb)
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
        aspect='auto', title='Es phase')
    plot.saveName = prefix + '6SPhase' + suffix + '.png'
    plot.caxis.fwhmFormatStr = None
    plot.caxis.limits = [-np.pi, np.pi]
    plot.caxis.fwhmFormatStr = None
    plot.ax1dHistE.set_yticks([l*np.pi for l in (-1, -0.5, 0, 0.5, 1)])
    plot.ax1dHistE.set_yticklabels(
        (r'$-\pi$', r'-$\frac{\pi}{2}$', 0, r'$\frac{\pi}{2}$', r'$\pi$'))
    plots.append(plot)

    complexPlotPCA = None
    if False:
        xaxis = xrtp.XYCAxis(r'$x$', 'mm', bins=bins, ppb=ppb)
        yaxis = xrtp.XYCAxis(r'$z$', 'mm', bins=bins, ppb=ppb)
        caxis = xrtp.XYCAxis('energy', eUnit, fwhmFormatStr=None,
                             bins=bins, ppb=ppb)
        plot = xrtp.XYCPlot(
            'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
            fluxKind='EsPCA', title='Es PCA')
        plot.xaxis.limits = xlimits
        plot.yaxis.limits = zlimits
        plot.saveName = prefix + 'EsPCA' + suffix + '.png'
        plot.caxis.fwhmFormatStr = None
        plots.append(plot)
        plotsE.append(plot)
        complexPlotPCA = plot

    ax = plot.xaxis
    edges = np.linspace(ax.limits[0], ax.limits[1], ax.bins+1)
    beamLine.fsmExpX = (edges[:-1] + edges[1:]) * 0.5 / ax.factor
    ax = plot.yaxis
    edges = np.linspace(ax.limits[0], ax.limits[1], ax.bins+1)
    beamLine.fsmExpZ = (edges[:-1] + edges[1:]) * 0.5 / ax.factor

    for plot in plotsE:
        f = plot.caxis.factor
        plot.caxis.limits = eMinRays*f, eMaxRays*f
    for plot in plots:
        plot.xaxis.fwhmFormatStr = '%.2f'
        plot.yaxis.fwhmFormatStr = '%.2f'
        plot.fluxFormatStr = '%.2p'
    return plots, plotsE, complexPlotPCA


def afterScript(plots, complexPlotPCA):
    import scipy.linalg as spl
    if repeats < 4:
        return

    start = time.time()
    k = complexPlotPCA.size2D
    wPCA, vPCA, outPCA = None, None, None
    x = complexPlotPCA.xaxis.binCenters
    y = complexPlotPCA.yaxis.binCenters
    if repeats >= 4:
        pE = complexPlotPCA.total4D
        cEr = pE[:, :repeats]
        cE = np.dot(cEr.T.conjugate(), cEr)
        cE /= np.diag(cE).sum()
        kwargs = dict(eigvals=(repeats-4, repeats-1))
        wPCA, vPCA = spl.eigh(cE, **kwargs)
        print(wPCA)
        outPCA = np.zeros((k, repeats), dtype=np.complex128)
        for i in range(4):
            mPCA = np.outer(vPCA[:, -1-i], vPCA[:, -1-i].T.conjugate())
            outPCA[:, -1-i] = np.dot(cEr, mPCA)[:, 0]
        print("repeats={0}; PCA problem has taken {1} s".format(
              repeats, time.time()-start))
    dump = [repeats, x, y, wPCA, outPCA]

    pickleName = '{0}-{1}repeats.pickle'.format(prefix, repeats)
    with open(pickleName, 'wb') as f:
        pickle.dump(dump, f, -1)
    print("Done")


def main():
    beamLine = build_beamline()
    plots, plotsE, complexPlotPCA = define_plots(beamLine)
    xrtr.run_ray_tracing(plots, repeats=repeats,
                         afterScript=afterScript, afterScriptArgs=[
                             plots, complexPlotPCA],
                         beamLine=beamLine)


def plotPCA():
#    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    cmap = cm.get_cmap('cubehelix')

    pickleName = '{0}-{1}repeats.pickle'.format(prefix, repeats)
    with open(pickleName, 'rb') as f:
        dump = pickle.load(f)

    repeatsS, x, y, wPCA, outPCA = dump
    extent = xlimits + zlimits
    if wPCA is not None:
        print(wPCA)
        norm = (abs(outPCA[:, -4:])**2).sum(axis=0)
        outPCA[:, -4:] /= norm**0.5
        figMs = plt.figure(figsize=(8, 8))
        figMs.suptitle('principal components of one-electron images',
                       fontsize=14)
        p1, p2 = 0.1-0.02, 0.505-0.02
        rect2d = [p1, p2, 0.4, 0.4]
        ax0 = figMs.add_axes(rect2d, aspect=1)
        rect2d = [p2, p2, 0.4, 0.4]
        ax1 = figMs.add_axes(rect2d, aspect=1)
        rect2d = [p1, p1, 0.4, 0.4]
        ax2 = figMs.add_axes(rect2d, aspect=1)
        rect2d = [p2, p1, 0.4, 0.4]
        ax3 = figMs.add_axes(rect2d, aspect=1)
        for ax in [ax0, ax1, ax2, ax3]:
            ax.set_xlim(extent[0], extent[1])
            ax.set_ylim(extent[2], extent[3])
            ax.tick_params(axis='x', colors='grey')
            ax.tick_params(axis='y', colors='grey')
        for ax in [ax0, ax1]:
            ax.xaxis.tick_top()
        for ax in [ax1, ax3]:
            ax.yaxis.tick_right()
        im = (outPCA[:, -1]).reshape(len(y), len(x))
        ax0.imshow(im.real**2 + im.imag**2, extent=extent, cmap=cmap)
        modeName = 'component'
        plt.text(0, extent[-1],
                 '0th (coherent) {0}: w={1:.3f}'.format(modeName, wPCA[-1]),
                 transform=ax0.transData, ha='center', va='top', color='w')
        im = (outPCA[:, -2]).reshape(len(y), len(x))
        ax1.imshow(im.real**2 + im.imag**2, extent=extent, cmap=cmap)
        plt.text(0, extent[-1],
                 '1st residual {0}: w={1:.3f}'.format(modeName, wPCA[-2]),
                 transform=ax1.transData, ha='center', va='top', color='w')
        im = (outPCA[:, -3]).reshape(len(y), len(x))
        ax2.imshow(im.real**2 + im.imag**2, extent=extent, cmap=cmap)
        plt.text(0, extent[-1],
                 '2nd residual {0}: w={1:.3f}'.format(modeName, wPCA[-3]),
                 transform=ax2.transData, ha='center', va='top', color='w')
        im = (outPCA[:, -4]).reshape(len(y), len(x))
        ax3.imshow(im.real**2 + im.imag**2, extent=extent, cmap=cmap)
        plt.text(0, extent[-1],
                 '3rd residual {0}: w={1:.3f}'.format(modeName, wPCA[-4]),
                 transform=ax3.transData, ha='center', va='top', color='w')

        figMs.savefig('Components-{0}-{1}repeats.png'.format(prefix, repeatsS))

    print("Done")
    plt.show()


if __name__ == '__main__':
    main()
#    plotPCA()
