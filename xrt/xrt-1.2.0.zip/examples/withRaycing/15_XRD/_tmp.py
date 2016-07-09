# -*- coding: utf-8 -*-
"""

__author__ = "Konstantin Klementiev", "Roman Chernikov"
__date__ = "2016-07-07"

Created with xrtQook




Powder Diffraction
------------------

Simulation of the real powder diffraction experiment on PETRA-III
High Resolution Powder Diffraction Beamline P02.1.
Uses Undulator source and double Laue Plate monochromator.
Cerium Dioxide powder as the sample.

.. image:: _images/rings_on_detector.png
   :height: 210

.. warning::
   Heavy computational load. Requires OpenCL.




"""

import numpy as np
import sys
sys.path.append(r"C:\Ray-tracing")
import xrt.backends.raycing.sources as rsources
import xrt.backends.raycing.screens as rscreens
import xrt.backends.raycing.materials as rmats
import xrt.backends.raycing.oes as roes
import xrt.backends.raycing.apertures as rapts
import xrt.backends.raycing.run as rrun
import xrt.backends.raycing as raycing
import xrt.plotter as xrtplot
import xrt.runner as xrtrun

LaueXtal = rmats.CrystalHarmonics(
    Nmax=1,
    name=r"LaueMono",
    tK=0,
    t=0.2,
    geom=r"Laue reflected")

PowderSample = rmats.Powder(
    chi=[0, 2*np.pi],
    name=None,
    hkl=[7, 7, 7],
    a=5.256,
    atoms=[58, 58, 58, 58, 8, 8, 8, 8, 8, 8, 8, 8],
    atomsXYZ=[[0.000, 0.000, 0.000],
         [0.000, 0.500, 0.500],
          [0.500, 0.00, 0.500],
          [0.500, 0.500, 0.00],
          [0.250, 0.250, 0.250],
          [0.250, 0.750, 0.750],
          [0.750, 0.250, 0.750],
          [0.750, 0.750, 0.250],
          [0.750, 0.750, 0.750],
          [0.750, 0.250, 0.250],
          [0.250, 0.750, 0.250],
          [0.250, 0.250, 0.750]],
    t=1.0)


def build_beamline():
    P02_2 = raycing.BeamLine()

    P02_2.Undulator01 = rsources.Undulator(
        bl=P02_2,
        name=r"P02_U23",
        center=[0, 0, 0],
        eE=6.08,
        eI=0.2,
        eEspread=0.001,
        betaX=20.01,
        betaZ=2.36,
        period=23,
        n=87,
        targetE=[60000, 11],
        eMin=59940,
        eMax=60060,
        xPrimeMax=0.06/29,
        zPrimeMax=0.06/29,
        gp=1e-06)

    P02_2.SLIT_FE = rapts.RectangularAperture(
        bl=P02_2,
        name=r"FrontEndSlit",
        center=[0.0, 29000, 0.0],
        opening=[-1., 1., -1., 1.])

    P02_2.FSM_Source = rscreens.Screen(
        bl=P02_2,
        name=r"FSM_Source",
        center=[0.0, 29001, 0.0])

    P02_2.LP1 = roes.LauePlate(
        bl=P02_2,
        name=r"LauePlate1",
        center=[0.0, 36000, 0.0],
        pitch=0.0,
        positionRoll=np.pi*0.5,
        material=LaueXtal,
        targetOpenCL=r"auto")

    P02_2.LP2 = roes.LauePlate(
        bl=P02_2,
        name=r"LauePlate2",
        center=[0.0, 44000, 0.0],
        pitch=0.0,
        positionRoll=-np.pi*0.5,
        material=LaueXtal,
        targetOpenCL=r"auto")

    P02_2.FSM_DCM = rscreens.Screen(
        bl=P02_2,
        name=r"DCM_Screen",
        center=[0.0, 44500, 0.0])

    P02_2.Slit_EH = rapts.RectangularAperture(
        bl=P02_2,
        name=r"ExperimentalHutchSlit",
        center=[0.0, 62000, 0.0],
        opening=[-1., 1., -1., 1.])

    P02_2.PowderSample = roes.LauePlate(
        bl=P02_2,
        name=r"CeO2 Powder",
        center=[0.0, 65000, 0.0],
        pitch=np.pi*0.5,
        material=PowderSample,
        targetOpenCL=r"auto")

    P02_2.FSM_Sample = rscreens.Screen(
        bl=P02_2,
        name=None,
        center=[P02_2.PowderSample.center[0], 65100, P02_2.PowderSample.center[2]])

    P02_2.RoundBeamStop01 = rapts.RoundBeamStop(
        bl=P02_2,
        name=r"BeamStop",
        center=[P02_2.PowderSample.center[0], 65499, P02_2.PowderSample.center[2]],
        r=20)

    P02_2.FSM_Detector = rscreens.Screen(
        bl=P02_2,
        name=r"Detector",
        center=[P02_2.PowderSample.center[0], 65500, P02_2.PowderSample.center[2]])

    return P02_2


