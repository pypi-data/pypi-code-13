#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INVENTARI DE CNMC Trafos
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

        trafo = O.GiscedataTransformadorTrafo.read(
            item, ['cini', 'historic', 'data_aps', 'ct', 'name',
                   'potencia_nominal', 'codi_instalacio'])

        #La propia empresa
        company = O.ResCompany.get(1)
        if trafo['codi_instalacio']:
            codi = trafo['codi_instalacio']

        if trafo['historic']:
            historic = O.GiscedataTransformadorHistoric.read(
                trafo['historic'][0], ['data_entrada'])
            data_hist = historic['data_entrada']
        for hist_id in trafo['historic']:
            historic = O.GiscedataTransformadorHistoric.read(
                hist_id, ['data_entrada'])
            if historic['data_entrada'] < data_hist:
                data_hist = historic['data_entrada']

        data_pm = trafo['data_aps'] or data_hist
        if data_pm:
            data_pm = datetime.strptime(str(data_pm), '%Y-%m-%d %H:%M:%S')
            data_pm = data_pm.strftime('%d/%m/%Y')

        comunitat = ''
        c_ccaa = ''
        finan = 0
        if trafo['ct']:
            cts = O.GiscedataCts.read(trafo['ct'][0], ['id_municipi',
                                                       'perc_financament'])
            id_comunitat = O.ResComunitat_autonoma.get_ccaa_from_municipi(
                [], cts['id_municipi'][0])
            comunidad = O.ResComunitat_autonoma.read(id_comunitat, ['codi'])
            if comunidad:
                comunitat = comunidad[0]['codi']
            finan = cts['perc_financament']
        if len(company.partner_id.address):
            if company.partner_id.address[0].state_id:
                c_ccaa = company.partner_id.address[0].state_id.comunitat_autonoma.codi

        output = [
            '%s' % trafo['name'],
            trafo['cini'] or '',
            trafo['name'] or '',
            codi or '',
            '',
            comunitat or c_ccaa or '',
            round(100 - int(finan)),
            data_pm,
            '',
            trafo['potencia_nominal']
        ]

        output_q.put(output)
        input_q.task_done()


def progress(total, input_q):
    """Rendering del progressbar de l'informe.
    """
    widgets = ['CNMC INVENTARI Trafos informe: ', Percentage(), ' ', Bar(), ' ', ETA()]
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