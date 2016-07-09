# -*- coding: utf-8 -*-
__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "08 Mar 2016"

#import matplotlib
#matplotlib.use('agg')

import os, sys; sys.path.append(os.path.join('..', '..', '..'))  # analysis:ignore
import numpy as np
import time
#import matplotlib
#matplotlib.use("Agg")
import xrt.backends.raycing as raycing
import xrt.backends.raycing.sources as rs
import xrt.backends.raycing.screens as rsc
import xrt.backends.raycing.run as rr
import xrt.plotter as xrtp
import xrt.runner as xrtr

suffix = ''
R0 = 25000
xPrimeMax = 0.6
zPrimeMax = 0.6
bins = 512
ppb = 1

#repeats = 40
repeats = 1

sheet, prefix = 'EPU_HP_mode', '1'
#sheet, prefix = 'QEPU_HP_mode', '2'
#sheet, prefix = 'EPU_VP_mode', '3'
#sheet, prefix = 'QEPU_VP_mode', '4'

prefix += 'vortex-' + sheet

#prefix += '-1-band'
#prefix += '-2-1stHarmonic'
prefix += '-3-mono1stHarmonic'
#prefix += '-4-2ndHarmonic'
#prefix += '-5-mono2ndHarmonic'
#prefix += '-6-3rdHarmonic'
#prefix += '-7-mono3rdHarmonic'
#prefix += '-8-5thHarmonic'
#prefix += '-9-mono5thHarmonic'

fixedEnergy = False
filamentBeam = False
if 'VP' in prefix:
    eMinRays, eMaxRays = 3., 60.
else:
    eMinRays, eMaxRays = 3., 40.
if 'mono' in prefix:
    if '1st' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                fixedEnergy = 11.3
            else:
                fixedEnergy = 10.65
        else:
            if 'QEPU' in prefix:
                fixedEnergy = 7.60
            else:
                fixedEnergy = 7.15
    elif '2nd' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                fixedEnergy = 21.9
            else:
                fixedEnergy = 20.7
        else:
            if 'QEPU' in prefix:
                fixedEnergy = 14.65
            else:
                fixedEnergy = 13.9
    elif '3rd' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                fixedEnergy = 34.0
            else:
                fixedEnergy = 32.0
        else:
            if 'QEPU' in prefix:
                fixedEnergy = 20.65
            else:
                fixedEnergy = 21.45
    elif '5th' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                fixedEnergy = 53
            else:
                fixedEnergy = 53.5
        else:
            if 'QEPU' in prefix:
                fixedEnergy = 35.85
            else:
                fixedEnergy = 35.75
    else:
        raise ValueError('unknown harmonic')
    prefix += '-E={0:.2f}eV'.format(fixedEnergy)
    filamentBeam = True
elif 'Harm' in prefix:
    if '1st' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 8.5, 12.
            else:
                eMinRays, eMaxRays = 8., 11.5
        else:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 6.4, 7.9
            else:
                eMinRays, eMaxRays = 6., 7.5
    elif '2nd' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 16., 23.
            else:
                eMinRays, eMaxRays = 16.5, 22.
        else:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 12., 16.
            else:
                eMinRays, eMaxRays = 12., 14.5
    elif '3rd' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 24., 34.5
            else:
                eMinRays, eMaxRays = 25., 33.
        else:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 18., 22.
            else:
                eMinRays, eMaxRays = 18., 22.
    elif '5th' in prefix:
        if 'VP' in prefix:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 43., 55.
            else:
                eMinRays, eMaxRays = 43., 55.
        else:
            if 'QEPU' in prefix:
                eMinRays, eMaxRays = 30.2, 36.2
            else:
                eMinRays, eMaxRays = 30., 36.
    else:
        raise ValueError('unknown harmonic')

Source = rs.Undulator
kwargs = dict(
    eE=1.5, eI=0.5, eEspread=8e-4,
    eEpsilonX=6.0, eEpsilonZ=0.06, betaX=5.66, betaZ=2.85,
    period=84., n=36,
    xPrimeMax=xPrimeMax, zPrimeMax=zPrimeMax,
    xPrimeMaxAutoReduce=False, zPrimeMaxAutoReduce=False,
    filamentBeam=filamentBeam)
