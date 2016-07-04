#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INVENTARI DE CNMC BT
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
    count = 0

    while True:
        try:
            count += 1
            item = input_q.get()
            progress_q.put(item)
            data_pm = False

            linia = O.GiscedataBtElement.read(item,
                                              ['name', 'municipi',
                                               'data_acta_posada_marxa', 'ct',
                                               'coeficient', 'cini',
                                               'perc_financament',
                                               'longitud_cad',
                                               'cable', 'voltatge'])

            res = O.GiscegisEdge.search([('id_linktemplate', '=', linia['name']),
                                         ('layer', 'ilike', '%BT%')])
            if not res:
                if not QUIET:
                    sys.stderr.write("**** ERROR: l'element %s (id:%s) no està "
                                     "en giscegis_edges.\n" % (linia['name'],
                                                               linia['id']))
                    sys.stderr.flush()
                edge = {'start_node': (0, '%s_0' % linia['name']),
                        'end_node': (0, '%s_1' % linia['name'])}
            elif len(res) > 1:
                if not QUIET:
                    sys.stderr.write("**** ERROR: l'element %s (id:%s) està més "
                                     "d'una vegada a giscegis_edges. %s\n" %
                                     (linia['name'], linia['id'], res))
                    sys.stderr.flush()
                edge = {'start_node': (0, '%s_0' % linia['name']),
                        'end_node': (0, '%s_1' % linia['name'])}
            else:
                edge = O.GiscegisEdge.read(res[0], ['start_node', 'end_node'])
            if linia['municipi']:
                id_comunitat = O.ResComunitat_autonoma.get_ccaa_from_municipi(
                    [], linia['municipi'][0])
                comunidad = O.ResComunitat_autonoma.read(id_comunitat, ['codi'])
                if comunidad:
                    comunitat = comunidad[0]
                else:
                    comunitat = {'codi': ''}

            if linia['ct']:
                #Agafar les dates del centrestransformadors
                cts = O.GiscedataCts.read(linia['ct'][0],
                                          ['data_industria', 'data_pm'])
                # Calculem any posada en marxa
                data_pm = linia['data_acta_posada_marxa'] or cts[
                    'data_industria'] or cts['data_pm']

            if data_pm:
                data_pm = datetime.strptime(str(data_pm), '%Y-%m-%d')
                data_pm = data_pm.strftime('%d/%m/%Y')

            # Coeficient per ajustar longituds de trams
            coeficient = linia['coeficient'] or 1.0

            # Afagem el tipus de instalacio
            tipus_inst_id = O.Giscedata_cnmcTipo_instalacion.search(
                [('cini', '=', linia['cini'])])
            codigo = O.Giscedata_cnmcTipo_instalacion.read(
                tipus_inst_id, ['codi'])
            if codigo:
                codi = codigo[0]
            else:
                codi = {'codi': ''}

            # Agafem el cable de la linia
            if linia['cable']:
                cable = O.GiscedataBtCables.read(linia['cable'][0], [
                    'intensitat_admisible', 'seccio'])
            else:
                cable = {'seccio': 0, 'intensitat_admisible': 0}

            output = [
                'B%s' % linia['name'],
                linia['cini'] or '',
                edge['start_node'][1] or '',
                edge['end_node'][1] or '',
                codi['codi'] or '',
                comunitat['codi'] or '',
                comunitat['codi'] or '',
                round(100 - int(linia['perc_financament'])),
                data_pm or '',
                '',
                1,
                1,
                round(linia['longitud_cad'] * coeficient / 1000.0, 3) or 0,
                cable['seccio'],
                round(
                    (cable['intensitat_admisible'] * int(linia['voltatge']) *
                     math.sqrt(3))/1000, 3)
            ]

            output_q.put(output)
            input_q.task_done()
        except Exception as e:
            print "\nERROR DINS DEL WHILE\n"
            print "{}".format(e)


def progress(total, input_q):
    """Rendering del progressbar de l'informe.
    """
    widgets = ['CNMC INVENTARI BT informe: ', Percentage(), ' ',
               Bar(), ' ', ETA()]
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
    sequence += O.GiscedataBtElement.search(search_params)
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
    search_params = [('baixa', '=', 1)]
    trams_indef = O.GiscedataBtElement.search(search_params)
    if trams_indef:
        long_cad = 0
        for tram in O.GiscedataBtElement.read(trams_indef, ['longitud_cad']):
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