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
from collections import namedtuple
import functools
import csv
import math

from libcnmc1048.loop import OOOP
from libcnmc1048 import __version__
from libcnmc1048 import cnmc_pla_inversio
from progressbar import ProgressBar, ETA, Percentage, Bar

N_PROC = min(int(os.getenv('N_PROC', multiprocessing.cpu_count())),
             multiprocessing.cpu_count())
QUIET = False
INTERACTIVE = True


def default_values(value, default):
    if not value:
        return default
    return value


def make_csv(data, fields):
    return ';'.join([data.get(k, '') for k in fields])


def fix_false(data):
    newdata = data.copy()
    for k, v in newdata.iteritems():
        if isinstance(v, bool) and not v:
            newdata[k] = ''
    return newdata


def get_municipi_codi(id_municipi):
    if id_municipi:
        vals = O.ResMunicipi.read(id_municipi[0], ['ine', 'dc'])
        return '%s-%s-%s' % (vals['ine'][0:2], vals['ine'][2:], vals['dc'])
    return '00-000-00'


def get_comunitat_autonoma_codi(id_comunitat):
    if id_comunitat:
        return O.ResComunitat_autonoma.read(id_comunitat[0], ['codi'])['codi']
    return '00'


def tractar_resumen_agr(pla_inversions_xml, resumens):
    fields = list(cnmc_pla_inversio.Resumen._sort_order)
    fields = ['periodo'] +fields
    fields = list(fields)
    res_csv = []
    for resumen_dades in resumens:
        resumen = cnmc_pla_inversio.Resumen(resumen_dades['anyo'])
        resumen_dades = fix_false(resumen_dades)
        dades = {
            'pib': '%s' % resumen_dades['pib'],
            'pib_prev': '%s' % resumen_dades['pib_prev'],
            'limite': '%s' % resumen_dades['limit'],
            'incr_demanda': '%s' % resumen_dades['inc_demanda'],
            'limite_empresa': '%s' % resumen_dades['limit_empresa'],
            'incr_demanda_empresa': '%s' % resumen_dades['inc_demanda_empresa'],
            'vpi_superado': '%s' % default_values(resumen_dades['vpi_sup'], 'no'),
            'volumen_total': '%s' % resumen_dades['volum_total_inv'],
            'ayudas': '%s' % resumen_dades['ajudes_prev'],
            'financiacion': '%s' % resumen_dades['financiacio'],
            'n_proyectos': '%s' % resumen_dades['n_projectes'],
            'vpo_bt': '%s' % resumen_dades['vpi_bt'],
            'inv_ccaa': '%s' % default_values(resumen_dades['inv_ccaa'], '00'),
            'inf_ccaa': '%s' % default_values(resumen_dades['inf_ccaa'], 'no'),
        }
        resumen.feed(dades)
        dades['periodo'] = '%s' % resumen_dades['anyo']
        res_csv.append(make_csv(dades, fields))

        pla_inversions_xml.resumenes.append(resumen)

    return '\n'.join(res_csv)

def tractar_resumen(pla_inversions_xml, resumens):
    fields = cnmc_pla_inversio.Resumen._sort_order
    res_csv = []
    for resumen_dades in resumens:
        resumen = cnmc_pla_inversio.Resumen(resumen_dades['anyo'])
        resumen_dades = fix_false(resumen_dades)
        dades = {
            'pib': '%s' % resumen_dades['pib'],
            'pib_prev': '%s' % resumen_dades['pib_prev'],
            'limite': '%s' % resumen_dades['limit'],
            'incr_demanda': '%s' % resumen_dades['inc_demanda'],
            'limite_empresa': '%s' % resumen_dades['limit_empresa'],
            'incr_demanda_empresa': '%s' % resumen_dades['inc_demanda_empresa'],
            'vpi_superado': '%s' % default_values(resumen_dades['vpi_sup'], 'no'),
            'volumen_total': '%s' % resumen_dades['volum_total_inv'],
            'ayudas': '%s' % resumen_dades['ajudes_prev'],
            'financiacion': '%s' % resumen_dades['financiacio'],
            'n_proyectos': '%s' % resumen_dades['n_projectes'],
            'vpo_bt': '%s' % resumen_dades['vpi_bt'],
            'inv_ccaa': '%s' % default_values(resumen_dades['inv_ccaa'], '00'),
            'inf_ccaa': '%s' % default_values(resumen_dades['inf_ccaa'], 'no'),
        }
        resumen.feed(dades)
        res_csv.append(make_csv(dades, fields))

        pla_inversions_xml.resumenes.append(resumen)

    return '\n'.join(res_csv)