def run_process(P02_2):
    Undulator01beamGlobal01 = P02_2.Undulator01.shine(
        withAmplitudes=False)

    SLIT_FEbeamLocal01 = P02_2.SLIT_FE.propagate(
        beam=Undulator01beamGlobal01)

    FSM_SourcebeamLocal01 = P02_2.FSM_Source.expose(
        beam=Undulator01beamGlobal01)

    LP1beamGlobal01, LP1beamLocal01 = P02_2.LP1.reflect(
        beam=Undulator01beamGlobal01)

    LP2beamGlobal01, LP2beamLocal01 = P02_2.LP2.reflect(
        beam=LP1beamGlobal01)

    FSM_DCMbeamLocal01 = P02_2.FSM_DCM.expose(
        beam=LP2beamGlobal01)

    Slit_EHbeamLocal01 = P02_2.Slit_EH.propagate(
        beam=LP2beamGlobal01)

    PowderSamplebeamGlobal01, PowderSamplebeamLocal01 = P02_2.PowderSample.reflect(
        beam=LP2beamGlobal01)

    FSM_SamplebeamLocal01 = P02_2.FSM_Sample.expose(
        beam=PowderSamplebeamGlobal01)

    RoundBeamStop01beamLocal01 = P02_2.RoundBeamStop01.propagate(
        beam=PowderSamplebeamGlobal01)

    FSM_DetectorbeamLocal01 = P02_2.FSM_Detector.expose(
        beam=PowderSamplebeamGlobal01)

    outDict = {
        'Undulator01beamGlobal01': Undulator01beamGlobal01,
        'FSM_SourcebeamLocal01': FSM_SourcebeamLocal01,
        'SLIT_FEbeamLocal01': SLIT_FEbeamLocal01,
        'LP1beamGlobal01': LP1beamGlobal01,
        'LP1beamLocal01': LP1beamLocal01,
        'LP2beamGlobal01': LP2beamGlobal01,
        'LP2beamLocal01': LP2beamLocal01,
        'FSM_DCMbeamLocal01': FSM_DCMbeamLocal01,
        'Slit_EHbeamLocal01': Slit_EHbeamLocal01,
        'PowderSamplebeamGlobal01': PowderSamplebeamGlobal01,
        'PowderSamplebeamLocal01': PowderSamplebeamLocal01,
        'FSM_SamplebeamLocal01': FSM_SamplebeamLocal01,
        'FSM_DetectorbeamLocal01': FSM_DetectorbeamLocal01,
        'RoundBeamStop01beamLocal01': RoundBeamStop01beamLocal01}
    return outDict


rrun.run_process = run_process