xlimits = [-xPrimeMax*R0*1e-3, xPrimeMax*R0*1e-3]
zlimits = [-zPrimeMax*R0*1e-3, zPrimeMax*R0*1e-3]
kwargs['customField'] = ['B-Hamed.xlsx', dict(sheetname=sheet, skiprows=0)]
#kwargs['customField'] = 10.

if True:  # zero source size:
    kwargs['eEpsilonX'] = 0
    kwargs['eEpsilonZ'] = 0
    eEpsilonC = '0'
else:
    eEpsilonC = 'n'

eUnit = 'eV'
kwargs['eMin'] = eMinRays
kwargs['eMax'] = eMaxRays


def build_beamline():
    beamLine = raycing.BeamLine()
    beamLine.source = Source(beamLine, **kwargs)
    beamLine.fsm1 = rsc.Screen(beamLine, 'FSM1', (0, R0, 0))
    return beamLine


def run_process(beamLine):
    startTime = time.time()
    waveOnScreen = beamLine.fsm1.prepare_wave(
        beamLine.source, beamLine.fsmExpX, beamLine.fsmExpZ)
    beamSource = beamLine.source.shine(wave=waveOnScreen,
                                       fixedEnergy=fixedEnergy)
    if 'mono' in prefix:
        x = beamLine.fsmExpX
        z = beamLine.fsmExpZ
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


#    beamSource = beamLine.source.shine(fixedEnergy=fixedEnergy)
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
    plot.saveName = prefix + '1totalFlux' + suffix + '.png'
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
    plot = xrtp.XYCPlot(
        'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis,
        caxis=xrtp.XYCAxis('circular polarization rate', '',
                           data=raycing.get_circular_polarization_rate,
                           limits=[-1, 1], bins=bins, ppb=ppb),
        aspect='auto', title='circular polarization rate')
    plot.saveName = prefix + '4circPolRate' + suffix + '.png'
    plot.caxis.fwhmFormatStr = None
    plots.append(plot)

    ax = plot.xaxis
    edges = np.linspace(ax.limits[0], ax.limits[1], ax.bins+1)
    beamLine.fsmExpX = (edges[:-1] + edges[1:]) * 0.5 / ax.factor
    ax = plot.yaxis
    edges = np.linspace(ax.limits[0], ax.limits[1], ax.bins+1)
    beamLine.fsmExpZ = (edges[:-1] + edges[1:]) * 0.5 / ax.factor

    if 'mono' in prefix:
        xaxis = xrtp.XYCAxis(r'$x$', 'mm', limits=xlimits, bins=bins, ppb=ppb)
        yaxis = xrtp.XYCAxis(r'$z$', 'mm', limits=zlimits, bins=bins, ppb=ppb)
        caxis = xrtp.XYCAxis('Es phase', '', data=raycing.get_Es_phase,
                             bins=bins, ppb=ppb)
        plot = xrtp.XYCPlot(
            'beamFSM1', (1,), xaxis=xaxis, yaxis=yaxis, caxis=caxis,
            aspect='auto', title='Es phase')
        plot.saveName = prefix + '5SPhase' + suffix + '.png'
        plot.caxis.fwhmFormatStr = None
        plot.caxis.limits = [-np.pi, np.pi]
        plot.caxis.fwhmFormatStr = None
        plot.ax1dHistE.set_yticks([l*np.pi for l in (-1, -0.5, 0, 0.5, 1)])
        plot.ax1dHistE.set_yticklabels(
            (r'$-\pi$', r'-$\frac{\pi}{2}$', 0, r'$\frac{\pi}{2}$', r'$\pi$'))
        plots.append(plot)

    for plot in plotsE:
        f = plot.caxis.factor
        plot.caxis.limits = eMinRays*f, eMaxRays*f
    for plot in plots:
        plot.xaxis.fwhmFormatStr = '%.2f'
        plot.yaxis.fwhmFormatStr = '%.2f'
        plot.fluxFormatStr = '%.2p'
    return plots, plotsE


def main():
    beamLine = build_beamline()
    plots, plotsE = define_plots(beamLine)
    xrtr.run_ray_tracing(plots, repeats=repeats, beamLine=beamLine)


if __name__ == '__main__':
    main()