def tractar_instalaciones_tension(pla_inversions_xml, insts_tension_id):
    fields = cnmc_pla_inversio.InstalacionTension._sort_order
    res_csv = []
    for inst_tension_dades in O.GiscedataCnmcAltres.read(insts_tension_id, []):
        inst_tension = cnmc_pla_inversio.InstalacionTension()
        inst_tension_dades = fix_false(inst_tension_dades)
        dades = {'codigo_proyecto': '%s' % inst_tension_dades['codi'],
            'cini': '%s' % inst_tension_dades['cini'],
            'codigo_tipo_instalacion': '%s' % inst_tension_dades['codi_tipus_inst'],
            'tension': '%s' % inst_tension_dades['tensio'],
            'financiacion': '%s' % inst_tension_dades['inv_financiada'],
            'ayudas': '%s' % inst_tension_dades['ajudes'],
            'volumen_total': '%s' % inst_tension_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % inst_tension_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % inst_tension_dades['any_apm'],
            'numero_unidades': '%s' % inst_tension_dades['num_unitats'],
            'suma_unidades': '%s' % inst_tension_dades['sum_num_unitats'],
            }
        inst_tension.feed(dades)
        res_csv.append(make_csv(dades, fields))

        pla_inversions_xml.instalaciones_tension.append(inst_tension)
    return '\n'.join(res_csv)


def tractar_transformacio(pla_inversions_xml, transformacion_id):
    res_csv = []
    for transformacion_dades in O.GiscedataCnmcCt.read(transformacion_id, []):
        transformacion = cnmc_pla_inversio.Transformacion()
        transformacion_dades = fix_false(transformacion_dades)
        dades = {'codigo_proyecto': '%s' % transformacion_dades['codi'],
            'finalidad': '%s' % transformacion_dades['finalitat'],
            'identificador': '%s' % transformacion_dades['id_instalacio'],
            'denominacion': '%s' % transformacion_dades['denominacio'],
            'cini': '%s' % transformacion_dades['cini'],
            'codigo_tipo_instalacion': '%s' % transformacion_dades['codi_tipus_inst'],
            'financiacion': '%s' % transformacion_dades['inv_financiada'],
            'ayudas': '%s' % transformacion_dades['ajudes'],
            'volumen_total': '%s' % transformacion_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % transformacion_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % transformacion_dades['any_apm'],
            'potencia_instalada_prev': '%s' % transformacion_dades['pot_inst_prev'],
            'codigo_comunidad': '%s' % get_comunitat_autonoma_codi(
                   transformacion_dades['ccaa']),
            'municipio_afectado': '%s' % get_municipi_codi(
                transformacion_dades['municipi'])
            }
        transformacion.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Transformacion._sort_order
        ))
        pla_inversions_xml.transformacion.append(transformacion)
    return '\n'.join(res_csv)


def tractar_fiabilidad(pla_inversions_xml, fiabilidads_id):
    res_csv = []
    for fiabilidad_dades in O.GiscedataCnmcFiabilitat.read(fiabilidads_id, []):
        fiabilidad = cnmc_pla_inversio.Fiabilidad()
        fiabilidad_dades = fix_false(fiabilidad_dades)
        dades = {'codigo_proyecto': '%s' % fiabilidad_dades['codi'],
            'finalidad': '%s' % fiabilidad_dades['finalitat'],
            'identificador': '%s' % fiabilidad_dades['id_instalacio'],
            'denominacion': '%s' % fiabilidad_dades['denominacio'],
            'cini': '%s' % fiabilidad_dades['cini'],
            'codigo_tipo_instalacion': '%s' % fiabilidad_dades['codi_tipus_inst'],
            'financiacion': '%s' % fiabilidad_dades['inv_financiada'],
            'ayudas': '%s' % fiabilidad_dades['ajudes'],
            'volumen_total': '%s' % fiabilidad_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % fiabilidad_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % fiabilidad_dades['any_apm'],
            'potencia_instalada_prev': '%s' % fiabilidad_dades['pot_inst_prev'],
            'codigo_comunidad': '%s' % get_comunitat_autonoma_codi(
                   fiabilidad_dades['ccaa']),
            'municipio_afectado': '%s' % get_municipi_codi(
                fiabilidad_dades['municipi'])
            }
        fiabilidad.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Fiabilidad._sort_order
        ))
        pla_inversions_xml.fiabilidad.append(fiabilidad)
    return '\n'.join(res_csv)