def align_beamline(P02_2, energy):
    Undulator01beamGlobal01 = rsources.Beam(nrays=2)
    Undulator01beamGlobal01.a[:] = 0
    Undulator01beamGlobal01.b[:] = 1
    Undulator01beamGlobal01.c[:] = 0
    Undulator01beamGlobal01.x[:] = 0
    Undulator01beamGlobal01.y[:] = 0
    Undulator01beamGlobal01.z[:] = 0
    Undulator01beamGlobal01.state[:] = 1

    tmpy = P02_2.SLIT_FE.center[1]
    newx = Undulator01beamGlobal01.x[0] +\
        Undulator01beamGlobal01.a[0] * (tmpy - Undulator01beamGlobal01.y[0]) /\
        Undulator01beamGlobal01.b[0]
    newz = Undulator01beamGlobal01.z[0] +\
        Undulator01beamGlobal01.c[0] * (tmpy - Undulator01beamGlobal01.y[0]) /\
        Undulator01beamGlobal01.b[0]
    P02_2.SLIT_FE.center = (newx, tmpy, newz)
    print("SLIT_FE.center:", P02_2.SLIT_FE.center)

    SLIT_FEbeamLocal01 = P02_2.SLIT_FE.propagate(
        beam=Undulator01beamGlobal01)
    tmpy = P02_2.FSM_Source.center[1]
    newx = Undulator01beamGlobal01.x[0] +\
        Undulator01beamGlobal01.a[0] * (tmpy - Undulator01beamGlobal01.y[0]) /\
        Undulator01beamGlobal01.b[0]
    newz = Undulator01beamGlobal01.z[0] +\
        Undulator01beamGlobal01.c[0] * (tmpy - Undulator01beamGlobal01.y[0]) /\
        Undulator01beamGlobal01.b[0]
    P02_2.FSM_Source.center = (newx, tmpy, newz)
    print("FSM_Source.center:", P02_2.FSM_Source.center)

    FSM_SourcebeamLocal01 = P02_2.FSM_Source.expose(
        beam=Undulator01beamGlobal01)
    tmpy = P02_2.LP1.center[1]
    newx = Undulator01beamGlobal01.x[0] +\
        Undulator01beamGlobal01.a[0] * (tmpy - Undulator01beamGlobal01.y[0]) /\
        Undulator01beamGlobal01.b[0]
    newz = Undulator01beamGlobal01.z[0] +\
        Undulator01beamGlobal01.c[0] * (tmpy - Undulator01beamGlobal01.y[0]) /\
        Undulator01beamGlobal01.b[0]
    P02_2.LP1.center = (newx, tmpy, newz)
    print("LP1.center:", P02_2.LP1.center)

    braggT = LaueXtal.get_Bragg_angle(energy)
    alphaT = 0 if P02_2.LP1.alpha is None else P02_2.LP1.alpha
    lauePitch = 0
    print("bragg, alpha:", np.degrees(braggT), np.degrees(alphaT), "degrees")

    braggT += -LaueXtal.get_dtheta(energy, alphaT)
    if LaueXtal.geom.startswith('Laue'):
        lauePitch = 0.5 * np.pi
    print("braggT:", np.degrees(braggT), "degrees")

    loBeam = rsources.Beam(copyFrom=Undulator01beamGlobal01)
    raycing.global_to_virgin_local(
        P02_2,
        Undulator01beamGlobal01,
        loBeam,
        center=P02_2.LP1.center)
    raycing.rotate_beam(
        loBeam,
        roll=-(P02_2.LP1.positionRoll + P02_2.LP1.roll),
        yaw=-P02_2.LP1.yaw,
        pitch=0)
    theta0 = np.arctan2(-loBeam.c[0], loBeam.b[0])
    th2pitch = np.sqrt(1. - loBeam.a[0]**2)
    targetPitch = np.arcsin(np.sin(braggT) / th2pitch) -\
        theta0
    targetPitch += alphaT + lauePitch
    P02_2.LP1.pitch = targetPitch
    print("LP1.pitch:", np.degrees(P02_2.LP1.pitch), "degrees")

    LP1beamGlobal01, LP1beamLocal01 = P02_2.LP1.reflect(
        beam=Undulator01beamGlobal01)
    tmpy = P02_2.LP2.center[1]
    newx = LP1beamGlobal01.x[0] +\
        LP1beamGlobal01.a[0] * (tmpy - LP1beamGlobal01.y[0]) /\
        LP1beamGlobal01.b[0]
    newz = LP1beamGlobal01.z[0] +\
        LP1beamGlobal01.c[0] * (tmpy - LP1beamGlobal01.y[0]) /\
        LP1beamGlobal01.b[0]
    P02_2.LP2.center = (newx, tmpy, newz)
    print("LP2.center:", P02_2.LP2.center)

    braggT = LaueXtal.get_Bragg_angle(energy)
    alphaT = 0 if P02_2.LP2.alpha is None else P02_2.LP2.alpha
    lauePitch = 0
    print("bragg, alpha:", np.degrees(braggT), np.degrees(alphaT), "degrees")

    braggT += -LaueXtal.get_dtheta(energy, alphaT)
    if LaueXtal.geom.startswith('Laue'):
        lauePitch = 0.5 * np.pi
    print("braggT:", np.degrees(braggT), "degrees")

    loBeam = rsources.Beam(copyFrom=LP1beamGlobal01)
    raycing.global_to_virgin_local(
        P02_2,
        LP1beamGlobal01,
        loBeam,
        center=P02_2.LP2.center)
    raycing.rotate_beam(
        loBeam,
        roll=-(P02_2.LP2.positionRoll + P02_2.LP2.roll),
        yaw=-P02_2.LP2.yaw,
        pitch=0)
    theta0 = np.arctan2(-loBeam.c[0], loBeam.b[0])
    th2pitch = np.sqrt(1. - loBeam.a[0]**2)
    targetPitch = np.arcsin(np.sin(braggT) / th2pitch) -\
        theta0
    targetPitch += alphaT + lauePitch
    P02_2.LP2.pitch = targetPitch
    print("LP2.pitch:", np.degrees(P02_2.LP2.pitch), "degrees")

    LP2beamGlobal01, LP2beamLocal01 = P02_2.LP2.reflect(
        beam=LP1beamGlobal01)
    tmpy = P02_2.FSM_DCM.center[1]
    newx = LP2beamGlobal01.x[0] +\
        LP2beamGlobal01.a[0] * (tmpy - LP2beamGlobal01.y[0]) /\
        LP2beamGlobal01.b[0]
    newz = LP2beamGlobal01.z[0] +\
        LP2beamGlobal01.c[0] * (tmpy - LP2beamGlobal01.y[0]) /\
        LP2beamGlobal01.b[0]
    P02_2.FSM_DCM.center = (newx, tmpy, newz)
    print("FSM_DCM.center:", P02_2.FSM_DCM.center)

    FSM_DCMbeamLocal01 = P02_2.FSM_DCM.expose(
        beam=LP2beamGlobal01)
    tmpy = P02_2.Slit_EH.center[1]
    newx = LP2beamGlobal01.x[0] +\
        LP2beamGlobal01.a[0] * (tmpy - LP2beamGlobal01.y[0]) /\
        LP2beamGlobal01.b[0]
    newz = LP2beamGlobal01.z[0] +\
        LP2beamGlobal01.c[0] * (tmpy - LP2beamGlobal01.y[0]) /\
        LP2beamGlobal01.b[0]
    P02_2.Slit_EH.center = (newx, tmpy, newz)
    print("Slit_EH.center:", P02_2.Slit_EH.center)

    Slit_EHbeamLocal01 = P02_2.Slit_EH.propagate(
        beam=LP2beamGlobal01)
    tmpy = P02_2.PowderSample.center[1]
    newx = LP2beamGlobal01.x[0] +\
        LP2beamGlobal01.a[0] * (tmpy - LP2beamGlobal01.y[0]) /\
        LP2beamGlobal01.b[0]
    newz = LP2beamGlobal01.z[0] +\
        LP2beamGlobal01.c[0] * (tmpy - LP2beamGlobal01.y[0]) /\
        LP2beamGlobal01.b[0]
    P02_2.PowderSample.center = (newx, tmpy, newz)
    print("PowderSample.center:", P02_2.PowderSample.center)

    PowderSamplebeamGlobal01, PowderSamplebeamLocal01 = P02_2.PowderSample.reflect(
        beam=LP2beamGlobal01)
    P02_2.FSM_Sample.center=[P02_2.PowderSample.center[0], 65100, P02_2.PowderSample.center[2]]
    tmpy = P02_2.FSM_Sample.center[1]
    newx = P02_2.FSM_Sample.center[0]
    newz = P02_2.FSM_Sample.center[2]
    P02_2.FSM_Sample.center = (newx, tmpy, newz)
    print("FSM_Sample.center:", P02_2.FSM_Sample.center)

    FSM_SamplebeamLocal01 = P02_2.FSM_Sample.expose(
        beam=PowderSamplebeamGlobal01)
    P02_2.RoundBeamStop01.center=[P02_2.PowderSample.center[0], 65499, P02_2.PowderSample.center[2]]
    tmpy = P02_2.RoundBeamStop01.center[1]
    newx = P02_2.RoundBeamStop01.center[0]
    newz = P02_2.RoundBeamStop01.center[2]
    P02_2.RoundBeamStop01.center = (newx, tmpy, newz)
    print("RoundBeamStop01.center:", P02_2.RoundBeamStop01.center)

    RoundBeamStop01beamLocal01 = P02_2.RoundBeamStop01.propagate(
        beam=PowderSamplebeamGlobal01)
    P02_2.FSM_Detector.center=[P02_2.PowderSample.center[0], 65500, P02_2.PowderSample.center[2]]
    tmpy = P02_2.FSM_Detector.center[1]
    newx = P02_2.FSM_Detector.center[0]
    newz = P02_2.FSM_Detector.center[2]
    P02_2.FSM_Detector.center = (newx, tmpy, newz)
    print("FSM_Detector.center:", P02_2.FSM_Detector.center)

    FSM_DetectorbeamLocal01 = P02_2.FSM_Detector.expose(
        beam=PowderSamplebeamGlobal01)


