#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from itertools import izip_longest
import dbflibc

__version__ = '0.0.1'
__date__ = '2016/07/07'


class DBFFile:
    # -------------------------------------------------------------------------
    def __init__(self, *args):
        """dbflib.DBFFile(dbf_path, mode='rb'|'rb+')
        Return dbfhandle.
        """
        self.this = apply(dbflibc.new_DBFFile, args)
        self.thisown = 1
        self.file_path = args[0]

    # -------------------------------------------------------------------------
    def __del__(self, lib=dbflibc):
        if self.thisown == 1:
            lib.delete_DBFFile(self)
            self.thisown = 0

    # -------------------------------------------------------------------------
    def close(*args):
        """dbfhandle.close()
        It's not neccesary in some cases when the dbfhandle is out of range.
        """
        val = apply(dbflibc.DBFFile_close, args)
        return val

    # -------------------------------------------------------------------------
    def clone(*args, **kwargs):
        """dbfhandle.clone(dbf_path, globals=globals(), flds=[fld])
        * The globals can be globals(), and if not input globals it will not declare any field.
        * Declare flds as (dbf_name.fld_name = fld_idx). For example, roadsegment.road = 0.
        Return cloned-dbfhandle with rb+ mode.
        """
        dir_path = os.path.dirname(os.path.abspath(args[1]))
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        val = apply(dbflibc.DBFFile_clone, args)
        if val:
            val = DBFFilePtr(val)
            val.thisown = 1
            val.file_path = args[1] if args[1].lower().endswith('.dbf') else args[1] + '.dbf'
            if kwargs.get('globals', False):
                val.declare_all_of_flds(globals=kwargs['globals'])
        return val

    # -------------------------------------------------------------------------
    def fld_count(*args):
        """dbfhandle.fld_count()
        Return the count of fields of dbfhandle.
        """
        val = apply(dbflibc.DBFFile_field_count, args)
        return val

    # -------------------------------------------------------------------------
    def rec_count(*args):
        """dbfhandle.rec_count()
        Return the count of records of dbfhandle.
        """
        val = apply(dbflibc.DBFFile_record_count, args)
        return val

    # -------------------------------------------------------------------------
    def fld_infos(self, flds=None):
        """dbfhandle.fld_infos(flds=None)
        * The flds is fld list or None as all of flds.
        Return tuple(type, upper_name, width, decimal) of all of flds.
        """
        if flds is None:
            infos = tuple(self.fld_info(i) for i in range(self.fld_count()))
        else:
            infos = tuple(self.fld_info(i) for i in flds)
        return infos

    # -------------------------------------------------------------------------
    def fld_infos2(self, flds=None):
        """dbfhandle.fld_infos(flds=None)
        * The flds is fld list or None as all of flds.
        Return tuple(upper_name, type, width, decimal) of all of flds.
        """
        if flds is None:
            infos = tuple(self.fld_info2(i) for i in range(self.fld_count()))
        else:
            infos = tuple(self.fld_info2(i) for i in flds)
        return infos

    # -------------------------------------------------------------------------
    def rec_len(self):
        """dbfhandle.rec_len()
        Return the sum of fileds length of dbfhandle.
        """
        flds_len = sum(a[2] for a in self.fld_infos())
        return flds_len

    # -------------------------------------------------------------------------
    def fld_info(*args):
        """dbfhandle.fld_info(fld_idx)
        * The fld_idx starts from 0.
        Return (type, upper_name, width, decimal) of the fld_idx(th) field.
        """
        if isinstance(args[1], str):
            args = list(args)
            args[1] = args[0].fld_index(args[1])
        val = apply(dbflibc.DBFFile_field_info, args)
        return val

    # -------------------------------------------------------------------------
    def fld_info2(*args):
        """dbfhandle.fld_info2(fld_idx)
        * The fld_idx starts from 0.
        Return (upper_name, type, width, decimal) of the fld_idx(th) field.
        """
        if isinstance(args[1], str):
            args = list(args)
            args[1] = args[0].fld_index(args[1])
        val = apply(dbflibc.DBFFile_field_info, args)
        val2 = (val[1], val[0], val[2], val[3])
        return val2

    # -------------------------------------------------------------------------
    def fld_index(*args):
        """dbfhandle.fld_index(fld_name)
        Return the fld_idx of field. If fld < 0 it will raise IndexError.
        """
        val = apply(dbflibc.DBFFile_field_index, args)
        if val < 0:
            raise IndexError('%s = %d' % (args[1], val))
        return val

    # -------------------------------------------------------------------------
    def fld_index2(*args):
        """dbfhandle.fld_index2(fld_name)
        Return the fld_idx of field. If fld < 0 it will return -1.
        """
        val = apply(dbflibc.DBFFile_field_index, args)
        return val

    # -------------------------------------------------------------------------
    def has_fld(*args):
        """dbfhandle.has_fld(fld_name)
        Return True or False.
        """
        val = apply(dbflibc.DBFFile_field_index, args)
        return True if val > -1 else False

    # -------------------------------------------------------------------------
    def read_line(*args):
        """dbfhandle.read_line(line_idx)
        * The line_idx starts from 0.
        Return the dict as {fld_name:fld_val} includes all of fields.
        """
        if not -1 < args[1] < args[0].count():
            raise Exception('Raise an error in reading rec_index=%s of path=%s(rec_count=%s)' % (
                args[1], args[0].file_path, args[0].count()))
        val = apply(dbflibc.DBFFile_read_record, args)

        if args[0].precise is not None:
            precise = args[0].precise
            xy_flds = args[0].xy_flds
            if xy_flds is None:
                xy_flds = set(val) & {'X_COORD', 'Y_COORD', 'X', 'Y'}
            if xy_flds:
                for k in xy_flds:
                    val[k] = round(val[k], precise)

        if args[0].read_func is not None:
            val = args[0].read_func(val)

        return val

    # -------------------------------------------------------------------------
    def read_attr(*args):
        """dbfhandle.read_attr(line_idx, fld_idx)
        * The line_idx and fld_idx start from 0.
        Return the fld_val.
        """
        if not -1 < args[1] < args[0].count():
            raise Exception('Raise an error in reading rec_index=%s of path=%s(rec_count=%s)' % (
                args[1], args[0].file_path, args[0].count()))
        if not -1 < args[2] < args[0].fld_count():
            raise Exception('Raise an error in reading fld_index=%s of path=%s(fld_count=%s)' % (
                args[2], args[0].file_path, args[0].fld_count()))
        val = apply(dbflibc.DBFFile_read_attribute, args)
        return val

    # -------------------------------------------------------------------------
    def read_attrs_by_idx(*args):
        """dbfhandle.read_attrs_by_idx(line_idx, fld_idx_list)
        * The line_idx start from 0.
        * The fld_idx_list is a list_or_tuple of fld_idxes as [fld_idx_1, fld_idx_2, ...]
        Return the list as (fld_val_1, fld_val_2, ...).
        """
        return tuple([args[0].read_attr(args[1], fld_idx) for fld_idx in args[2]])

    # -------------------------------------------------------------------------
    def read_attrs_by_name(self, line_idx, fld_names, ordered=True, func=None):
        """dbfhandle.read_attrs_by_name(line_idx, fld_names, ordered=True)
        * The line_idx starts from 0.
        * The fld_names is an iterable object, such as ['node', 'type', ...].
        Return a OrderedDict or Dict as {'node':val, 'type':val}.
        """
        x = self.read_line(line_idx)
        if func is None:
            func = (lambda a: a)
        elif not callable(func):
            raise SyntaxError(str(func))

        if fld_names:
            if ordered:
                x = OrderedDict([(fld, func(x[fld])) for fld in fld_names])
            else:
                x = {fld: func(x[fld]) for fld in fld_names}
        return x

    # -------------------------------------------------------------------------
    def add_fld(*args):
        """dbfhandle.add_fld(name, type, width, decimal=0, default=None)
        * The width must > 0;
        * The decimal must >= 0;
        Return the fld_idx.
        """
        fld_idx = args[0].fld_index2(args[1])
        if fld_idx < 0:
            fld_idx = apply(dbflibc.DBFFile_add_field, args[:5])
        if len(args) > 5 and args[5] is not None and fld_idx > -1:
            args[0].write_column(fld_idx, args[2], args[5])
        return fld_idx

    # -------------------------------------------------------------------------
    def add_flds(*args):
        """dbfhandle.add_fld((name1, type1, width1, decimal1),
        (name2, type2, width2, decimal2), ...)
        * The width must > 0;
        * The decimal must >= 0;
        Return the fld_idx.
        """
        fld_idx_list = []
        for fld in args[1:]:
            fld_idx = args[0].fld_index2(fld[0].upper())
            if fld_idx < 0:
                fld_idx = args[0].add_fld(*fld)
            fld_idx_list.append(fld_idx)
        return fld_idx_list

    # -------------------------------------------------------------------------
    def del_fld(*args):
        """dbfhandle.del_fld(fld_idx)
        Return 1 or 0.
        """
        if isinstance(args[1], str):
            args = list(args)
            args[1] = args[0].fld_index2(args[1])
        val = apply(dbflibc.DBFFile_delete_field, args)
        return val

    # -------------------------------------------------------------------------
    def del_flds(*args):
        """dbfhandle.del_fld(flds_list)
        Return 1 or 0.
        """
        if not hasattr(args[1], '__iter__'):
            flds_list = [args[1]]
        else:
            flds_list = args[1]
        ret = []
        for fld in flds_list:
            fld_idx = args[0].fld_index2(fld)
            if fld_idx > -1:
                val = args[0].del_fld(fld_idx)
                ret.append(val)
            else:
                ret.append(0)
        return tuple(ret)

    # -------------------------------------------------------------------------
    def write_line(*args):
        """dbfhandle.write_line(line_idx, dict)
        * The line_idx starts from 0;
        * The dict can be {fld_name:fld_val}.
        """
        if args[1] < 0:
            args = list(args)
            args[1] = args[0].rec_count()
        val = apply(dbflibc.DBFFile_write_record, args)
        return val

    # -------------------------------------------------------------------------
    def write_attr(*args):
        """dbfhandle.write_attr(line_idx, fld_idx, fld_type, val)
        * The line_idx starts from 0;
        * The fld_idx starts from 0;
        Return 1 or 0.
        """
        args = list(args)
        if args[1] < 0:
            args[1] = args[0].rec_count()
        val = apply(dbflibc.DBFFile_write_attribute, args)
        return val

    # -------------------------------------------------------------------------
    def commit(*args):
        val = apply(dbflibc.DBFFile_commit, args)
        return val

    # -------------------------------------------------------------------------
    def __repr__(self):
        return "<C DBFFile instance at %s>" % (self.this,)

    # -------------------------------------------------------------------------
    def __iter__(self):
        for i in xrange(self.rec_count()):
            yield self.read_line(i)

    # -------------------------------------------------------------------------
    def next(self):
        for i in xrange(self.rec_count()):
            yield self.read_line(i)

    # -------------------------------------------------------------------------
    def __call__(*args):
        """dbfhandle(line_idx) <==> dbfhandle.read_line(line_idx);
        dbfhandle(line_idx, fld_idx) <==> dbfhandle.read_attr(line_idx, fld_idx);
        dbfhandle(line_idx, dict) <==> dbfhandle.write_line(line_idx, dict);
        dbfhandle(line_idx, fld_idx, fld_type, val)
        <==> dbfhandle.write_attr(line_idx, fld_idx, fld_type, val);
        """
        len_args = len(args)
        if len_args == 2:
            return apply(dbflibc.DBFFile_read_record, args)
        elif len_args == 3:
            if hasattr(args[2], 'bit_length'):
                return apply(dbflibc.DBFFile_read_attribute, args)
            else:
                return apply(dbflibc.DBFFile_write_record, args)
        elif len_args == 5:
            return apply(dbflibc.DBFFile_write_attribute, args)
        else:
            raise SyntaxError(str(args))

    # -------------------------------------------------------------------------
    def read(*args):
        """dbfhandle.read(line_idx) <==> dbfhandle.read_line(line_idx);
        dbfhandle.read(line_idx, fld_idx) <==> dbfhandle.read_attr(line_idx, fld_idx).
        """
        len_args = len(args)
        if len_args == 2:
            return apply(dbflibc.DBFFile_read_record, args)
        elif len_args == 3 and hasattr(args[2], 'bit_length'):
            return apply(dbflibc.DBFFile_read_attribute, args)
        else:
            raise SyntaxError(str(args))

    # -------------------------------------------------------------------------
    def write(*args):
        """dbfhandle.write(line_idx, dict) <==> dbfhandle.write_line(line_idx, dict);
        dbfhandle.write(line_idx, fld_idx, fld_type, val)
        <==> dbfhandle.write_attr(line_idx, fld_idx, fld_type, val).
        """
        len_args = len(args)
        if len_args == 5:
            return apply(dbflibc.DBFFile_write_attribute, args)
        elif len_args == 3 and hasattr(args[2], '__iter__'):
            return apply(dbflibc.DBFFile_write_record, args)
        else:
            raise SyntaxError(str(args))

    # -------------------------------------------------------------------------
    def __enter__(self):
        return self

    # -------------------------------------------------------------------------
    def __exit__(self):
        self.close()

    # -------------------------------------------------------------------------
    def read_column(self, fld_idx, func=None):
        """dbfhandle.read_column(fld_idx, func=None)
        * If func isn't None, it should return valid-value.
        Return the val-list of fld.
        """
        if isinstance(fld_idx, str):
            fld_idx = self.fld_index(fld_idx)

        if not func:
            return [self.read_attr(i, fld_idx) for i in xrange(self.rec_count())]
        elif callable(func):
            return [func(self.read_attr(i, fld_idx)) for i in xrange(self.rec_count())]
        else:
            raise SyntaxError(str(func))

    # -------------------------------------------------------------------------
    def read_columns(self, fld_idx_list=None, func=None):
        """dbfhandle.read_columns(fld_idx_list=[], func=None)
        * The fld_idx_list can be a [fld_idx,] to return fld_vals defined,
            and its default is [] to return all of fld_vals.
        * If func isn't None, it should return valid-list.
        For example, if fld_idx_list is [1,3,...] it will return [[ln0-fld1,ln0-fld3,...],].
        Return the val-list of fld.
        """
        if not fld_idx_list:
            fld_idx_list = [self.fld_index(fldinfo[0]) for fldinfo in self.fld_infos2()]

        if not hasattr(fld_idx_list, '__iter__'):
            raise SyntaxError("fld_idx_list isn't iterable.")

        fld_idx_list = [(self.fld_index(fld) if isinstance(fld, str) else fld) for fld in
                        fld_idx_list]

        if not func:
            if fld_idx_list:
                return [[self.read_attr(ln, fld_idx) for fld_idx in fld_idx_list] for ln in
                        xrange(self.rec_count())]
            else:
                return [self.read_line(ln) for ln in xrange(self.rec_count())]
        elif callable(func):
            if fld_idx_list:
                return [func(*[self.read_attr(ln, fld_idx) for fld_idx in fld_idx_list]) for ln in
                        xrange(self.rec_count())]
            else:
                return [func(self.read_line(ln)) for ln in xrange(self.rec_count())]
        else:
            raise SyntaxError(str(func))

    # -------------------------------------------------------------------------
    def read_lines_if(self, func=None, if_func=None, ret_map=None, ret_notif=None, ret_shp=None,
                      ret_idx=None, ordered=True):
        """dbfhandle.read_lines_if(func=None, if_func=None)
        * If func isn't None, it should return valid-list.
        * If if_func isn't None, it should return True or False.
        Return [func(a) for a in self if if_func(a)].
        """
        if not func:
            func = (lambda s: s)
        if not if_func:
            if_func = (lambda s: 1)
        if ret_shp:
            import shapelib as shp
            feat_shp = shp.open(ret_shp) if isinstance(ret_shp, str) else ret_shp
        else:
            feat_shp = None

        if not ret_idx:
            ret_idx = None

        if ret_map:
            if isinstance(ret_map, (tuple, list)) and len(ret_map) > 0:
                if len(ret_map) == 1:
                    ret_map = list(ret_map)
                    ret_map.append([])
                key_flds = [f.strip().upper() for f in ret_map[0] if f]
                val_flds = [f.strip().upper() for f in ret_map[1] if f]

                def map_func(db):
                    len_key_flds = len(key_flds)
                    for a in db:
                        key = tuple([a[fld] for fld in key_flds]) if len_key_flds > 1 \
                            else a[key_flds[0]]
                        val = {fld: a[fld] for fld in val_flds} if val_flds else a
                        yield (key, val)
            else:
                map_func = enumerate

            ret = OrderedDict() if ordered else dict()
            for i, (k, v) in enumerate(map_func(self)):
                if feat_shp is not None:
                    v['<SHP>'] = feat_shp[i]
                if ret_idx is not None:
                    v['<IDX>'] = i
                if if_func(v):
                    ret[k] = func(v)
                elif ret_notif is not None:
                    ret_notif[k] = func(v)

        else:
            ret = []
            for i, ln in enumerate(self):
                if feat_shp is not None:
                    ln['<SHP>'] = feat_shp[i]
                if ret_idx is not None:
                    ln['<IDX>'] = i
                if if_func(ln):
                    ret.append(func(ln))
                elif ret_notif is not None:
                    ret_notif.append(func(ln))

        return ret

    # -------------------------------------------------------------------------
    def write_lines_if(self, lst, func=None, if_func=None, begid=-1):
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
            enum_lst = izip_longest([], lst, fillvalue=-1)
        # enum_lst = zip([-1]*len(lst), lst)
        if callable(func) and callable(if_func):
            return [self.write_line(idx, func(ln)) for idx, ln in enum_lst if if_func(ln)]
        elif callable(func):
            return [self.write_line(idx, func(ln)) for idx, ln in enum_lst]
        elif callable(if_func):
            return [self.write_line(idx, ln) for idx, ln in enum_lst if if_func(ln)]
        else:
            return [self.write_line(idx, ln) for idx, ln in enum_lst]

    # -------------------------------------------------------------------------
    def write_column(self, fld_idx, fld_type, lst, func=None):
        """dbfhandle.write_column(fld_idx, fld_type, iterable_or_val, func=None)
        * The iterable can be a list or tuple and its length should be <= dbfhandle.rec_count().
        * The val can be a string or int or float which type fits to fld_type defined.
        * The func can be callable to translate iterable_or_val, and default is None.
        """
        if isinstance(fld_idx, str):
            fld_idx = self.fld_index(fld_idx)
        if hasattr(lst, '__iter__') and not isinstance(lst, str):
            if not func:
                return [self.write_attr(i, fld_idx, fld_type, x) for i, x in enumerate(lst)]
            elif callable(func):
                return [self.write_attr(i, fld_idx, fld_type, func(x)) for i, x in enumerate(lst)]
            else:
                raise SyntaxError(str(func))
        else:
            if callable(func):
                lst = func(lst)
            return [self.write_attr(i, fld_idx, fld_type, lst) for i in xrange(self.rec_count())]

    # -------------------------------------------------------------------------
    def write_columns(self, fld_val_list, func=None):
        """dbfhandle.write_columns(fld_val_list, func=None)
        * The fld_val_list must be a list as [{fld_name:val},]
        and its length should be <= dbfhandle.rec_count().
        * The func can be callable to translate every line-data in fld_val_list,
        and default is None.
        """
        if hasattr(fld_val_list, '__iter__'):
            if len(fld_val_list) > self.rec_count() > 0:
                raise OverflowError
            if not func:
                return [self.write_line(i, data) for i, data in enumerate(fld_val_list)]
            elif callable(func):
                return [self.write_line(i, func(data)) for i, data in enumerate(fld_val_list)]
            else:
                raise SyntaxError(str(func))
        else:
            raise SyntaxError("fld_val_list isn't iterable.")

    # -------------------------------------------------------------------------
    def write_attrs_by_idx(self, rec_idx, fld_idx_list, fld_val_list, func=None):
        """dbfhandle.write_attrs_by_idx(fld_idx_list, fld_val_list, func=None)
        * The fld_idx_list must be a list as [(fld_idx_0,fld_type_0), ..., (fld_idx_n, fld_type_n)].
        * The fld_val_list must be a list as [fld_val_0, ..., fld_val_n] and its length should be
        <= dbfhandle.rec_count().
        * The func can be callable to translate every line-data in fld_val_list,
        and default is None.
        """
        if not hasattr(fld_idx_list, '__iter__'):
            raise SyntaxError("fld_idx_list isn't iterable.")

        if hasattr(fld_val_list, '__iter__'):
            if rec_idx > self.rec_count():
                raise OverflowError('rec_idx=%d > self.rec_count()' % rec_idx)
            if not func:
                return [self.write_attr(rec_idx, fld_idx, fld_type, fld_val) for
                        (fld_idx, fld_type), fld_val in zip(fld_idx_list, fld_val_list)]
            elif callable(func):
                return [self.write_attr(rec_idx, fld_idx, fld_type, func(fld_val)) for
                        (fld_idx, fld_type), fld_val in zip(fld_idx_list, fld_val_list)]
            else:
                raise SyntaxError(str(func))
        elif type(fld_val_list) in (str, int, float, long):
            return [self.write_attr(rec_idx, fld_idx, fld_type, fld_val_list) for
                    (fld_idx, fld_type) in fld_idx_list]
        else:
            raise SyntaxError("fld_val_list isn't iterable.")

    # -------------------------------------------------------------------------
    def fld_list(self):
        """dbfhandle.fld_list()
        Return [(fld_name, fld_idx),...]
        """
        return [(self.fld_info(i)[1], i) for i in xrange(self.fld_count())]

    # -------------------------------------------------------------------------
    def fldname_list(self):
        """dbfhandle.fldname_list()
        Return [fld_name,...]
        """
        return tuple([self.fld_info(i)[1] for i in xrange(self.fld_count())])

    # -------------------------------------------------------------------------
    def fld_dict(self):
        """dbfhandle.fld_dict()
        Return {fld_name : fld_idx}
        """
        return dict(self.fld_list())

    # -------------------------------------------------------------------------
    def declare_all_of_flds(self, globals, redeclare=False):
        """dbfhandle.declare_all_of_flds(globals, flds=None)
        Declare all of flds(dbf_name.fld_name = fld_idx).
        For example, roadsegment.road = 0.
        """
        import os
        dbf_name = self.file_path.rpartition(os.sep)[2].lower().strip()
        if dbf_name[-4:] == '.dbf':
            dbf_name = dbf_name[:-4]

        if dbf_name not in globals or redeclare:
            exec ('class %s(object):__hasfld__=0' % dbf_name, globals)
        # exec('print %s, dir(%s)' % (dbf_name, dbf_name), globals)
        fld_count = self.fld_count()
        if globals[dbf_name].__hasfld__ != fld_count:
            exec ('%s.__hasfld__=%d' % (dbf_name, fld_count), globals)
            for fld in self.fld_list():
                exec ('%s.%s = %d' % (dbf_name, fld[0].lower(), fld[1]), globals)

    # -------------------------------------------------------------------------
    def translate(self, cloned_dbf, trans_func=None):
        """dbfhandle.translate(cloned_dbf, trans_func=None)
        Firstly, clone dbfhandle as cloned_dbf, translate every line-rec with trans_func
        and write it into the cloned_dbf, and return cloned_dbf at last.
        * The cloned_dbf can be a dbf-path or dbfhandle.
        * The trans_func can be a function to translate src-line and return des-line.
            If the trans_func is None the function will copy src-line to des-line.
        """
        des_dbf = self.clone(cloned_dbf) if type(cloned_dbf) == str else cloned_dbf

        if not trans_func:
            for i, line in enumerate(self):
                des_dbf[i] = line
        elif callable(trans_func):
            for i, line in enumerate(self):
                des_dbf[i] = trans_func(line)
        else:
            raise SyntaxError(str(trans_func))

        return des_dbf

    if not dbflibc._have_commit:
        del commit


