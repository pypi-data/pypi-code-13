#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
INVENTARI DE CNMC
"""

import sys
import os
import multiprocessing
import pprint
from datetime import datetime
from optparse import OptionGroup, OptionParser
import csv
import math
import tempfile
import base64
import csv

from libcnmc1048.loop import OOOP
from libcnmc1048 import __version__
from libcnmc1048 import cnmc_inventari
from progressbar import ProgressBar, ETA, Percentage, Bar

N_PROC = min(int(os.getenv('N_PROC', multiprocessing.cpu_count())),
             multiprocessing.cpu_count())
QUIET = False
INTERACTIVE = True

def tractar_linies(pla_inversions_xml, arxiucsvlinies):
    for row in arxiucsvlinies:
        linia = cnmc_inventari.Linea()

        identificador = row[0]
        cini = row[1]
        origen = row[2]
        destino = row[3]
        codigo_tipo_linea = row[4]
        codigo_ccaa_1 = row[5]
        codigo_ccaa_2 = row[6]
        participacion = row[7]
        fecha_aps = row[8]
        fecha_baja = row[9]
        numero_circuitos = row[10]
        numero_conductores = row[11]
        longitud = row[12]
        seccion = row[13]
        capacidad = row[14]

        linia.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'origen': '%s' % origen or ' ',
            'destino': '%s' % destino or ' ',
            'codigo_tipo_linea': '%s' % codigo_tipo_linea,
            'codigo_ccaa_1': '%s' % codigo_ccaa_1,
            'codigo_ccaa_2': '%s' % codigo_ccaa_2,
            'participacion': '%s' % participacion,
            'fecha_aps': '%s' % fecha_aps or ' ',
            'fecha_baja': '%s' % fecha_baja or ' ',
            'numero_circuitos': '%s' % numero_circuitos,
            'numero_conductores': '%s' % numero_conductores,
            'longitud': '%s' % longitud,
            'seccion': '%s' % seccion,
            'capacidad': '%s' % capacidad
        })
        pla_inversions_xml.linea.append(linia)


def tractar_sub(pla_inversions_xml, arxiucsvsub):
    for row in arxiucsvsub:
        sub = cnmc_inventari.Subestacion()

        identificador = row[0]
        cini = row[1]
        denominacion = row[2]
        codigo_tipo_posicion = row[3]
        codigo_ccaa = row[4]
        participacion = row[5]
        fecha_aps = row[6]
        fecha_baja = row[7]
        posiciones = row[8]

        sub.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'denominacion': '%s' % denominacion or ' ',
            'codigo_tipo_posicion': '%s' % codigo_tipo_posicion,
            'codigo_ccaa': '%s' % codigo_ccaa,
            'participacion': '%s' % participacion,
            'fecha_aps': '%s' % fecha_aps or ' ',
            'fecha_baja': '%s' % fecha_baja or ' ',
            'posiciones': '%s' % posiciones,
        })
        pla_inversions_xml.linea.append(sub)


def tractar_pos(pla_inversions_xml, arxiucsvpos):
    for row in arxiucsvpos:
        pos = cnmc_inventari.Posicion()

        identificador = row[0]
        cini = row[1]
        denominacion = row[2]
        codigo_tipo_posicion = row[3]
        codigo_ccaa = row[4]
        participacion = row[5]
        fecha_aps = row[6]
        fecha_baja = row[7]

        pos.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'denominacion': '%s' % denominacion or ' ',
            'codigo_tipo_posicion': '%s' % codigo_tipo_posicion,
            'codigo_ccaa': '%s' % codigo_ccaa,
            'participacion': '%s' % participacion,
            'fecha_aps': '%s' % fecha_aps or ' ',
            'fecha_baja': '%s' % fecha_baja or ' ',
        })
        pla_inversions_xml.linea.append(pos)


def tractar_maq(pla_inversions_xml, arxiucsvmaq):
    for row in arxiucsvmaq:
        maq = cnmc_inventari.Maquina()

        identificador = row[0]
        cini = row[1]
        denominacion = row[2]
        codigo_tipo_maquina = row[3]
        codigo_zona = row[4]
        codigo_ccaa = row[5]
        participacion = row[6]
        fecha_aps = row[7]
        fecha_baja = row[8]
        capacidad = row[9]

        maq.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'denominacion': '%s' % denominacion or ' ',
            'codigo_tipo_posicion': '%s' % codigo_tipo_maquina,
            'codigo_zona': '%s' % codigo_zona,
            'codigo_ccaa': '%s' % codigo_ccaa,
            'participacion': '%s' % participacion,
            'fecha_aps': '%s' % fecha_aps or ' ',
            'fecha_baja': '%s' % fecha_baja or ' ',
            'capacidad': '%s' % capacidad,
        })
        pla_inversions_xml.linea.append(maq)


def tractar_desp(pla_inversions_xml, arxiucsvdesp):
    for row in arxiucsvdesp:
        despt = cnmc_inventari.Despacho()

        identificador = row[0]
        cini = row[1]
        denominacion = row[2]
        anyo_ps = row[3]
        vai = row[4]

        despt.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'denominacion': '%s' % denominacion or ' ',
            'anyo_ps': '%s' % anyo_ps,
            'vai': '%s' % vai,
        })
        pla_inversions_xml.linea.append(despt)


def tractar_fia(pla_inversions_xml, arxiucsvfia):
    for row in arxiucsvfia:
        despt = cnmc_inventari.Fiabilidad()

        identificador = row[0]
        cini = row[1]
        denominacion = row[2]
        codigo_tipo_inst = row[3]
        codigo_ccaa = row[4]
        fecha_aps = row[5]
        fecha_baja = row[6]

        despt.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'denominacion': '%s' % denominacion or ' ',
            'codigo_tipo_inst': '%s' % codigo_tipo_inst or ' ',
            'codigo_ccaa': '%s' % codigo_ccaa,
            'fecha_aps': '%s' % fecha_aps or ' ',
            'fecha_baja': '%s' % fecha_baja or ' ',
        })
        pla_inversions_xml.linea.append(despt)

def tractar_trans(pla_inversions_xml, arxiucsvtrans):
    for row in arxiucsvtrans:
        trans = cnmc_inventari.Transformacion()

        identificador = row[0]
        cini = row[1]
        denominacion = row[2]
        codigo_tipo_ct = row[3]
        codigo_ccaa = row[4]
        participacion = row[5]
        fecha_aps = row[6]
        fecha_baja = row[7]

        trans.feed({
            'identificador': '%s' % identificador or ' ',
            'cini': '%s' % cini or ' ',
            'denominacion': '%s' % denominacion or ' ',
            'codigo_tipo_ct': '%s' % codigo_tipo_ct or ' ',
            'codigo_ccaa': '%s' % codigo_ccaa,
            'participacion': '%s' % participacion,
            'fecha_aps': '%s' % fecha_aps or ' ',
            'fecha_baja': '%s' % fecha_baja or ' ',
        })
        pla_inversions_xml.linea.append(trans)


def main(codi_r1, csvlineaat, csvlineabt, csvsub, csvpos, csvmaq, csvdesp,
         csvfia, csvtrans, file_out):
    """ Funció principal del programa """
    #creo l'XML final
    arxiuxml = open(file_out, 'wb')
    start = datetime.now()

    pla_inversio_xml = cnmc_inventari.Empresa(codi_r1)

    # Carrega dels fitxers CSV LAT
    arxiucsvlineaat = csv.reader(open(csvlineaat), delimiter=';')
    tractar_linies(pla_inversio_xml, arxiucsvlineaat)

    # Carrega dels fitxers CSV LBT
    arxiucsvlineabt = csv.reader(open(csvlineabt), delimiter=';')
    tractar_linies(pla_inversio_xml, arxiucsvlineabt)

    # Carrega dels fitxers CSV subestacions
    arxiucsvsub = csv.reader(open(csvsub), delimiter=';')
    tractar_sub(pla_inversio_xml, arxiucsvsub)

    # Carrega dels fitxers CSV subestacions
    arxiucsvpos = csv.reader(open(csvpos), delimiter=';')
    tractar_pos(pla_inversio_xml, arxiucsvpos)

    # Carrega dels fitxers CSV maquines
    arxiucsvmaq = csv.reader(open(csvmaq), delimiter=';')
    tractar_maq(pla_inversio_xml, arxiucsvmaq)

    # Carrega dels fitxers CSV despatxos
    arxiucsvdesp = csv.reader(open(csvdesp), delimiter=';')
    tractar_desp(pla_inversio_xml, arxiucsvdesp)

    # Carrega dels fitxers CSV fiabilitat
    arxiucsvfia = csv.reader(open(csvfia), delimiter=';')
    tractar_fia(pla_inversio_xml, arxiucsvfia)

    # Carrega dels fitxers CSV transformadors
    arxiucsvtrans = csv.reader(open(csvtrans), delimiter=';')
    tractar_trans(pla_inversio_xml, arxiucsvtrans)

    pla_inversio_xml.set_xml_encoding('iso-8859-1')
    pla_inversio_xml.build_tree()
    arxiuxml.write(str(pla_inversio_xml))

    if not QUIET:
        sys.stderr.write("Time Elapsed: %s\n" % (datetime.now() - start))
        sys.stderr.flush()


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
        parser.add_option("-r", "--R1", dest="r1",
                          help="Codi R1")
        parser.add_option("-l", "--Liniesat", dest="liniesat",
                          help="Fitxers CSV de linies AT")
        parser.add_option("-b", "--Liniesbt", dest="liniesbt",
                          help="Fitxers CSV de linies BT")
        parser.add_option("-e", "--Subestacions", dest="subestacions",
                          help="Fitxers CSV de subestacions")
        parser.add_option("-c", "--Posicions", dest="posicions",
                          help="Fitxers CSV de posicions")
        parser.add_option("-m", "--Maquines", dest="maquinas",
                          help="Fitxers CSV de maquines")
        parser.add_option("-x", "--Despatxos", dest="despatxos",
                          help="Fitxers CSV de despatxos")
        parser.add_option("-f", "--Fiabilitat", dest="fiabilidad",
                          help="Fitxers CSV de fiabilitat")
        parser.add_option("-t", "--Transformacio", dest="transformacion",
                          help="Fitxers CSV de transformacio")

        group = OptionGroup(parser, "Server options")
        group.add_option("-s", "--server", dest="server",
                         default="http://localhost",
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
        if not options.fout:
            parser.error("Es necessita indicar un nom de fitxer")
        if not options.r1:
            parser.error("Es necessita indicar el codi R1")
        if not options.liniesat:
            parser.error("Es necessita determinar el CSV de AT")
        if not options.liniesbt:
            parser.error("Es necessita determinar el CSV de BT")
        if not options.subestacions:
            parser.error("Es necessita determinar el CSV de Subestacions")
        if not options.posicions:
            parser.error("Es necessita determinar el CSV de Posicions")
        if not options.maquinas:
            parser.error("Es necessita determinar el CSV de Màquines")
        if not options.despatxos:
            parser.error("Es necessita determinar el CSV de Despatxos")
        if not options.fiabilidad:
            parser.error("Es necessita determinar el CSV de Fiabilitat")
        if not options.transformacion:
            parser.error("Es necessita determinar el CSV de Transformadors")

        O = OOOP(dbname=options.database, user=options.user,
                 pwd=options.password, port=int(options.port),
                 uri=options.server)

        main(options.r1, options.liniesat, options.liniesbt,
             options.subestacions, options.posicions, options.maquinas,
             options.despatxos, options.fiabilidad, options.transformacion,
             options.fout)

    except KeyboardInterrupt:
	    pass