def tractar_despatxos(pla_inversions_xml, despatxos_id):
    res_csv = []
    for despatx_dades in O.GiscedataCnmcDespatx.read(despatxos_id, []):
        despatx = cnmc_pla_inversio.Despacho()
        despatx_dades = fix_false(despatx_dades)
        dades = {'codigo_proyecto': '%s' % despatx_dades['codi'],
            'finalidad': '%s' % despatx_dades['finalitat'],
            'identificador': '%s' % despatx_dades['id_instalacio'],
            'denominacion': '%s' % despatx_dades['denominacio'],
            'cini': '%s' % despatx_dades['cini'],
            'codigo_tipo_instalacion': '%s' % despatx_dades['codi_tipus_inst'],
            'financiacion': '%s' % despatx_dades['inv_financiada'],
            'ayudas': '%s' % despatx_dades['ajudes'],
            'volumen_total': '%s' % despatx_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % despatx_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % despatx_dades['any_apm'],
            }
        despatx.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Despacho._sort_order
        ))
        pla_inversions_xml.despachos.append(despatx)
    return '\n'.join(res_csv)


def tractar_maquines(pla_inversions_xml, maquinas_id):
    res_csv = []
    for maquina_dades in O.GiscedataCnmcMaquines.read(maquinas_id, []):
        maquina = cnmc_pla_inversio.Maquina()
        maquina_dades = fix_false(maquina_dades)
        dades = {'codigo_proyecto': '%s' % maquina_dades['codi'],
            'finalidad': '%s' % maquina_dades['finalitat'],
            'identificador': '%s' % maquina_dades['id_instalacio'],
            'denominacion': '%s' % maquina_dades['denominacio'],
            'cini': '%s' % maquina_dades['cini'],
            'codigo_tipo_instalacion': '%s' % maquina_dades['codi_tipus_inst'],
            'financiacion': '%s' % maquina_dades['inv_financiada'],
            'ayudas': '%s' % maquina_dades['ajudes'],
            'volumen_total': '%s' % maquina_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % maquina_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % maquina_dades['any_apm'],
            'potencia_instalada_prev': '%s' % maquina_dades['pot_inst_prev'],
            'codigo_comunidad': '%s' % get_comunitat_autonoma_codi(
                   maquina_dades['ccaa']),
            'municipio_afectado': '%s' % get_municipi_codi(
                maquina_dades['municipi'])
            }
        maquina.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Maquina._sort_order
        ))
        pla_inversions_xml.maquinas.append(maquina)
    return '\n'.join(res_csv)


def tractar_posicions(pla_inversions_xml, posicions_id):
    res_csv = []
    for posicio_dades in O.GiscedataCnmcPosicions.read(posicions_id, []):
        posicio = cnmc_pla_inversio.Posicion()
        posicio_dades = fix_false(posicio_dades)
        dades = {'codigo_proyecto': '%s' % posicio_dades['codi'],
            'finalidad': '%s' % posicio_dades['finalitat'],
            'identificador': '%s' % posicio_dades['id_instalacio'],
            'denominacion': posicio_dades['denominacio'],
            'cini': '%s' % posicio_dades['cini'],
            'codigo_tipo_instalacion': '%s' % posicio_dades['codi_tipus_inst'],
            'financiacion': '%s' % posicio_dades['inv_financiada'],
            'ayudas': '%s' % posicio_dades['ajudes'],
            'volumen_total': '%s' % posicio_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % posicio_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % posicio_dades['any_apm'],
            'codigo_comunidad': '%s' % get_comunitat_autonoma_codi(
                   posicio_dades['ccaa']),
            'municipio_afectado': '%s' % get_municipi_codi(
                posicio_dades['municipi'])
            }
        posicio.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Posicion._sort_order
        ))
        pla_inversions_xml.posiciones.append(posicio)
    return '\n'.join(res_csv)


def tractar_linies(pla_inversions_xml, linies_id):
    res_csv = []
    for linia_dades in O.GiscedataCnmcLinies.read(linies_id, []):
        linia = cnmc_pla_inversio.Linea()
        linia_dades = fix_false(linia_dades)
        dades = {'codigo_proyecto': '%s' % linia_dades['codi'],
            'finalidad': '%s' % linia_dades['finalitat'],
            'identificador': '%s' % linia_dades['id_instalacio'],
            'cini': '%s' % linia_dades['cini'],
            'codigo_tipo_instalacion': '%s' % linia_dades['codi_tipus_inst'],
            'origen': '%s' % linia_dades['origen'],
            'destino': '%s' % linia_dades['desti'],
            'financiacion': '%s' % linia_dades['inv_financiada'],
            'ayudas': '%s' % linia_dades['ajudes'],
            'volumen_total': '%s' % linia_dades['vol_total_inv'],
            'vpo_retribuible': '%s' % linia_dades['vpi_retri'],
            'anyo_previsto_ps': '%s' % linia_dades['any_apm'],
            'longitud_prevista': '%s' % linia_dades['long_total'],
            'codigo_comunidad': '%s' % get_comunitat_autonoma_codi(
                   linia_dades['ccaa']),
            }
        linia.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Linea._sort_order
        ))
        pla_inversions_xml.lineas.append(linia)
    return '\n'.join(res_csv)