# -------------------------------------------------------------------------
class DBFFilePtr(DBFFile):
    def __init__(self, this):
        self.this = this
        self.thisown = 0
        self.__class__ = DBFFile


# -------------- FUNCTION WRAPPERS ------------------
def open(*args, **kwargs):
    """dbflib.open(dbf_path, mode, globals=globals())
    * The mode can be 'rb'(default) or 'rb+'.
    * The globals can be globals(), and if not input globals it will not declare any field.
    * The flds can be an iterable, and if input globals() will declare all of fields.
    * Declare flds as (dbf_name.fld_name = fld_idx). For example, roadsegment.road = 0.
    Return opened dbfhandle.
    """
    args = list(args)

    val = apply(dbflibc.open, args)
    if val:
        val = DBFFilePtr(val)
        val.thisown = 1
        val.file_path = args[0] if args[0].lower().endswith('.dbf') else args[0] + '.dbf'
        val.file_path = os.path.abspath(val.file_path)

        if kwargs.get('globals', False):
            val.declare_all_of_flds(globals=kwargs['globals'])

        val.precise = kwargs.get('precise', None)
        if val.precise is not None:
            val.precise = int(val.precise)
        val.xy_flds = None

        val.read_func = kwargs.get('read_func', None)
        if not callable(val.read_func):
            val.read_func = None

    return val


