#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INVENTARI DE CNMC
Script per passar crear els cinis correctament a la taula de maquines
"""

import sys
import os
import multiprocessing
import pprint
from datetime import datetime
from optparse import OptionGroup, OptionParser
import csv
import math

from libcnmc1048.loop import OOOP
from progressbar import ProgressBar, ETA, Percentage, Bar
from libcnmc1048 import __version__

N_PROC = min(int(os.getenv('N_PROC', multiprocessing.cpu_count())),
             multiprocessing.cpu_count())
QUIET = False
INTERACTIVE = True


def producer(sequence, output_q):
    """Posem els items que serviran per fer l'informe.
    """
    for item in sequence:
        output_q.put(item)


def consumer(input_q, output_q, progress_q):
    """Creació dels CINIS"""

    while True:
        item = input_q.get()
        progress_q.put(item)
        cini = ''
        trafo = O.GiscedataTransformadorTrafo.read(
            item, ['cini', 'tensio_primari_actual', 'tensio_b1', 'tensio_b2',
                   'potencia_nominal', 'reductor'])

        if not trafo['cini']:
            #Els cinis de màquines tots començen amb I27
            cini_ = "I27"
            #Per completar el tercer digit
            codi3 = ''
            if trafo['tensio_primari_actual'] <= 40000:
                codi3 = '0'
            elif 220000 <= trafo['tensio_primari_actual'] < 400000:
                codi3 = '1'
            elif 110000 <= trafo['tensio_primari_actual'] < 220000:
                codi3 = '2'
            elif 36000 <= trafo['tensio_primari_actual'] < 110000:
                codi3 = '3'
            elif 1000 <= trafo['tensio_primari_actual'] < 36000:
                codi3 = '4'
            #Per completar el quart digit
            codi4 = ''
            if trafo['tensio_b1']:
                if 110000 <= trafo['tensio_b1'] < 220000:
                    codi4 = '2'
                elif 36000 <= trafo['tensio_b1'] < 110000:
                    codi4 = '3'
                elif 1000 <= trafo['tensio_b1'] < 36000:
                    codi4 = '4'
                elif trafo['tensio_b1'] < 1000:
                    codi4 = '4'
            elif trafo['tensio_b2']:
                if 110000 <= trafo['tensio_b2'] < 220000:
                    codi4 = '2'
                elif 36000 <= trafo['tensio_b2'] < 110000:
                    codi4 = '3'
                elif 1000 <= trafo['tensio_b2'] < 36000:
                    codi4 = '4'
                elif trafo['tensio_b2'] < 1000:
                    codi4 = '4'
            #Per completar el cinquè digit
            codi5 = ''
            if trafo['reductor']:
                codi5 = '1'
            else:
                codi5 = '2'
            #Per completar el sisè digit
            codi6 = ''
            if trafo['potencia_nominal'] < 1000:
                codi6 = 'A'
            elif 1000 <= trafo['potencia_nominal'] < 5000:
                codi6 = 'B'
            elif 5000 <= trafo['potencia_nominal'] < 10000:
                codi6 = 'C'
            elif 10000 <= trafo['potencia_nominal'] < 15000:
                codi6 = 'D'
            elif 15000 <= trafo['potencia_nominal'] < 20000:
                codi6 = 'E'
            elif 20000 <= trafo['potencia_nominal'] < 25000:
                codi6 = 'F'
            elif 25000 <= trafo['potencia_nominal'] < 30000:
                codi6 = 'G'
            elif 30000 <= trafo['potencia_nominal'] < 40000:
                codi6 = 'H'
            elif 40000 <= trafo['potencia_nominal'] < 60000:
                codi6 = 'I'
            elif 60000 <= trafo['potencia_nominal'] < 80000:
                codi6 = 'J'
            elif 80000 <= trafo['potencia_nominal'] < 100000:
                codi6 = 'K'
            elif 100000 <= trafo['potencia_nominal'] < 120000:
                codi6 = 'L'
            elif 120000 <= trafo['potencia_nominal'] < 150000:
                codi6 = 'M'
            elif 150000 >= trafo['potencia_nominal']:
                codi6 = 'N'

            cini = cini_ + codi3 + codi4 + codi5 + codi6
            #El write del cini en cada un dels trafos
            O.GiscedataTransformadorTrafo.write([item], {'cini': cini})

        output_q.put(cini)
        input_q.task_done()


def progress(total, input_q):
    """Rendering del progressbar de l'informe.
    """
    widgets = ['CNMC INVENTARI Trafos informe: ', Percentage(), ' ', Bar(),
               ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=total).start()
    done = 0
    while True:
        input_q.get()
        done += 1
        pbar.update(done)
        if done >= total:
            pbar.finish()


def main():
    sequence = []
    search_params = [('name', '!=', '1'),
                     ('id_estat.cnmc_inventari', '=', True)]
    sequence += O.GiscedataTransformadorTrafo.search(search_params)
    if not QUIET or INTERACTIVE:
        sys.stderr.write("Filtres utilitzats:\n")
        pprint.pprint(search_params, sys.stderr)
        sys.stderr.write("S'han trobat %s maquines.\n" % len(sequence))
        sys.stderr.flush()
    if INTERACTIVE:
        sys.stderr.write("Correcte? ")
        raw_input()
        sys.stderr.flush()
    start = datetime.now()
    q = multiprocessing.JoinableQueue()
    q2 = multiprocessing.Queue()
    q3 = multiprocessing.Queue()
    processes = [multiprocessing.Process(target=consumer, args=(q, q2, q3))
                 for x in range(0, N_PROC)]
    if not QUIET:
        processes += [multiprocessing.Process(target=progress,
                                              args=(len(sequence), q3))]
    for proc in processes:
        proc.daemon = True
        proc.start()
        if not QUIET:
            sys.stderr.write("^Starting process PID: %s\n" % proc.pid)
    sys.stderr.flush()
    producer(sequence, q)
    q.join()
    if not QUIET:
        sys.stderr.write("Time Elapsed: %s\n" % (datetime.now() - start))
        sys.stderr.flush()
    while not q2.empty():
        msg = q2.get()
        print "CINI: %s" % msg

if __name__ == '__main__':
    try:
        parser = OptionParser(usage="%prog [OPTIONS]", version=__version__)
        parser.add_option("-q", "--quiet", dest="quiet",
                          action="store_true", default=False,
                          help="No mostrar missatges de status per stderr")
        parser.add_option("--no-interactive", dest="interactive",
                          action="store_false", default=True,
                          help="Deshabilitar el mode interactiu")
        group = OptionGroup(parser, "Server options")
        group.add_option("-s", "--server", dest="server", default="localhost",
                         help=u"Adreça servidor ERP")
        group.add_option("-p", "--port", dest="port", default=8069,
                         help="Port servidor ERP")
        group.add_option("-u", "--user", dest="user", default="admin",
                         help="Usuari servidor ERP")
        group.add_option("-w", "--password", dest="password", default="admin",
                         help="Contrasenya usuari ERP")
        group.add_option("-d", "--database", dest="database",
                         help="Nom de la base de dades")

        parser.add_option_group(group)
        (options, args) = parser.parse_args()
        QUIET = options.quiet
        INTERACTIVE = options.interactive

        O = OOOP(dbname=options.database, user=options.user,
                 pwd=options.password, port=int(options.port))

        main()

    except KeyboardInterrupt:
        pass

