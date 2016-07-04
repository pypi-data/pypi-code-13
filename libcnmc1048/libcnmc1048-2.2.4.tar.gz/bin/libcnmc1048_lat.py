#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INVENTARI DE CNMC AT
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
    """Informe"""

    while True:
        item = input_q.get()
        progress_q.put(item)

        linia = O.GiscedataAtLinia.read(item, ['trams', 'tensio', 'municipi'])

        for tramo in linia['trams']:
            tram = O.GiscedataAtTram.read(tramo,
                                          ['baixa', 'data_pm', 'data_industria',
                                           'coeficient', 'cini',
                                           'tensio_max_disseny', 'name',
                                           'origen', 'final',
                                           'perc_financament', 'circuits',
                                           'longitud_cad', 'cable'])

            #Si el tram es de baixa no l'afegim
            if tram['baixa']:
                continue
            # Calculem any posada en marxa
            if not tram['data_pm']:
                data_pm = tram['data_industria'] or ''
            else:
                data_pm = tram['data_pm']

            if data_pm:
                data_pm = datetime.strptime(str(data_pm), '%Y-%m-%d')
                data_pm = data_pm.strftime('%d/%m/%Y')

            # Coeficient per ajustar longituds de trams
            coeficient = tram['coeficient'] or 1.0

            tipus_inst_id = O.Giscedata_cnmcTipo_instalacion.search(
                [('cini', '=', tram['cini'])])
            codigo = O.Giscedata_cnmcTipo_instalacion.read(tipus_inst_id,
                                                           ['codi'])
            if codigo:
                codi = codigo[0]
            else:
                codi = {'codi': ' '}

            #Agafem la tensió
            tensio = tram['tensio_max_disseny'] or linia['tensio']

            id_comunitat = O.ResComunitat_autonoma.get_ccaa_from_municipi(
                [], linia['municipi'][0])
            comunidad = O.ResComunitat_autonoma.read(id_comunitat, ['codi'])
            if comunidad:
                comunitat = comunidad[0]

            # Agafem el cable de la linia
            cable = O.GiscedataAtCables.read(tram['cable'][0], [
                'intensitat_admisible', 'seccio'])

            output = [
                'A%s' % tram['name'],
                tram['cini'] or '',
                tram['origen'] or '',
                tram['final'] or '',
                codi['codi'] or '',
                comunitat['codi'] or '',
                comunitat['codi'] or '',
                round(100 - int(tram['perc_financament'])),
                data_pm,
                '',
                tram['circuits'] or 1,
                1,
                round(tram['longitud_cad'] * coeficient / 1000.0, 3) or 0,
                cable['seccio'],
                round(
                    (cable['intensitat_admisible'] * tensio *
                     math.sqrt(3))/1000, 3)]

            output_q.put(output)

        input_q.task_done()


def progress(total, input_q):
    """Rendering del progressbar de l'informe.
    """
    widgets = ['CNMC INVENTARI AT informe: ', Percentage(), ' ', Bar(), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=total).start()
    done = 0
    while True:
        input_q.get()
        done += 1
        pbar.update(done)
        if done >= total:
            pbar.finish()


def main(file_out):
    """Funció principal del programa"""
    sequence = []
    search_params = [('name', '!=', '1')]
    sequence += O.GiscedataAtLinia.search(search_params)
    if not QUIET or INTERACTIVE:
        sys.stderr.write("Filtres utilitzats:\n")
        pprint.pprint(search_params, sys.stderr)
        sys.stderr.write("S'han trobat %s línies.\n" % len(sequence))
        sys.stderr.flush()
    if INTERACTIVE:
        sys.stderr.write("Correcte? ")
        raw_input()
        sys.stderr.flush()

    #Buscar trams actius i de baixa
    search_params = [('active', '=', 1),
                     ('baixa', '=', 1)]
    trams_indef = O.GiscedataAtTram.search(search_params)
    if trams_indef:
        long_cad = 0
        for tram in O.GiscedataAtTram.read(trams_indef, ['longitud_cad']):
            long_cad += tram['longitud_cad']
        if not QUIET or INTERACTIVE:
            sys.stderr.write("*** ATENCIÓ ***\n")
            sys.stderr.write("S'han trobat %i trams que estan actius i de "
                             "baixa al mateix temps. Sumen %f m.\n"
                             % (len(trams_indef), long_cad))
            sys.stderr.write("Si estan marcats com a baixa, no s'inclouran en "
                             "l'informe.\n")
            sys.stderr.flush()
        if INTERACTIVE:
            sys.stderr.write("Continuar igualment? ")
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
    fout = open(file_out, 'wb')
    fitxer = csv.writer(fout, delimiter=';', lineterminator='\n')
    while not q2.empty():
        msg = q2.get()
        msg = map(lambda x: type(x) == unicode and x.encode('utf-8') or x, msg)
        fitxer.writerow(msg)

if __name__ == '__main__':
    try:
        parser = OptionParser(usage="%prog [OPTIONS]", version=__version__)
        parser.add_option("-q", "--quiet", dest="quiet",
                          action="store_true", default=False,
                          help="No mostrar missatges de status per stderr")
        parser.add_option("--no-interactive", dest="interactive",
                          action="store_false", default=True,
                          help="Deshabilitar el mode interactiu")
        parser.add_option("-o", "--output", dest="fout",
                          help="Fitxer de sortida")

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
        if not options.fout:
            parser.error("Es necessita indicar un nom de fitxer")
        O = OOOP(dbname=options.database, user=options.user,
                 pwd=options.password, port=int(options.port))

        main(options.fout)

    except KeyboardInterrupt:
        pass