def define_plots():
    plots = []

    Plot01 = xrtplot.XYCPlot(
        beam=r"FSM_SourcebeamLocal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        yaxis=xrtplot.XYCAxis(
            label=r"z",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        title=r"01 - Undulator Beam at 29m",
        saveName=r"01 - Undulator Beam at 29m.png")
    plots.append(Plot01)

    Plot02 = xrtplot.XYCPlot(
        beam=r"FSM_DCMbeamLocal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        yaxis=xrtplot.XYCAxis(
            label=r"z",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        title=r"02 - Monocromatized Beam",
        saveName=r"02 - Monocromatized Beam.png")
    plots.append(Plot02)

    Plot03 = xrtplot.XYCPlot(
        beam=r"FSM_DetectorbeamLocal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x",
            limits=[-100, 100],
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        yaxis=xrtplot.XYCAxis(
            label=r"z",
            limits=[-100, 100],
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        title=r"03 - Detector",
        saveName=r"03 - Detector.png",
        persistentName=r"03 - Detector.mat")
    plots.append(Plot03)

    Plot04 = xrtplot.XYCPlot(
        beam=r"LP1beamLocal01",
        xaxis=xrtplot.XYCAxis(
            label=r"x",
            limits=[-1, 1],
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        yaxis=xrtplot.XYCAxis(
            label=r"y",
            limits=[-1, 1],
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        caxis=xrtplot.XYCAxis(
            label=r"energy",
            unit=r"eV",
            bins=256,
            ppb=1,
            fwhmFormatStr=r"%.2f"),
        title=r"04 -Laue Plate 1 Footprint",
        saveName=r"Plo04.title.png")
    plots.append(Plot04)
    return plots


def main():
    P02_2 = build_beamline()
    E0 = 0.5 * (P02_2.Undulator01.eMin +
                P02_2.Undulator01.eMax)
    align_beamline(P02_2, E0)
    plots = define_plots()
    xrtrun.run_ray_tracing(
        plots=plots,
        repeats=1000,
        pickleEvery=10,
        backend=r"raycing",
        beamLine=P02_2)


if __name__ == '__main__':
    main()
