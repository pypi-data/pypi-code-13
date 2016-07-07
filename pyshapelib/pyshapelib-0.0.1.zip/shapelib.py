#! /usr/bin/env python
# -*- coding: utf-8 -*-
# This file was created automatically by SWIG.
# Modified by wzy.
import os
from itertools import izip
import shapelibc

__version__ = '0.0.1'
__date__ = '2016/07/07'


# ---------------------------------------------------------------------------------
class SHPObject:
    def __init__(self, *args, **kw):
        """shapelib.obj(geom_type, id, parts_coords_list, part_type_list=None, **kw)
        """
        self.this = apply(shapelibc.new_SHPObject, args)
        self.thisown = 1

        # wzy add begin-----------------
        self.precise = None
        self.distol = 0
        for k, v in kw.iteritems():
            exec ('self.%s=v' % k)

        if 360 < abs(args[2][0][0][0]) <= 1296000:
            self.unit = 'S'
        elif 0 <= abs(args[2][0][0][0]) <= 360:
            self.unit = 'D'
        else:
            self.unit = 'M'

        if self.precise is None:
            self.precise = 3 if self.unit == 'S' else 7
            # wzy add end-----------------

    # -------------------------------------------------------------------------
    def __del__(self, lib=shapelibc):
        if self.thisown == 1:
            lib.delete_SHPObject(self)
            self.thisown = 0

    # -------------------------------------------------------------------------
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self.type != other.type or self.count != other.count:
            return False

        # -------------------------------------------------------------
        distol = self.distol
        precise = self.precise

        if distol > 0:
            def pt_dist_chk(c1, c2):
                dis = ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5
                rt = (dis <= distol)
                return rt
        else:
            def pt_dist_chk(c1, c2):
                rt = round(c1[0], precise) == round(c2[0], precise) and round(c1[1],
                                                                              precise) == round(
                    c2[1], precise)
                return rt
        # -------------------------------------------------------------

        coords_a = self.coords()
        coords_b = other.coords()

        if len(coords_a) != len(coords_b):
            return False

        if self.type == POINT:
            coords_a = [coords_a]
            coords_b = [coords_b]

        for part1, part2 in izip(coords_a, coords_b):
            if len(part1) != len(part2):
                return False
            ret = all(pt_dist_chk(a, b) for a, b in izip(part1, part2))
            if not ret:
                return False

        return True

    # -------------------------------------------------------------------------
    def __ne__(self, other):
        return not self == other

    # -------------------------------------------------------------------------
    def __hash__(self):
        precise = self.precise

        if self.type == POINT:
            coords = [self.coords()]
        else:
            coords = self.coords()

        ret = hash(
            tuple(tuple(tuple(round(a, precise) for a in xy[:2]) for xy in p) for p in coords))
        return ret

    # -------------------------------------------------------------------------
    def info(*args):
        """shpobj.info()
        Return (min_list[x,y,z,m], max_list[x,y,z,m]) of shpobj.
        """
        val = apply(shapelibc.SHPObject_extents, args)
        return val

    # -------------------------------------------------------------------------
    def box(*args):
        """shpobj.box()
        Return (minx,miny,maxx,maxy) of shpobj.
        """
        val = apply(shapelibc.SHPObject_extents, args)
        #        if val[0][0] == val[1][0]:
        #            val[0][0] -= 0.000001
        #            val[1][0] += 0.000001
        #        if val[0][1] == val[1][1]:
        #            val[0][1] -= 0.000001
        #            val[1][1] += 0.000001
        return val[0][0], val[0][1], val[1][0], val[1][1]

    # -------------------------------------------------------------------------
    def coords(*args):
        """shpobj.coords()
        Return [part0_list,part1_list,...] of shpobj.
        """
        val = apply(shapelibc.SHPObject_vertices, args)
        return val

    # -------------------------------------------------------------------------
    def coords0(*args):
        """shpobj.coords0()
        Return [(x0, y0), (x1, y1)...] of the first part of shpobj.
        """
        val = apply(shapelibc.SHPObject_vertices, args)
        return val[0]

    # -------------------------------------------------------------------------
    def box_overlaps(self, other):
        """shpobj.box_overlaps(shpobj2)
        Return overlaps ? True : False
        """
        box_1 = self.box()
        box_2 = other.box()
        for i in range(2):
            if box_2[1][i] < box_1[0][i]:
                return False
            if box_1[1][i] < box_2[0][i]:
                return False
        return True

    __setmethods__ = {}

    # -------------------------------------------------------------------------
    def __setattr__(self, name, value):
        if (name == "this") or (name == "thisown"):
            self.__dict__[name] = value
            return
        method = SHPObject.__setmethods__.get(name, None)
        if callable(method):
            return method(self, value)
        self.__dict__[name] = value

    # -------------------------------------------------------------------------
    __getmethods__ = {"type":       shapelibc.SHPObject_type_get, "id": shapelibc.SHPObject_id_get,
                      "count":      shapelibc.SHPObject_count_get,
                      "part_types": shapelibc.SHPObject_parttypes_get}

    # -------------------------------------------------------------------------
    def __getattr__(self, name):
        method = SHPObject.__getmethods__.get(name, None)
        if callable(method):
            return method(self)
        raise AttributeError(name)

    # -------------------------------------------------------------------------
    def __repr__(self):
        return "<C SHPObject instance at %s>" % (self.this,)

    # -------------------------------------------------------------------------
    def __str__(self):
        return 'id=%s, type=%s, count=%s, parts=%s, coords=%s' % (
            self.id, self.type, self.count, len(self.coords()), str(self.coords()))

    # -------------------------------------------------------------------------
    def d2s(self):
        if getattr(self, 'unit', '') == 'S':
            return self
        coords = [self.coords()] if self.type == POINT else self.coords()
        if all(map(lambda x: 1296000 > x > 360, coords[0][0])):
            return self

        def _d2s(xy):
            xy = list(xy)
            xy[0] *= 3600
            xy[1] *= 3600
            return tuple(xy)

        coords2 = tuple(tuple(_d2s(xy) for xy in p) for p in coords)
        obj2 = SHPObject(self.type, self.id, coords2, self.part_types)
        obj2.unit = 'S'
        return obj2

    # -------------------------------------------------------------------------
    def s2d(self):
        if getattr(self, 'unit', '') == 'D':
            return self
        coords = [self.coords()] if self.type == POINT else self.coords()
        if all(map(lambda x: -180 < x < 360, coords[0][0])):
            return self

        def _s2d(xy):
            xy = list(xy)
            xy[0] /= 3600
            xy[1] /= 3600
            return tuple(xy)

        coords2 = tuple(tuple(_s2d(xy) for xy in p) for p in coords)
        obj2 = SHPObject(self.type, self.id, coords2, self.part_types)
        obj2.unit = 'D'
        return obj2

    # -------------------------------------------------------------------------
    def copy(self):
        coords = [self.coords()] if self.type == POINT else self.coords()
        # print self.type, self.id, coords, self.part_types, self.file_path
        obj2 = SHPObject(self.type, self.id, coords, self.part_types)
        return obj2

    def __copy__(self):
        return self.copy()

        # -------------------------------------------------------------------------


