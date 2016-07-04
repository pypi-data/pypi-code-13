#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INVENTARI DE CNMC
Script per passar crear els cinis correctament a la taula de posicions
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
    """CreaciÃ³ dels CINIS"""

    while True:
        item = input_q.get()
        progress_q.put(item)
        cini = ''
        trafo = O.GiscedataCtsSubestacionsPosicio.read(
            item, ['cini', 'tensio', 'interruptor', 'tipus_posicio', 'barres'])

        if not trafo['cini']:
            #Els cinis de mÃ quines tots comenÃ§en amb I27
            cini_ = "I28"
            #Per completar el tercer digit
            codi3 = ''
            if 110000 <= trafo['tensio'] < 220000:
                codi3 = '2'
            elif 36000 <= trafo['tensio'] < 110000:
                codi3 = '3'
            elif 1000 <= trafo['tensio'] < 36000:
                codi3 = '4'
            #Per completar el quart digit
            codi4 = ''
            if trafo['interruptor']:
                #els codis  de cini coincideixen amb els que tenim d'interruptor
                codi4 = '%s' % trafo['interruptor']
            #Per completar el cinque digit
            codi5 = ''
            if trafo['tipus_posicio'] == 'B':
                codi5 = '2'
            elif trafo['tipus_posicio'] == 'C':
                codi5 = '1'
            elif trafo['tipus_posicio'] == 'H':
                codi5 = '3'
            #Per completar el sise digit
            codi6 = ''
            if trafo['barres']:
                codi6 = '%s' % trafo['barres']

            cini = cini_ + codi3 + codi4 + codi5 + codi6
            #El write del cini en cada un dels trafos
            O.GiscedataTransformadorTrafo.write([item], {'cini': cini})

        output_q.put(cini)
        input_q.task_done()


def progress(total, input_q):
    """Rendering del progressbar de l'informe.
    """
    widgets = ['CNMC INVENTARI CINI Posicions: ', Percentage(), ' ', Bar(),
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
    search_params = [('name', '!=', '1')]
    sequence += O.GiscedataCtsSubestacionsPosicio.search(search_params)
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
                         help=u"AdreÃ§a servidor ERP")
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