def tractar_projectes(pla_inversions_xml, projectes_id):
    res_csv = []
    for projecte_dades in O.GiscedataCnmcProjectes.read(projectes_id, []):
        projecte = cnmc_pla_inversio.Proyecto()
        projecte_dades = fix_false(projecte_dades)
        dades = {'codigo_proyecto': '%s' % projecte_dades['codi'],
               'nombre': '%s' % projecte_dades['name'],
               'codigo_comunidad': get_comunitat_autonoma_codi(
                   projecte_dades['ccaa']),
               'memoria': '%s' % default_values(projecte_dades['memoria'], ''),
               }
        projecte.feed(dades)
        res_csv.append(make_csv(
            dades, cnmc_pla_inversio.Proyecto._sort_order
        ))
        pla_inversions_xml.proyectos.append(projecte)
    return '\n'.join(res_csv)


OutFileInfo = namedtuple(
    'OutFileInfo', ['prefix', 'filename', 'values', 'function']
)


def make_files(zip_out, items):
    for item in items:
        assert isinstance(item, OutFileInfo)
        zip_out.writestr(
            '_'.join([item.prefix, item.filename]),
            item.function(item.values).encode('utf-8')
        )


def main(any_pla, file_out):
    """Funció principal del programa"""
    import zipfile
    zip_out = zipfile.ZipFile(file_out, 'w')
    search_params = [('anyo', '=', any_pla)]
    pla_inversio = O.GiscedataCnmcPla_inversio.search(search_params)
    start = datetime.now()
    if not QUIET or INTERACTIVE:
            sys.stderr.write("Filtres utilitzats:\n")
            pprint.pprint(search_params, sys.stderr)
            sys.stderr.write("S'han trobat %s plans d'inversió.\n" % len(pla_inversio))
            sys.stderr.flush()

    if pla_inversio and len(pla_inversio) == 1:
        pla_inversio_id = pla_inversio[0]
        pla_inversio = O.GiscedataCnmcPla_inversio.read(pla_inversio_id,
                                                        ['codi'])
        pla_inversio_xml = cnmc_pla_inversio.Empresa(pla_inversio['codi'])
        resums_any_ids = O.GiscedataCnmcResum_any.search(
            [('pla_inversio', '=', pla_inversio_id)], 0, 0, 'anyo')
        resumenes = {}
        proyectos = {}
        lineas = {}
        posiciones = {}
        maquinas = {}
        despachos = {}
        fiabilidad = {}
        transformacion = {}
        instalaciones_tension = {}
        if not QUIET:
            sys.stderr.write("^Starting process ... \n")
            sys.stderr.write("^Export resums\n")
            sys.stderr.flush()
            widgets = [Percentage(), ' ', Bar(), ' ', ETA()]
            pbar = ProgressBar(widgets=widgets,
                               maxval=len(resums_any_ids)).start()
            done = 0
        inici = 3000
        final = 0

        def process_method(method):
            return functools.partial(method, pla_inversio_xml)

        for resum in O.GiscedataCnmcResum_any.read(resums_any_ids, []):
            if not QUIET:
                done += 1

            inici = min(resum['anyo'], inici)
            final = max(resum['anyo'], final)

            if not QUIET:
                pbar.update(done)

            resumenes.setdefault(resum['anyo'], [])
            resumenes[resum['anyo']].append(resum)

            proyectos.setdefault(resum['anyo'], [])
            proyectos[resum['anyo']] += resum['projectes']

            lineas.setdefault(resum['anyo'], [])
            lineas[resum['anyo']] += resum['linies']

            posiciones.setdefault(resum['anyo'], [])
            posiciones[resum['anyo']] += resum['posicions']

            maquinas.setdefault(resum['anyo'], [])
            maquinas[resum['anyo']] += resum['maquines']

            despachos.setdefault(resum['anyo'], [])
            despachos[resum['anyo']] += resum['despatxos']

            fiabilidad.setdefault(resum['anyo'], [])
            fiabilidad[resum['anyo']] += resum['fiabilitats']

            transformacion.setdefault(resum['anyo'], [])
            transformacion[resum['anyo']] += resum['cts']

            instalaciones_tension.setdefault(resum['anyo'], [])
            instalaciones_tension[resum['anyo']] += resum['altres']

        resumen_agr = sum(resumenes.values(), [])
        proyectos_agr = sum(proyectos.values(), [])
        lineas_agr = sum(lineas.values(), [])
        posiciones_agr = sum(posiciones.values(), [])
        maquinas_agr = sum(maquinas.values(), [])
        despachos_agr = sum(despachos.values(), [])
        fiabilidad_agr = sum(fiabilidad.values(), [])
        transformacion_agr = sum(transformacion.values(), [])
        instalaciones_tension_agr = sum(instalaciones_tension.values(), [])

        r1_code = pla_inversio['codi']
        prefix_agr = 'Plan{0}-{1}_R1-{2}'.format(inici, final, r1_code)
        prefix = 'Plan{0}_R1-{1}'.format(inici, r1_code)

        to_process = [
            OutFileInfo(
                prefix_agr,
                'resumen.txt',
                resumen_agr,
                process_method(tractar_resumen_agr)
            ),
            OutFileInfo(
                prefix,
                'resumen.txt',
                resumenes[inici],
                process_method(tractar_resumen)
            ),
            OutFileInfo(
                prefix_agr,
                'Proyecto_36.txt',
                proyectos_agr,
                process_method(tractar_projectes)
            ),
            OutFileInfo(
                prefix,
                'Proyecto_36.txt',
                proyectos[inici],
                process_method(tractar_projectes)
            ),
            OutFileInfo(
                prefix_agr,
                'Lineas_36.txt',
                lineas_agr,
                process_method(tractar_linies)
            ),
            OutFileInfo(
                prefix,
                'Lineas_36.txt',
                lineas[inici],
                process_method(tractar_linies)
            ),
            OutFileInfo(
                prefix_agr,
                'Posiciones_36.txt',
                posiciones_agr,
                process_method(tractar_posicions)
            ),
            OutFileInfo(
                prefix,
                'Posiciones_36.txt',
                posiciones[inici],
                process_method(tractar_posicions)
            ),
            OutFileInfo(
                prefix_agr,
                'Maquinas_36.txt',
                maquinas_agr,
                process_method(tractar_maquines)
            ),
            OutFileInfo(
                prefix,
                'Maquinas_36.txt',
                maquinas[inici],
                process_method(tractar_maquines)
            ),
            OutFileInfo(
                prefix_agr,
                'Despachos_36.txt',
                despachos_agr,
                process_method(tractar_despatxos)
            ),
            OutFileInfo(
                prefix,
                'Despachos_36.txt',
                despachos[inici],
                process_method(tractar_despatxos)
            ),
            OutFileInfo(
                prefix_agr,
                'Equipos_36.txt',
                fiabilidad_agr,
                process_method(tractar_fiabilidad)
            ),
            OutFileInfo(
                prefix,
                'Equipos_36.txt',
                fiabilidad[inici],
                process_method(tractar_fiabilidad)
            ),
            OutFileInfo(
                prefix_agr,
                'Centros_36.txt',
                transformacion_agr,
                process_method(tractar_transformacio)
            ),
            OutFileInfo(
                prefix,
                'Centros_36.txt',
                transformacion[inici],
                process_method(tractar_transformacio)
            ),
            OutFileInfo(
                prefix_agr,
                'Resto_inferior_36.txt',
                instalaciones_tension_agr,
                process_method(tractar_instalaciones_tension)
            ),
            OutFileInfo(
                prefix,
                'Resto_inferior_36.txt',
                instalaciones_tension[inici],
                process_method(tractar_instalaciones_tension)
            ),

        ]

        make_files(zip_out, to_process)

        pla_inversio_xml.set_xml_encoding('iso-8859-1')
        pla_inversio_xml.build_tree()
        zip_out.writestr('{0}.xml'.format(prefix), str(pla_inversio_xml))
        zip_out.close()

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
        parser.add_option("-a", "--any", dest="any_pla",
                          help="Any del pla d'inversió")

        group = OptionGroup(parser, "Server options")
        group.add_option("-s", "--server", dest="server", default="http://localhost",
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
        if not options.any_pla:
            parser.error("Es necessita indicar l'any del pla d'inversió")

        O = OOOP(dbname=options.database, user=options.user,
                 pwd=options.password, port=int(options.port),
                 uri=options.server)

        main(options.any_pla, options.fout)

    except KeyboardInterrupt:
        pass
