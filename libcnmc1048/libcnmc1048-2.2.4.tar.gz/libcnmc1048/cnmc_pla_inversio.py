# -*- coding: utf-8 -*-

from libcomxml.core import XmlModel, XmlField


class Resumen(XmlModel):
    _sort_order = ('pib', 'pib_prev', 'limite', 'incr_demanda',
                   'limite_empresa', 'incr_demanda_empresa', 'vpi_superado',
                   'volumen_total', 'ayudas', 'financiacion', 'n_proyectos',
                   'vpo_bt', 'inv_ccaa', 'inf_ccaa')
    
    def __init__(self, any_resum):
        tag = 'RESUMEN_%s' % any_resum
        self.resumen = XmlField(tag)
        self.pib = XmlField('PIB')
        self.pib_prev = XmlField('PIB_PREVISTO')
        self.limite = XmlField('LIMITE')
        self.incr_demanda = XmlField('INCR_DEMANDA')
        self.limite_empresa = XmlField('LIMITE_EMPRESA')
        self.incr_demanda_empresa = XmlField('INCR_DEMANDA_EMPRESA')
        self.vpi_superado = XmlField('VPI_SUPERADO')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.ayudas = XmlField('AYUDAS')
        self.financiacion = XmlField('FINANCIACION')
        self.n_proyectos = XmlField('N_PROYECTOS')
        self.vpo_bt = XmlField('VPO_BT')
        self.inv_ccaa = XmlField('INV_CCAA')
        self.inf_ccaa = XmlField('INF_CCAA')

        super(Resumen, self).__init__(tag, 'resumen') 


class Proyecto(XmlModel):
    _sort_order = ('codigo_proyecto', 'nombre', 'codigo_comunidad','memoria')

    def __init__(self):
        self.proyectos = XmlField('PROYECTOS')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.nombre = XmlField('NOMBRE')
        self.codigo_comunidad = XmlField('CODIGO_COMUNIDAD')
        self.memoria = XmlField('MEMORIA')

        super(Proyecto, self).__init__('PROYECTOS', 'proyectos')


class Linea(XmlModel):
    _sort_order = ('codigo_proyecto', 'finalidad', 'identificador', 'cini',
                   'codigo_tipo_instalacion', 'origen', 'destino',
                   'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps', 'longitud_prevista',
                   'codigo_comunidad')

    def __init__(self):
        self.lineas = XmlField('LINEAS')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.finalidad = XmlField('FINALIDAD')
        self.identificador = XmlField('IDENTIFICADOR') 
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.origen = XmlField('ORIGEN')
        self.destino = XmlField('DESTINO')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')
        self.longitud_prevista = XmlField('LONGITUD_PREVISTA')
        self.codigo_comunidad = XmlField('CODIGO_COMUNIDAD')

        super(Linea, self).__init__('LINEAS', 'lineas')



class Posicion(XmlModel):
    _sort_order = ('codigo_proyecto', 'finalidad', 'identificador',
                   'denominacion', 'cini', 'codigo_tipo_instalacion',
                   'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps',
                   'codigo_comunidad', 'municipio_afectado')

    def __init__(self):
        self.posiciones = XmlField('POSICIONES')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.finalidad = XmlField('FINALIDAD')
        self.identificador = XmlField('IDENTIFICADOR') 
        self.denominacion = XmlField('DENOMINACION') 
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')
        self.codigo_comunidad = XmlField('CODIGO_COMUNIDAD')
        self.municipio_afectado = XmlField('MUNICIPIO_AFECTADO')

        super(Posicion, self).__init__('POSICIONES', 'posiciones')


class Maquina(XmlModel):
    _sort_order = ('codigo_proyecto', 'finalidad', 'identificador',
                   'denominacion', 'cini', 'codigo_tipo_instalacion',
                   'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps',
                   'potencia_instalada_prev', 'codigo_comunidad',
                   'municipio_afectado')

    def __init__(self):
        self.maquinas= XmlField('MAQUINAS')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.finalidad = XmlField('FINALIDAD')
        self.identificador = XmlField('IDENTIFICADOR') 
        self.denominacion = XmlField('DENOMINACION') 
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')
        self.potencia_instalada_prev = XmlField('POTENCIA_INSTALADA_PREVISTA')
        self.codigo_comunidad = XmlField('CODIGO_COMUNIDAD')
        self.municipio_afectado = XmlField('MUNICIPIO_AFECTADO')

        super(Maquina, self).__init__('MAQUINAS', 'maquinas')