# -------------------------------------------------------------------------
def create(*args, **kwargs):
    """dbflib.create(dbf_path)
    Return created dbfhandle with rb+ mode.
    """
    val = apply(dbflibc.create, args)
    if val:
        val = DBFFilePtr(val)
        val.thisown = 1
        val.file_path = args[0] if args[0].lower().endswith('.dbf') else args[0] + '.dbf'
        val.precise = kwargs.get('precise', None)
        if val.precise is not None:
            val.precise = int(val.precise)
        val.xy_flds = None

        val.read_func = kwargs.get('read_func', None)
        if not callable(val.read_func):
            val.read_func = None

    return val


# -------------------------------------------------------------------------
STR = FTString = dbflibc.FTString
INT = FTInteger = dbflibc.FTInteger
DBL = FTDouble = dbflibc.FTDouble
FTInvalid = dbflibc.FTInvalid
_have_commit = dbflibc._have_commit

RB = SHPDBF_R = 'rb'
AB = WB = SHPDBF_W = 'rb+'

DBFFile.__getitem__ = DBFFile.read_line
DBFFile.__setitem__ = DBFFile.write_line
DBFFile.__len__ = DBFFile.count = DBFFile.rec_count
dbffile = DBFFile

# -------------------------------------------------------------------------
if __name__ == '__main__':
    print 'cannot be used in main mode.'