# def __deepcopy__(self, visit):
#        new_obj = self.copy()
#        return new_obj
#        new_obj = copy.deepcopy(self)
#        return new_obj

# ---------------------------------------------------------------------------------
class SHPObjectPtr(SHPObject):
    # -------------------------------------------------------------------------
    def __init__(self, this):
        self.this = this
        self.thisown = 0
        self.__class__ = SHPObject


# ---------------------------------------------------------------------------------
class ShapeFile:
    # -------------------------------------------------------------------------
    def __init__(self, *args):
        """shapelib.ShapeFile(file_path, mode='rb'|'rb+')
        Return shphandle.
        """
        self.this = apply(shapelibc.new_ShapeFile, args)
        self.thisown = 1
        self.file_path = args[0]
        self.geom_type = self.precise = self.distol = self.unit = None

    # -------------------------------------------------------------------------
    def __del__(self, lib=shapelibc):
        if self.thisown == 1:
            lib.delete_ShapeFile(self)
            self.thisown = 0

    # -------------------------------------------------------------------------
    def close(*args):
        """shphandle.close()
        It's not neccesary in some cases when the shphandle is out of range.
        """
        val = apply(shapelibc.ShapeFile_close, args)
        return val

    # -------------------------------------------------------------------------
    def clone(self, cloned_shp_path):
        """shphandle.clone(cloned_shp_path)
        Return cloned-shphandle and saved as cloned_shp_path.
        """
        cloned_shp_path = os.path.abspath(cloned_shp_path)
        dir_path = os.path.dirname(cloned_shp_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        return create(cloned_shp_path, self.geom_type, precise=self.precise, distol=self.distol,
                      unit=self.unit)

    # -------------------------------------------------------------------------
    def translate(self, cloned_shp, trans_func=None):
        """shphandle.translate(cloned_shp, trans_func=None)
        Firstly, clone shphandle as cloned_shp, translate every shpobj with trans_func
        and write it into the cloned_shp, and return cloned_shp at last.
        * The cloned_shp can be a shp-path or shphandle.
        * The trans_func can be a function to translate src-shpobj and return des-shpobj.
            If the trans_func is None the function will copy src-shpobj to des-shpobj.

        For example:
            shphandle's path is 'c:\test.shp', the purpose is clone and process
            every shpobj-coords of shphandle by using Degree2Second rule.
            So it needed to define a function as below:

            def obj_trans(src_obj):
                des_coords = src_obj.coords()
                for lst in des_coords:
                    for i,(x,y) in enumerate(lst):
                        x *= 3600
                        y *= 3600
                        lst[i] = (x,y)
                return shapelib.obj2(src_obj.type, src_obj.id, des_coords)

            shphandle2 = shphandle.translate(r'c:\test2.shp', obj_trans)
        """
        des_shp = self.clone(cloned_shp) if type(cloned_shp) == str else cloned_shp

        if not trans_func:
            for i, obj2 in enumerate(self):
                des_shp[i] = obj2
        elif callable(trans_func):
            for i, obj2 in enumerate(self):
                des_shp[i] = trans_func(obj2)
        else:
            raise SyntaxError(str(trans_func))

        return des_shp

    # -------------------------------------------------------------------------
    def info(*args):
        """shphandle.info()
        Return (obj_count, geom_type, min_list[x,y,z,m], max_list[x,y,z,m]) of shphandle.
        """
        val = apply(shapelibc.ShapeFile_info, args)
        return val

    # -------------------------------------------------------------------------
    def count(self):
        """shphandle.count() or shphandle.rec_count() or len(shphandle)
        Return the shpobj-count of shphandle.
        """
        return self.info()[0]

    # -------------------------------------------------------------------------
    def type(self):
        """shphandle.type()
        Return the geom_type of shphandle.
        """
        return self.info()[1]

    # -------------------------------------------------------------------------
    def box(self):
        """shphandle.box()
        Return (minx, miny, maxx, maxy)
        """
        val = self.info()[2:]
        #        if val[0][0] == val[1][0]:
        #            val[0][0] -= 0.000001
        #            val[1][0] += 0.000001
        #        if val[0][1] == val[1][1]:
        #            val[0][1] -= 0.000001
        #            val[1][1] += 0.000001
        return val[0][0], val[0][1], val[1][0], val[1][1]

    # -------------------------------------------------------------------------
    def read(*args):
        """shphandle.read(obj_id) or shphandle.read_obj(obj_id)
        or shphandle[obj_id] or shphandle(obj_id)
        * The obj_id start from 0. return the obj_id(th) shpobj.
        """
        if not -1 < args[1] < args[0].count():
            raise Exception('Raise an error in reading index=%s of path=%s(count=%s)' % (
                args[1], args[0].file_path, args[0].count()))
        val = apply(shapelibc.ShapeFile_read_object, args)
        if val:
            val = SHPObjectPtr(val)
            val.thisown = 1
            # wzy add begin-------------------
            val.unit = args[0].unit
            val.precise = args[0].precise
            val.distol = args[0].distol
            val.file_path = args[0].file_path
            # wzy add end-------------------
        return val

    # -------------------------------------------------------------------------
    def write(*args):
        """shphandle.write(obj_id, shpobj) or shphandle.write_obj(obj_id, shpobj)
        or shphandle[obj_id] = shpobj or shphandle(obj_id, shpobj)
        * The obj_id start from 0 and can be -1 when write new shpfile by order.
        * The func write the shpobj into shphandle and return the obj_id of shpobj.
        """
        if args[1] < 0:
            args = list(args)
            args[1] = args[0].count()
        val = apply(shapelibc.ShapeFile_write_object, args)
        return val

    # -------------------------------------------------------------------------
    def cobject(*args):
        val = apply(shapelibc.ShapeFile_cobject, args)
        return val

    # -------------------------------------------------------------------------
    def __repr__(self):
        return "<C ShapeFile instance at %s>" % (self.this,)

    # -------------------------------------------------------------------------
    def __str__(self):
        return 'file_path=%s, info=%s' % (self.file_path, self.info())

    # -------------------------------------------------------------------------
    def __iter__(self):
        for i in xrange(self.count()):
            yield self.read(i)

    # -------------------------------------------------------------------------
    def __call__(*args):
        """shphandle(obj_id) is the same as shphandle.read(obj_id);
        shphandle(obj_id, shpobj) is the same as shphandle.write(obj_id) = shpobj
        * The obj_id starts from 0 and can be -1 when write new shpfile by order.
        """
        len_args = len(args)
        if len_args == 2:
            val = apply(shapelibc.ShapeFile_read_object, args)
            if val:
                val = SHPObjectPtr(val)
                val.thisown = 1
        elif len_args == 3:
            val = apply(shapelibc.ShapeFile_write_object, args)
        else:
            raise SyntaxError(str(args))
        return val

    # -------------------------------------------------------------------------
    def __enter__(self):
        return self

    # -------------------------------------------------------------------------
    def __exit__(self):
        self.close()

    # -------------------------------------------------------------------------
    def is_second(self):
        return all(map(lambda x: 1296000 > abs(x) > 360, self.box()))

    # -------------------------------------------------------------------------
    def get_unit(self):
        unit = getattr(self, 'unit', None)
        if unit:
            return unit

        if self.count() == 0:
            unit = ''
        box = self.box()
        if all(map(lambda x: 0 < abs(x) <= 1296000, box)):
            unit = 'S'
        elif all(map(lambda x: 0 <= abs(x) <= 360, box)):
            unit = 'D'
        else:
            unit = 'M'

        if self.precise is None:
            self.precise = 3 if unit == 'S' else 7

        if not isinstance(self.distol, (int, long, float)) or self.distol <= 0:
            self.distol = 0

        return unit

    # -------------------------------------------------------------------------
    def write_objs(self, lst, begid=-1):
        """dbfhandle.write_lines_if(lst, func=None, if_func=None, begid=0)
        * lst is as [dict0, dict1...].
        * If func isn't None, it should return valid-list.
        * If if_func isn't None, it should return True or False.
        * begin starts from 0.
        Return None.
        """
        if begid >= 0:
            enum_lst = enumerate(lst, begid)
        else:
            enum_lst = zip([-1] * len(lst), lst)

        return [self.write(idx, obj2) for idx, obj2 in enum_lst]


# ---------------------------------------------------------------------------------
class ShapeFilePtr(ShapeFile):
    # -------------------------------------------------------------------------
    def __init__(self, this):
        self.this = this
        self.thisown = 0
        self.__class__ = ShapeFile


# -------------- FUNCTION WRAPPERS ------------------
# ---------------------------------------------------------------------------------
def open(*args, **kwargs):
    """shapelib.open(shp_path, mode='rb')
    Return the opened shphandle with inputed mode.
    """
    args = list(args)

    val = apply(shapelibc.open, args)
    if val:
        val = ShapeFilePtr(val)
        val.thisown = 1

        # wzy add begin-----------------
        val.file_path = args[0] if args[0].lower().endswith('.shp') else args[0] + '.shp'
        val.file_path = os.path.abspath(val.file_path)

        val.mode = args[1] if len(args) > 1 else 'rb'
        val.precise = kwargs.get('precise', None)
        val.distol = kwargs.get('distol', 0)
        val.unit = val.get_unit()
        val.geom_type = val.info()[1]

        # wzy add end-----------------
    return val


# ---------------------------------------------------------------------------------
def create(*args, **kwargs):
    """shapelib.create(shp_path, geom_type)
    Return the opened shphandle with 'rb+' mode.
    """
    val = apply(shapelibc.create, args)
    if val:
        val = ShapeFilePtr(val)
        val.thisown = 1

        # wzy add begin-----------------
        val.file_path = args[0] if args[0].lower().endswith('.shp') else args[0] + '.shp'
        val.file_path = os.path.abspath(val.file_path)
        val.mode = 'rb+'
        val.precise = kwargs.get('precise', None)
        val.distol = kwargs.get('distol', 0)
        val.unit = kwargs.get('unit', '')
        val.geom_type = args[1]
        # wzy add end-----------------
    return val


# ---------------------------------------------------------------------------------
c_api = shapelibc.c_api
type_name = shapelibc.type_name
part_type_name = shapelibc.part_type_name
obj = shpobj = SHPObject
# ---------------------------------------------------------------------------------
shpfile = ShapeFile
ShapeFile.__getitem__ = ShapeFile.read_obj = ShapeFile.read
ShapeFile.__setitem__ = ShapeFile.write_obj = ShapeFile.write
ShapeFile.__len__ = ShapeFile.rec_count = ShapeFile.count

# -------------- VARIABLE WRAPPERS ------------------
NULL = SHPT_NULL = shapelibc.SHPT_NULL
POINT = SHPT_POINT = shapelibc.SHPT_POINT
LINE = ARC = SHPT_ARC = shapelibc.SHPT_ARC
AREA = POLYGON = SHPT_POLYGON = shapelibc.SHPT_POLYGON
MPOINT = SHPT_MULTIPOINT = shapelibc.SHPT_MULTIPOINT
POINTZ = SHPT_POINTZ = shapelibc.SHPT_POINTZ
LINEZ = ARCZ = SHPT_ARCZ = shapelibc.SHPT_ARCZ
AREAZ = POLYGONZ = SHPT_POLYGONZ = shapelibc.SHPT_POLYGONZ
MPOINTZ = SHPT_MULTIPOINTZ = shapelibc.SHPT_MULTIPOINTZ
POINTM = SHPT_POINTM = shapelibc.SHPT_POINTM
LINEM = ARCM = SHPT_ARCM = shapelibc.SHPT_ARCM
AREAM = POLYGONM = SHPT_POLYGONM = shapelibc.SHPT_POLYGONM
MPOINTM = SHPT_MULTIPOINTM = shapelibc.SHPT_MULTIPOINTM
SHPT_MULTIPATCH = shapelibc.SHPT_MULTIPATCH
# ---------------------------------------------------------------------------------
TRISTRIP = SHPP_TRISTRIP = shapelibc.SHPP_TRISTRIP
TRIFAN = SHPP_TRIFAN = shapelibc.SHPP_TRIFAN
OUTERRING = SHPP_OUTERRING = shapelibc.SHPP_OUTERRING
INNERRING = SHPP_INNERRING = shapelibc.SHPP_INNERRING
FIRSTRING = SHPP_FIRSTRING = shapelibc.SHPP_FIRSTRING
SHPP_RING = shapelibc.SHPP_RING
# ---------------------------------------------------------------------------------
RB = SHPDBF_R = 'rb'
AB = WB = SHPDBF_W = 'rb+'

# ---------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'cannot be used in main mode.'