class Despacho(XmlModel):
    _sort_order = ('codigo_proyecto', 'finalidad', 'identificador',
                   'denominacion', 'cini', 'codigo_tipo_instalacion',
                   'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps',)

    def __init__(self):
        self.despachos= XmlField('DESPACHOS')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.finalidad = XmlField('FINALIDAD')
        self.identificador = XmlField('IDENTIFICADOR') 
        self.denominacion = XmlField('DENOMINACION') 
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')

        super(Despacho, self).__init__('DESPACHOS', 'despachos')

class Fiabilidad(XmlModel):
    _sort_order = ('codigo_proyecto', 'finalidad', 'identificador',
                   'denominacion', 'cini', 'codigo_tipo_instalacion',
                   'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps', 
                   'potencia_instalada_prev', 'codigo_comunidad',
                   'municipio_afectado')

    def __init__(self):
        self.fiabilidad= XmlField('FIABILIDAD')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.finalidad = XmlField('FINALIDAD')
        self.identificador = XmlField('IDENTIFICADOR') 
        self.denominacion = XmlField('DENOMINACION') 
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')
        self.potencia_instalada_prev = XmlField('POTENCIA_INSTALADA_PREVISTA')
        self.codigo_comunidad = XmlField('CODIGO_COMUNIDAD')
        self.municipio_afectado = XmlField('MUNICIPIO_AFECTADO')
        super(Fiabilidad, self).__init__('FIABILIDAD', 'fiabilidad')

class Transformacion(XmlModel):
    _sort_order = ('codigo_proyecto', 'finalidad', 'identificador',
                   'denominacion', 'cini', 'codigo_tipo_instalacion',
                   'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps', 
                   'potencia_instalada_prev', 'codigo_comunidad',
                   'municipio_afectado')

    def __init__(self):
        self.transformacion= XmlField('TRANSFORMACION')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.finalidad = XmlField('FINALIDAD')
        self.identificador = XmlField('IDENTIFICADOR') 
        self.denominacion = XmlField('DENOMINACION') 
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')
        self.potencia_instalada_prev = XmlField('POTENCIA_INSTALADA_PREVISTA')
        self.codigo_comunidad = XmlField('CODIGO_COMUNIDAD')
        self.municipio_afectado = XmlField('MUNICIPIO_AFECTADO')
        super(Transformacion, self).__init__('TRANSFORMACION', 'transformacion')

class InstalacionTension(XmlModel):
    _sort_order = ('codigo_proyecto', 'cini', 'codigo_tipo_instalacion',
                   'tension', 'financiacion', 'ayudas', 'volumen_total',
                   'vpo_retribuible', 'anyo_previsto_ps', 
                   'numero_unidades', 'suma_unidades')

    def __init__(self):
        self.instalaciones_tension= XmlField('INSTALACIONES_TENSION')
        self.codigo_proyecto = XmlField('CODIGO_PROYECTO')
        self.cini = XmlField('CINI')
        self.codigo_tipo_instalacion = XmlField('CODIGO_TIPO_INSTALACION')
        self.tension = XmlField('TENSION')
        self.financiacion = XmlField('FINANCIACION')
        self.ayudas = XmlField('AYUDAS')
        self.volumen_total = XmlField('VOLUMEN_TOTAL')
        self.vpo_retribuible = XmlField('VPO_RETRIBUIBLE')
        self.anyo_previsto_ps = XmlField(u'AÑO_PREVISTO_PS')
        self.numero_unidades = XmlField('NUMERO_UNIDADES')
        self.suma_unidades = XmlField('SUMA_UNIDADES')
        super(InstalacionTension, self).__init__(
           'INSTALACIONES_TENSION','instalaciones_tension')



class Empresa(XmlModel):
    _sort_order = ('root', 'resumenes', 'proyectos', 'lineas', 'posiciones',
                   'maquinas','despachos','fiabilidad', 'transformacion',
                   'instalaciones_tension')
    def __init__(self, codigo=''):
        self.root = XmlField('EMPRESA', attributes={'CODIGO': codigo})
        self.resumenes = []
        self.proyectos = []
        self.lineas = []
        self.posiciones = []
        self.maquinas = []
        self.despachos = []
        self.fiabilidad = []
        self.transformacion = []
        self.instalaciones_tension = []
        super(Empresa, self).__init__('EMPRESA','root')

    def set_codigo(self, codigo):
        self.root.attributes.update({'CODIGO': codigo})
